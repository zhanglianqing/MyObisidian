"""
Export offline axial color-FA PNGs styled for comparison with GE AW screen captures.

Fixes vs raw offline_axial_png:
  - Radiological axial orientation (A top, R on screen-left)
  - Fixed crop from central slice(s) + pad to 509 canvas (same FOV all slices)
  - Color: linear scale from Dipy color_fa (no extra histogram/gamma boost)
  - Patient / scan text overlays (yellow, AW-style positions)
"""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import nibabel as nib
import numpy as np
import pydicom
from PIL import Image, ImageDraw, ImageFont


CANVAS = 509
MARGIN_PCT = 0.08
DEFAULT_MIN_FA = 0.18


def load_patient_meta(dicom_dir: Path) -> dict:
    for p in sorted(dicom_dir.glob("**/*")):
        if not p.is_file():
            continue
        try:
            ds = pydicom.dcmread(str(p), stop_before_pixels=True, force=True)
        except Exception:
            continue
        if str(getattr(ds, "Modality", "")) != "MR":
            continue
        name = str(getattr(ds, "PatientName", "ANON")).replace("^", " ")
        study = str(getattr(ds, "StudyDate", ""))
        try:
            ex = datetime.strptime(study, "%Y%m%d").strftime("Ex: %b %d %Y")
        except ValueError:
            ex = "Ex: " + study
        thick = float(getattr(ds, "SliceThickness", 5) or 5)
        sp = float(getattr(ds, "SpacingBetweenSlices", thick) or thick)
        series = int(getattr(ds, "SeriesNumber", 6))
        proto = str(getattr(ds, "ProtocolName", "-HX-Brain-DTI+c(48CH)"))
        return {
            "name": name,
            "exam": ex,
            "series": series,
            "protocol": proto,
            "thick": thick,
            "spacing": sp,
        }
    return {"name": "ANON", "exam": "", "series": 6, "protocol": "", "thick": 5.0, "spacing": 5.0}


def to_radiological_axial(
    sl: np.ndarray,
    flip_ap: bool = False,
    flip_lr: bool = False,
) -> np.ndarray:
    """(L,A,3) from NIfTI (axcodes L,A,S) -> screen axial; default rot90 + fliplr (radiological)."""
    sl = np.rot90(sl, k=1)
    sl = np.fliplr(sl)
    if flip_ap:
        sl = np.flipud(sl)
    if flip_lr:
        sl = np.fliplr(sl)
    return sl


def _bbox_from_mask(mask: np.ndarray, pad_frac: float) -> tuple[int, int, int, int] | None:
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    h, w = mask.shape
    dy = int((y1 - y0 + 1) * pad_frac)
    dx = int((x1 - x0 + 1) * pad_frac)
    y0 = max(0, y0 - dy)
    y1 = min(h - 1, y1 + dy)
    x0 = max(0, x0 - dx)
    x1 = min(w - 1, x1 + dx)
    return y0, y1, x0, x1


