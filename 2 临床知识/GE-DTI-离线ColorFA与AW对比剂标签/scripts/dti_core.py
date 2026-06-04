"""DTI conversion, GE gradient extraction, tensor fit + color FA."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np
import pydicom
from dipy.core.gradients import gradient_table
from dipy.io.gradients import read_bvals_bvecs
from dipy.io.image import load_nifti
from dipy.reconst.dti import TensorModel, color_fa
from dipy.segment.mask import median_otsu

try:
    import dcm2niix
except ImportError:
    dcm2niix = None


def find_bval_bvec(nifti_path: Path) -> tuple[Path | None, Path | None]:
    stem = str(nifti_path).replace(".nii.gz", "").replace(".nii", "")
    bval = Path(stem + ".bval")
    bvec = Path(stem + ".bvec")
    if bval.is_file() and bvec.is_file():
        return bval, bvec
    return None, None


def write_bval_bvec(nifti_path: Path, bvals: np.ndarray, bvecs: np.ndarray) -> None:
    stem = str(nifti_path).replace(".nii.gz", "").replace(".nii", "")
    np.savetxt(stem + ".bval", bvals.reshape(1, -1), fmt="%.6g")
    np.savetxt(stem + ".bvec", bvecs.T, fmt="%.6g")


def extract_ge_bvals_bvecs(dicom_dir: Path) -> tuple[np.ndarray, np.ndarray]:
    by_grad: dict[tuple[float, tuple[float, float, float]], list[int]] = defaultdict(list)
    for p in sorted(dicom_dir.glob("**/*"), key=lambda x: x.name):
        if not p.is_file():
            continue
        try:
            ds = pydicom.dcmread(str(p), stop_before_pixels=True, force=True)
        except Exception:
            continue
        if not hasattr(ds, "DiffusionBValue"):
            if ds.get((0x0019, 0x10BB)) is None:
                continue
        b = float(getattr(ds, "DiffusionBValue", 0) or 0)
        tags = ((0x0019, 0x10BB), (0x0019, 0x10BC), (0x0019, 0x10BD))
        if not all(ds.get(t) for t in tags):
            continue
        g = tuple(float(ds[t].value) for t in tags)
        by_grad[(b, g)].append(int(getattr(ds, "InstanceNumber", 0)))
    if not by_grad:
        raise RuntimeError("No GE diffusion tags (0019,10BB/BC/BD) in %s" % dicom_dir)
    vols = sorted(((min(v), b, g) for (b, g), v in by_grad.items()), key=lambda x: x[0])
    bvals = np.array([x[1] for x in vols], dtype=np.float64)
    bvecs = np.array([x[2] for x in vols], dtype=np.float64)
    bvecs[:, 0] *= -1
    return bvals, bvecs


def dicom_to_nifti_dcm2niix(dicom_dir: Path, work_dir: Path) -> Path:
    if dcm2niix is None:
        raise RuntimeError("pip install dcm2niix")
    work_dir.mkdir(parents=True, exist_ok=True)
    result = dcm2niix.main(
        ["-z", "y", "-f", "%p_%s", "-o", str(work_dir), str(dicom_dir)],
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    nii = sorted(work_dir.glob("*.nii.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not nii:
        raise RuntimeError("dcm2niix produced no NIfTI")
    return nii[0]


def load_gradients(nii_path: Path, dicom_dir: Path) -> tuple[np.ndarray, np.ndarray]:
    bval_p, bvec_p = find_bval_bvec(nii_path)
    if bval_p and bvec_p:
        return read_bvals_bvecs(str(bval_p), str(bvec_p))
    bvals, bvecs = extract_ge_bvals_bvecs(dicom_dir)
    write_bval_bvec(nii_path, bvals, bvecs)
    return bvals, bvecs


def fit_color_fa(dicom_dti_dir: Path, work_dir: Path):
    work_dir.mkdir(parents=True, exist_ok=True)
    nii_path = dicom_to_nifti_dcm2niix(dicom_dti_dir, work_dir)
    data, affine = load_nifti(str(nii_path))
    bvals, bvecs = load_gradients(nii_path, dicom_dti_dir)
    if len(bvals) != data.shape[-1]:
        raise RuntimeError("NIfTI volumes %d != gradients %d" % (data.shape[-1], len(bvals)))
    gtab = gradient_table(bvals, bvecs=bvecs)
    _, mask = median_otsu(
        data, vol_idx=range(1, min(10, data.shape[-1])), median_radius=2, numpass=1
    )
    tenfit = TensorModel(gtab).fit(data, mask=mask)
    cfa = np.clip(color_fa(tenfit.fa, tenfit.evecs), 0, 1).astype(np.float32)
    return cfa, affine, tenfit, nii_path
