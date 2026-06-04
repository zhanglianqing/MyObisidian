"""
One-shot offline Color FA: DTI fit -> NIfTI + DICOM (jiang).

  python run_offline_colorfa.py

View DICOM_ColorFA_generic in RadiAnt / Weasis / online DICOM viewers.
Optional PNG: aw_style_axial_export.py (not run by default).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import nibabel as nib
from dipy.io.image import save_nifti

from aw_style_axial_export import load_patient_meta
from dti_core import fit_color_fa
from export_colorfa_dicom import load_study_template, write_generic_series

DTI_DIR = Path("DICOM/PA0/ST0/SE6")
OUT_DIR = Path("jiang_offline_output")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-fit", action="store_true", help="use existing *_colorFA_rgb.nii.gz")
    ap.add_argument("--dti", type=Path, default=DTI_DIR, help="source DTI DICOM series folder")
    ap.add_argument("--out", type=Path, default=OUT_DIR, help="output root (NIfTI + DICOM_ColorFA_generic)")
    args = ap.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    work = out / "_work"
    rgb_p = out / "jiang_offline_colorFA_rgb.nii.gz"
    fa_p = out / "jiang_offline_fa.nii.gz"

    if args.skip_fit and rgb_p.is_file() and fa_p.is_file():
        cfa = nib.load(str(rgb_p)).get_fdata().astype(np.float32)
        fa = nib.load(str(fa_p)).get_fdata().astype(np.float32)
        aff = nib.load(str(rgb_p)).affine
    else:
        cfa, aff, tenfit, _ = fit_color_fa(args.dti, work)
        save_nifti(str(rgb_p), cfa, aff)
        save_nifti(str(fa_p), tenfit.fa.astype("float32"), aff)
        fa = tenfit.fa
        print("Saved", rgb_p, fa_p)

    if cfa.max() > 1.5:
        cfa = cfa / 255.0

    meta = load_patient_meta(args.dti)
    z_mm = None
    try:
        z_mm = np.array([aff[2, 2] * k + aff[2, 3] for k in range(cfa.shape[2])])
    except Exception:
        pass

    write_generic_series(
        cfa,
        fa,
        load_study_template(args.dti),
        meta,
        out / "DICOM_ColorFA_generic",
        "DTI Color FA (DEC map)",
        901,
        0.18,
        False,
        False,
        z_mm,
    )
    print("Done ->", out)


if __name__ == "__main__":
    main()
