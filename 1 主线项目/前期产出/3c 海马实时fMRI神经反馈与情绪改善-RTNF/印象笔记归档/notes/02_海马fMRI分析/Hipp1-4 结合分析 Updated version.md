---
title: "Hipp1-4 结合分析 Updated version"
source: evernote_html
source_html: "Hipp1-4 结合分析 Updated version.html"
category: "02_海马fMRI分析"
imported: 2026-05-23
---

# Hipp1-4 结合分析 Updated version

1. 每个被试first-level 重做，把4个run都输入。重跑的first run：first_level_base_dir = 'J:\RTNF\test2-bids\fmriprep\spm_first_level\Hipp1-4';

  2. contrast设置：

     1. matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = 'UpRegulate'; matlabbatch{3}.spm.stats.con.consess{1}.tcon.weights = [0 1 0]; matlabbatch{3}.spm.stats.con.consess{1}.tcon.sessrep = 'none'; matlabbatch{3}.spm.stats.con.consess{2}.tcon.name = 'UpRegulate2rest'; matlabbatch{3}.spm.stats.con.consess{2}.tcon.weights = [-1 1 0]; matlabbatch{3}.spm.stats.con.consess{2}.tcon.sessrep = 'none'; matlabbatch{3}.spm.stats.con.consess{3}.tcon.name = 'UpRegulate2count'; matlabbatch{3}.spm.stats.con.consess{3}.tcon.weights = [0 1 -1]; matlabbatch{3}.spm.stats.con.consess{3}.tcon.sessrep = 'none'; matlabbatch{3}.spm.stats.con.consess{4}.tcon.name = 'UpRegulate2All'; matlabbatch{3}.spm.stats.con.consess{4}.tcon.weights = [-0.5 1 -0.5]; matlabbatch{3}.spm.stats.con.consess{4}.tcon.sessrep = 'none'; matlabbatch{3}.spm.stats.con.consess{5}.tcon.name = 'Count'; matlabbatch{3}.spm.stats.con.consess{5}.tcon.weights = [0 0 1]; matlabbatch{3}.spm.stats.con.consess{5}.tcon.sessrep = 'none'; matlabbatch{3}.spm.stats.con.consess{6}.tcon.name = 'Rest'; matlabbatch{3}.spm.stats.con.consess{6}.tcon.weights = [1 0 0]; matlabbatch{3}.spm.stats.con.consess{6}.tcon.sessrep = 'none'; matlabbatch{3}.spm.stats.con.consess{7}.tcon.name = 'Count2Rest'; matlabbatch{3}.spm.stats.con.consess{7}.tcon.weights = [-1 0 1]; matlabbatch{3}.spm.stats.con.consess{7}.tcon.sessrep = 'none';

  3. Second level

     1. UpRegulate2rest,

     2. 结果：

        1.   





  


UpReg vs Rest| FWE，cluster > 130|   
  
---|---|---  
contrast_filename = 'con_0002.nii'; output_dir = 'J:\RTNF\test2-bids\fmriprep\spm_2nd_level\UpRegulate2Rest\Hipp1-4\SecondLevel_OneSampleT_UpRegulate2Rest';| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Hipp1-4 结合分析 Updated version_files/Image.png]]  
  
  
  
  
Neg![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Hipp1-4 结合分析 Updated version_files/].png]]| 小脑6，SMA，insular（双侧）2个白质，不要precentral  
  
heschl 初级听觉，insularprecunous视觉-双侧枕下回内侧额叶-额上回 - DMN（内侧前额叶+PCC）  
UpReg vs Count| FWE cluster>100|   
  
contrast_filename = 'con_0003.nii'; output_dir = 'J:\RTNF\test2-bids\fmriprep\spm_2nd_level\UpRegulate2Count\Hipp1-4\SecondLevel_OneSampleT_UpRegulate2Count';| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Hipp1-4 结合分析 Updated version_files/].png]]VAN为主，==salienceDLPFC小脑  
  
  
  
  
![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Hipp1-4 结合分析 Updated version_files/].png]]IPL(DAN)|   
  
Count2Rest|   
|   
  
% --- Basic Setup ---% Directory where the first-level results (for each subject) are storedfirst_level_base_dir = 'J:\RTNF\test2-bids\fmriprep\spm_first_level\Hipp1-4'; % Name of the contrast file from the first-level analysis.% In your previous script, 'UpRegulate2count' was the 3rd contrast.contrast_filename = 'con_0007.nii'; % Directory where the results of THIS second-level analysis will be savedoutput_dir = 'J:\RTNF\test2-bids\fmriprep\spm_2nd_level\Count2Rest\Hipp1-4\SecondLevel_OneSampleT_Count2Rest';  
| ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Hipp1-4 结合分析 Updated version_files/].png]]SMA, Precentral（--> SMN），IPL（顶下小叶）  
  
  
![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Hipp1-4 结合分析 Updated version_files/].png]]  
DMN + 枕叶+insular+caudate/acc小脑IFG|