def compute_fixed_crop_box(
    rgb_vol: np.ndarray,
    fa_vol: np.ndarray | None,
    min_fa: float,
    flip_ap: bool,
    flip_lr: bool,
    pad_frac: float = 0.06,
) -> tuple[int, int, int, int]:
    """Crop box from central slice(s); same box for all axial PNGs."""
    n = rgb_vol.shape[2]
    ref_ks = sorted({max(0, min(n - 1, k)) for k in (n // 2 - 1, n // 2, n // 2 + 1)})
    boxes: list[tuple[int, int, int, int]] = []
    for k in ref_ks:
        sl = to_radiological_axial(rgb_vol[:, :, k, :].copy(), flip_ap, flip_lr)
        if fa_vol is not None and min_fa > 0:
            fa_sl = to_radiological_axial(
                np.stack([fa_vol[:, :, k]] * 3, axis=-1), flip_ap, flip_lr
            )[:, :, 0]
            mask = fa_sl >= min_fa
        else:
            sl_u8 = to_uint8_rgb(sl)
            mask = np.max(sl_u8, axis=-1) > max(8, 0.04 * sl_u8.max())
        box = _bbox_from_mask(mask, pad_frac)
        if box:
            boxes.append(box)
    if not boxes:
        h, w = rgb_vol.shape[0], rgb_vol.shape[1]
        return 0, h - 1, 0, w - 1
    y0 = min(b[0] for b in boxes)
    y1 = max(b[1] for b in boxes)
    x0 = min(b[2] for b in boxes)
    x1 = max(b[3] for b in boxes)
    return y0, y1, x0, x1


def apply_fixed_crop(rgb: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    y0, y1, x0, x1 = box
    h, w = rgb.shape[:2]
    y0, y1 = max(0, y0), min(h - 1, y1)
    x0, x1 = max(0, x0), min(w - 1, x1)
    return rgb[y0 : y1 + 1, x0 : x1 + 1, :]


def apply_min_fa_mask(rgb: np.ndarray, fa: np.ndarray, min_fa: float) -> np.ndarray:
    """Zero color where FA < min_fa (AW default 0.18); linear scale only, no gamma."""
    x = rgb.astype(np.float32)
    if x.max() > 1.5:
        x = x / 255.0
    x[fa < min_fa] = 0
    return x


def to_uint8_rgb(rgb: np.ndarray) -> np.ndarray:
    """Linear 0–255 from Dipy color_fa (previous offline_axial_png style)."""
    x = rgb.astype(np.float32)
    if x.max() > 1.5:
        return np.clip(x, 0, 255).astype(np.uint8)
    return (np.clip(x, 0, 1) * 255).astype(np.uint8)


def fit_to_canvas(rgb: np.ndarray, size: int = CANVAS) -> np.ndarray:
    h, w = rgb.shape[:2]
    scale = (size * (1 - 2 * MARGIN_PCT)) / max(h, w)
    nh, nw = max(1, int(h * scale)), max(1, int(w * scale))
    img = Image.fromarray(rgb, mode="RGB").resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), (0, 0, 0))
    ox, oy = (size - nw) // 2, (size - nh) // 2
    canvas.paste(img, (ox, oy))
    return np.array(canvas)


def get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for fp in (
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(fp).is_file():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def draw_minimal_overlay(
    img: Image.Image,
    meta: dict,
    slice_idx: int,
    n_slices: int,
) -> None:
    """Patient info only (no GE-style clutter)."""
    draw = ImageDraw.Draw(img)
    yellow = (255, 255, 0)
    f_sm, f_md = get_font(13), get_font(15)
    draw.text((8, 8), meta["name"], fill=yellow, font=f_md)
    draw.text((8, 28), meta["exam"], fill=yellow, font=f_sm)
    draw.text((8, 46), "Im: %d / %d" % (slice_idx + 1, n_slices), fill=yellow, font=f_sm)


def render_clinical_rgb_slice(
    rgb_vol: np.ndarray,
    fa_vol: np.ndarray | None,
    k: int,
    crop_box: tuple[int, int, int, int],
    min_fa: float,
    flip_ap: bool,
    flip_lr: bool,
    canvas_size: int = 256,
) -> np.ndarray:
    """Same orient/mask/crop as PNG; scale to square canvas (default 256, not 509)."""
    sl = rgb_vol[:, :, k, :].copy()
    sl = to_radiological_axial(sl, flip_ap=flip_ap, flip_lr=flip_lr)
    if fa_vol is not None and min_fa > 0:
        fa_sl = to_radiological_axial(
            np.stack([fa_vol[:, :, k]] * 3, axis=-1), flip_ap=flip_ap, flip_lr=flip_lr
        )[:, :, 0]
        sl = apply_min_fa_mask(sl, fa_sl, min_fa)
    sl = to_uint8_rgb(sl)
    sl = apply_fixed_crop(sl, crop_box)
    return fit_to_canvas(sl, size=canvas_size)


def draw_aw_overlay(
    img: Image.Image,
    meta: dict,
    slice_idx: int,
    n_slices: int,
    slice_loc_mm: float | None = None,
) -> None:
    draw = ImageDraw.Draw(img)
    yellow = (255, 255, 0)
    f_sm, f_md, f_lg = get_font(14), get_font(16), get_font(20)
    im_no = slice_idx + 1
    loc = slice_loc_mm if slice_loc_mm is not None else im_no
    lines_left = [
        ("Axial Colored orientation  A %.0f" % loc, f_md),
        ("S: %.1f" % meta["series"], f_sm),
        ("Im: %d" % im_no, f_sm),
        ("DFOV 24.0 cm", f_sm),
    ]
    y = 8
    for text, font in lines_left:
        draw.text((12, y), text, fill=yellow, font=font)
        y += 18 if font == f_sm else 22
    draw.text((CANVAS - 200, 10), meta["name"], fill=yellow, font=f_md)
    draw.text((CANVAS - 200, 32), meta["exam"], fill=yellow, font=f_sm)
    sp, th = meta["spacing"], meta["thick"]
    lines_bot = [
        "SE/EPI",
        "%.1f/%.1fmm /%.1fsp" % (th, sp, sp),
        "m=-1 M=511",
        "W=512.0 L=255.0",
    ]
    y = CANVAS - 78
    for line in lines_bot:
        draw.text((12, y), line, fill=yellow, font=f_sm)
        y += 16
    draw.text((CANVAS // 2 - 8, 6), "A", fill=yellow, font=f_lg)
    draw.text((CANVAS // 2 - 8, CANVAS - 28), "P", fill=yellow, font=f_lg)
    draw.text((8, CANVAS // 2 - 8), "R", fill=yellow, font=f_lg)
    draw.text((CANVAS - 22, CANVAS // 2 - 8), "L", fill=yellow, font=f_lg)


def export_stack(
    rgb_vol: np.ndarray,
    out_dir: Path,
    meta: dict,
    z_positions_mm: np.ndarray | None = None,
    fa_vol: np.ndarray | None = None,
    min_fa: float = DEFAULT_MIN_FA,
    flip_ap: bool = False,
    flip_lr: bool = False,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    n = rgb_vol.shape[2]
    crop_box = compute_fixed_crop_box(
        rgb_vol, fa_vol, min_fa, flip_ap, flip_lr
    )
    for k in range(n):
        sl = rgb_vol[:, :, k, :].copy()
        sl = to_radiological_axial(sl, flip_ap=flip_ap, flip_lr=flip_lr)
        if fa_vol is not None and min_fa > 0:
            fa_sl = to_radiological_axial(
                np.stack([fa_vol[:, :, k]] * 3, axis=-1), flip_ap=flip_ap, flip_lr=flip_lr
            )[:, :, 0]
            sl = apply_min_fa_mask(sl, fa_sl, min_fa)
        sl = to_uint8_rgb(sl)
        sl = apply_fixed_crop(sl, crop_box)
        sl = fit_to_canvas(sl)
        img = Image.fromarray(sl, mode="RGB")
        loc = float(z_positions_mm[k]) if z_positions_mm is not None else None
        draw_aw_overlay(img, meta, k, n, loc)
        img.save(out_dir / ("slice_%02d.png" % k))
    print("Wrote %d styled PNGs -> %s" % (n, out_dir))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rgb_nii", type=Path, default=Path("jiang_offline_output/jiang_offline_colorFA_rgb.nii.gz"))
    ap.add_argument("--fa_nii", type=Path, default=Path("jiang_offline_output/jiang_offline_fa.nii.gz"), help="FA map for Min-FA mask")
    ap.add_argument("--min-fa", type=float, default=DEFAULT_MIN_FA, help="FA threshold (0=off)")
    ap.add_argument("--dicom_dir", type=Path, default=Path("DICOM/PA0/ST0/SE6"))
    ap.add_argument("--out_dir", type=Path, default=Path("jiang_offline_output/offline_axial_png"))
    ap.add_argument("--flip-ap", action="store_true", help="flip A<->P after base orient (if still inverted)")
    ap.add_argument("--flip-lr", action="store_true", help="flip R<->L after base orient")
    args = ap.parse_args()

    rgb = nib.load(str(args.rgb_nii)).get_fdata()
    fa = None
    if args.fa_nii and Path(args.fa_nii).is_file():
        fa = nib.load(str(args.fa_nii)).get_fdata()
    meta = load_patient_meta(args.dicom_dir)
    z_mm = None
    try:
        img = nib.load(str(args.rgb_nii))
        aff = img.affine
        n = rgb.shape[2]
        z_mm = np.array([aff[2, 2] * k + aff[2, 3] for k in range(n)])
    except Exception:
        pass
    export_stack(
        rgb,
        args.out_dir,
        meta,
        z_mm,
        fa_vol=fa,
        min_fa=args.min_fa,
        flip_ap=args.flip_ap,
        flip_lr=args.flip_lr,
    )


if __name__ == "__main__":
    main()
