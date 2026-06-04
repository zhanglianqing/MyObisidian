"""
Export offline color-FA as RGB DICOM.

Formats:
  ge-display  — 509 canvas, AW overlays, GE private tag (screen-save style)
  generic     — 509 canvas, same orient/crop/colors as AW display, patient tags + overlay,
                standard SC without MR IOP/IPP (bitmap = display)

jiang generic:
  python export_colorfa_dicom.py --format generic ^
    --rgb_nii jiang_offline_output/jiang_offline_colorFA_rgb.nii.gz ^
    --fa_nii jiang_offline_output/jiang_offline_fa.nii.gz ^
    --dicom_dir DICOM/PA0/ST0/SE6 ^
    --out_dir jiang_offline_output/DICOM_ColorFA_generic
"""
from __future__ import annotations

import argparse
from pathlib import Path

import nibabel as nib
import numpy as np
import pydicom
from pydicom.dataset import Dataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid

from aw_style_axial_export import (
    CANVAS,
    DEFAULT_MIN_FA,
    apply_fixed_crop,
    apply_min_fa_mask,
    compute_fixed_crop_box,
    draw_aw_overlay,
    fit_to_canvas,
    load_patient_meta,
    render_clinical_rgb_slice,
    to_radiological_axial,
    to_uint8_rgb,
)


def render_display_frames(
    rgb_vol: np.ndarray,
    fa_vol: np.ndarray | None,
    meta: dict,
    z_positions_mm: np.ndarray | None,
    min_fa: float,
    flip_ap: bool,
    flip_lr: bool,
) -> list[np.ndarray]:
    n = rgb_vol.shape[2]
    crop_box = compute_fixed_crop_box(rgb_vol, fa_vol, min_fa, flip_ap, flip_lr)
    frames = []
    for k in range(n):
        sl = render_clinical_rgb_slice(
            rgb_vol, fa_vol, k, crop_box, min_fa, flip_ap, flip_lr, canvas_size=CANVAS
        )
        img = Image.fromarray(sl, mode="RGB")
        loc = float(z_positions_mm[k]) if z_positions_mm is not None else None
        draw_aw_overlay(img, meta, k, n, loc)
        frames.append(np.array(img))
    return frames
from PIL import Image


def load_study_template(dicom_dir: Path) -> pydicom.Dataset:
    for p in sorted(dicom_dir.glob("**/*")):
        if not p.is_file():
            continue
        try:
            ds = pydicom.dcmread(str(p), stop_before_pixels=True, force=True)
        except Exception:
            continue
        if str(getattr(ds, "Modality", "")) == "MR":
            return pydicom.dcmread(str(p), stop_before_pixels=True, force=True)
    raise FileNotFoundError("No MR DICOM in %s" % dicom_dir)


def copy_patient_study_tags(target: pydicom.Dataset, source: pydicom.Dataset) -> None:
    """Copy standard patient/study attributes (no series/instance UIDs)."""
    for elem in source:
        g = elem.tag.group
        if g in (0x0008, 0x0010, 0x0020):
            if elem.tag in (
                (0x0008, 0x0018),
                (0x0020, 0x000D),
                (0x0020, 0x000E),
                (0x0020, 0x0011),
                (0x0020, 0x0013),
            ):
                continue
            target[elem.tag] = elem


def strip_spatial_tags(ds: pydicom.Dataset) -> None:
    """SC bitmap matches display; do not claim MR slice geometry."""
    for name in (
        "ImageOrientationPatient",
        "ImagePositionPatient",
        "SliceLocation",
        "SliceThickness",
        "SpacingBetweenSlices",
        "PixelSpacing",
        "FrameOfReferenceUID",
        "PositionReferenceIndicator",
    ):
        if name in ds:
            del ds[name]


def strip_private_tags(ds: pydicom.Dataset) -> None:
    remove = [elem.tag for elem in ds if elem.tag.group % 2 == 1]
    for tag in remove:
        del ds[tag]


