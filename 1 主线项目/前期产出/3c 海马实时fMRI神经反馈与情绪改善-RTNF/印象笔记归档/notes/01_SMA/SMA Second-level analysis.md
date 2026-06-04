---
title: "SMA: Second-level analysis"
source: evernote_html
source_html: "SMA Second-level analysis.html"
category: "01_SMA"
imported: 2026-05-23
---

# SMA: Second-level analysis

2024/8/9 11:44

本周已完成first-level analysis，正在尝试 Second-level

  


目前尝试包括：

  


One Sample T (无协变量）  
---  
contrast: 0 1 （正激活）  
Sample|   
| FWE-level  
全部被试（n=18）| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/Image.png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]| 无显著:![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]  
  
| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]  
cluster size > 100![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]|   
  
contrast: 0 -1 （负激活）  
全部被试（n=18）| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]| contra![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]  
  
  
st: 0 1 （正激活）  
  
  
  
|   
| 双侧 Temporal_Pole_Sup extend to middle temporal， PCC DMN网络 （包括Middle Temporal Gyrus）  
  
H:\RTNF\test2-bids\fmriprep\spm_2nd_level\SMA\contrast-neg\one-sample\spmT_0001.nii,1Type: Tdf: 17Threshold\-- p value = 1.0744e-06\-- intensity = 6.9974\-- cluster size = 5Number of clusters found: 3\----------------------Cluster 1Number of voxels: 36Peak MNI coordinate: -49 7.5 -18.5Peak MNI coordinate region: // Left Cerebrum // Temporal Lobe // Middle Temporal Gyrus // Gray Matter // brodmann area 21 // Temporal_Pole_Sup_L (aal)Peak intensity: 9.0865# voxels structure 36 --TOTAL # VOXELS-- 36 Left Cerebrum 36 Temporal Lobe 24 Middle Temporal Gyrus 19 Temporal_Pole_Sup_L (aal) 18 Gray Matter 13 White Matter 12 brodmann area 21 12 Superior Temporal Gyrus 11 Temporal_Sup_L (aal) 6 Temporal_Mid_L (aal) 4 brodmann area 38 2 brodmann area 22\----------------------Cluster 2Number of voxels: 46Peak MNI coordinate: 46 -2.5 -11Peak MNI coordinate region: // Right Cerebrum // Temporal Lobe // Superior Temporal Gyrus // White Matter // undefined // Temporal_Sup_R (aal)Peak intensity: 10.061# voxels structure 46 --TOTAL # VOXELS-- 46 Right Cerebrum 46 Temporal Lobe 39 White Matter 24 Temporal_Mid_R (aal) 23 Middle Temporal Gyrus 20 Temporal_Sup_R (aal) 17 Sub-Gyral 6 Superior Temporal Gyrus 6 Gray Matter 5 brodmann area 21 1 brodmann area 38\----------------------Cluster 3Number of voxels: 63Peak MNI coordinate: 11 -45 31.5Peak MNI coordinate region: // Right Cerebrum // Limbic Lobe // Cingulate Gyrus // Gray Matter // brodmann area 31 // Cingulum_Mid_R (aal)Peak intensity: 8.0034# voxels structure 63 --TOTAL # VOXELS-- 63 Right Cerebrum 49 Parietal Lobe 48 Precuneus 35 Gray Matter 32 Precuneus_R (aal) 26 Cingulum_Mid_R (aal) 24 brodmann area 31 23 White Matter 15 Cingulate Gyrus 14 Limbic Lobe 11 brodmann area 7 5 Cingulum_Post_R (aal)  
主要结果：当把所有被试放在一起分析时，NF期无显著正激活，但双侧Middle temporal gyrus、Precuneus 显著抑制The precuneus is a highly developed region in the medial parietal cortex that is involved in controlling voluntary attention shifts, episodic memory retrieval, personal identity, and past experiences. It is associated with the highest resting perfusion rate in the cerebral cortex and plays a role in spatially guided behavior and imagining one's own actions.  #但是为什么是负激活？  
  
  


Two Sample T (协变量：性别、年龄）  
---  
contrast: 0 1 （正激活）  
Sample| 校正前| FWE-level  
有训练被试（g1，n=11） > 无训练被试（g2，n=7)| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]| contrast: ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]0 1 （正contrast: 0 1 （正激活）激活）  
有训练被试（g1，n=11） < 无训练被试（g2，n=7)| 无| 无显著  
contrast: 0 -1 （负激活）  
有训练被试（g1，n=11） > 无训练被试（g2，n=7)| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]|   
  
有训练被试（g1，n=11） < 无训练被试（g2，n=7)| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/SMA Second-level analysis_files/].png]]  
  
pos 和 neg是一样的？
