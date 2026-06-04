# GE DTI 离线 Color FA 脚本

来源：`C:\Users\41516\Desktop\SampleData-GE-DTI`（2026-05-22 与定稿交付同步）

## 运行

在项目根目录（含 `DICOM/.../SE*` DTI 序列）执行：

```powershell
python scripts/run_offline_colorfa.py
```

修改 `run_offline_colorfa.py` 中 `DTI_DIR`、`OUT_DIR` 以适配新数据。

## 依赖

```powershell
pip install dcm2niix dipy nibabel pydicom pillow
```

## 说明

- 不随仓库附带 DICOM / NIfTI；仅 Python 源码。
- 主文档：上级目录 `GE-DTI-离线ColorFA与AW对比剂标签.md`