def write_ge_display_series(
    frames: list[np.ndarray],
    template: pydicom.Dataset,
    out_dir: Path,
    series_description: str,
    series_number: int,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    series_uid = generate_uid()
    study_uid = getattr(template, "StudyInstanceUID", None) or generate_uid()
    for i, px in enumerate(frames):
        ds = Dataset()
        ds.file_meta = Dataset()
        ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
        ds.file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.7"
        sop = generate_uid()
        ds.file_meta.MediaStorageSOPInstanceUID = sop
        ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.7"
        ds.SOPInstanceUID = sop
        ds.Modality = "MR"
        copy_patient_study_tags(ds, template)
        ds.StudyInstanceUID = study_uid
        ds.SeriesInstanceUID = series_uid
        ds.Manufacturer = getattr(template, "Manufacturer", "OFFLINE")
        ds.SeriesDescription = series_description
        ds.SeriesNumber = series_number
        ds.InstanceNumber = i + 1
        ds.ImageType = ["DERIVED", "SECONDARY", "SCREEN SAVE"]
        ds.SamplesPerPixel = 3
        ds.PhotometricInterpretation = "RGB"
        ds.PlanarConfiguration = 0
        ds.Rows, ds.Columns = px.shape[0], px.shape[1]
        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.is_little_endian = True
        ds.is_implicit_VR = False
        ds.PixelData = px.tobytes()
        ds.add_new(0x00511002, "LO", "Colored orientation")
        ds.save_as(str(out_dir / ("IM%d" % i)), write_like_original=False)
    print("Wrote %d GE-style DICOM -> %s" % (len(frames), out_dir))


def write_generic_series(
    rgb_vol: np.ndarray,
    fa_vol: np.ndarray | None,
    study_template: pydicom.Dataset,
    meta: dict,
    out_dir: Path,
    series_description: str,
    series_number: int,
    min_fa: float,
    flip_ap: bool,
    flip_lr: bool,
    z_positions_mm: np.ndarray | None = None,
    canvas_size: int = CANVAS,
) -> None:
    """Same 509 layout + full overlay as offline_axial_png; no GE private tags / no MR IOP."""
    out_dir.mkdir(parents=True, exist_ok=True)
    n = rgb_vol.shape[2]
    crop_box = compute_fixed_crop_box(rgb_vol, fa_vol, min_fa, flip_ap, flip_lr)
    series_uid = generate_uid()
    study_uid = study_template.StudyInstanceUID

    for k in range(n):
        px = render_clinical_rgb_slice(
            rgb_vol, fa_vol, k, crop_box, min_fa, flip_ap, flip_lr, canvas_size
        )
        img = Image.fromarray(px, mode="RGB")
        loc = float(z_positions_mm[k]) if z_positions_mm is not None else None
        draw_aw_overlay(img, meta, k, n, loc)
        px = np.array(img)

        ds = Dataset()
        ds.file_meta = Dataset()
        ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
        ds.file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.7"
        sop = generate_uid()
        ds.file_meta.MediaStorageSOPInstanceUID = sop
        ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.7"
        ds.SOPInstanceUID = sop
        copy_patient_study_tags(ds, study_template)
        ds.StudyInstanceUID = study_uid
        ds.SeriesInstanceUID = series_uid
        ds.Modality = "MR"
        ds.Manufacturer = "OFFLINE_DTI"
        ds.ManufacturerModelName = "Dipy"
        ds.SeriesDescription = series_description
        ds.SeriesNumber = series_number
        ds.InstanceNumber = k + 1
        ds.ImageType = ["DERIVED", "SECONDARY", "OTHER"]
        ds.SamplesPerPixel = 3
        ds.PhotometricInterpretation = "RGB"
        ds.PlanarConfiguration = 0
        ds.Rows, ds.Columns = px.shape[0], px.shape[1]
        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.is_little_endian = True
        ds.is_implicit_VR = False
        ds.BurnedInAnnotation = "YES"
        ds.ImageComments = "DTI DEC map; FA>=%.2f; display-aligned" % min_fa
        strip_spatial_tags(ds)
        strip_private_tags(ds)
        ds.PixelData = np.ascontiguousarray(px).tobytes()
        ds.save_as(str(out_dir / ("IM%04d.dcm" % k)), write_like_original=False)

    print("Wrote %d generic DICOM (%dx%d) -> %s" % (n, canvas_size, canvas_size, out_dir))
    print("SeriesInstanceUID:", series_uid)


def main() -> None:
    ap = argparse.ArgumentParser(description="Export color FA as RGB DICOM")
    ap.add_argument(
        "--format",
        choices=("ge-display", "generic"),
        default="generic",
    )
    ap.add_argument("--rgb_nii", type=Path, required=True)
    ap.add_argument("--fa_nii", type=Path, default=None)
    ap.add_argument("--dicom_dir", type=Path, required=True)
    ap.add_argument("--out_dir", type=Path, required=True)
    ap.add_argument("--series_desc", type=str, default=None)
    ap.add_argument("--series_number", type=int, default=None)
    ap.add_argument("--min-fa", type=float, default=DEFAULT_MIN_FA)
    ap.add_argument("--flip-ap", action="store_true")
    ap.add_argument("--flip-lr", action="store_true")
    ap.add_argument("--png_dir", type=Path, default=None)
    ap.add_argument(
        "--canvas",
        type=int,
        default=CANVAS,
        help="generic square size (default 509, same as offline_axial_png)",
    )
    args = ap.parse_args()

    rgb = nib.load(str(args.rgb_nii)).get_fdata()
    fa = (
        nib.load(str(args.fa_nii)).get_fdata()
        if args.fa_nii and args.fa_nii.is_file()
        else None
    )
    study_tpl = load_study_template(args.dicom_dir)
    meta = load_patient_meta(args.dicom_dir)

    if args.format == "generic":
        z_mm = None
        try:
            aff = nib.load(str(args.rgb_nii)).affine
            z_mm = np.array([aff[2, 2] * k + aff[2, 3] for k in range(rgb.shape[2])])
        except Exception:
            pass
        write_generic_series(
            rgb,
            fa,
            study_tpl,
            meta,
            args.out_dir,
            args.series_desc or "DTI Color FA (DEC map)",
            args.series_number if args.series_number is not None else 901,
            args.min_fa,
            args.flip_ap,
            args.flip_lr,
            z_mm,
            args.canvas,
        )
        return

    desc = args.series_desc or "Offline Axial Colored orientation"
    sn = args.series_number if args.series_number is not None else 900
    z_mm = None
    try:
        aff = nib.load(str(args.rgb_nii)).affine
        z_mm = np.array([aff[2, 2] * k + aff[2, 3] for k in range(rgb.shape[2])])
    except Exception:
        pass
    frames = render_display_frames(
        rgb, fa, meta, z_mm, args.min_fa, args.flip_ap, args.flip_lr
    )
    if args.png_dir:
        args.png_dir.mkdir(parents=True, exist_ok=True)
        for i, fr in enumerate(frames):
            Image.fromarray(fr).save(args.png_dir / ("slice_%02d.png" % i))
        print("Wrote PNGs ->", args.png_dir)
    write_ge_display_series(frames, study_tpl, args.out_dir, desc, sn)


if __name__ == "__main__":
    main()
