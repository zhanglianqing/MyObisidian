---
title: "first-level"
source: evernote_html
source_html: "first-level.html"
category: "01_SMA"
imported: 2026-05-23
---

# first-level

参考教程： [5-SPM-fmri任务态数据 一阶分析(单个被试） - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/662273422)

2024/8/6 19:44 正在进行批处理

  1. 已用python写完fmriprep到spm的准备，主要包括：选取需要的nii，保存，解压缩，选取需要的头动参数。位置：H:\RTNF\test2-bids\fmriprep\post_fmriprep.py

  2. 已完成批处理脚本。参考教程： [6-SPM-fmri任务态 一阶分析（单个被试的批处理） - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/663299409) 及 [SPM批量处理_matlab function matlabbatch = preproc(id)-CSDN博客](https://blog.csdn.net/2301_80326602/article/details/134464870)

  3. 大致步骤：

     1. 根据上述  [6-SPM-fmri任务态 一阶分析（单个被试的批处理） - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/663299409) 通过Batch设置完单个被试的流程化处理后，保存，选择同时保存batch和script

     2. 保存之后会出现 xx_job.m及 xx.m文件，用法如下：

        1. job文件直接使用：图形界面点batch，然后load这个文件，按绿色三角开始跑

        2. 修改script：首先把 job文件内的代码复制到 xx.m里面，替换所有输入字符为变量。然后运行。已修改完成的代码位置：H:\RTNF\test2-bids\fmriprep\spm_first_level\run_first_level.m




  


  


文件位置：H:\RTNF\test2-bids\fmriprep\spm_first_level

  1. ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/en_todo.png]]slice timing 这一步在实际的预处理中受到实验设计和扫描层数的影响，block设计可以不做这一步，event则必须做

     1. fmriprep：Slice timing correction: Applied已经做过这一步了

  2. ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/].png]]Realign，Coregister & Normalise：fmriprep都做了

  3. ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/].png]]Susceptibility distortion correction: None 这个需要解决一下,后面整理pipeline的时候重新做这个 #已处理，fmriprep已经做了

  4. ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/].png]]skull strip这一步也没做，需要做吗？ #想起来应该是最后二阶分析的时候做

  5. ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/].png]]没有做smooth，需要做

     1. 把nii.gz数据解压成nii（spm读不了nii.gz），放到spm_first_level文件夹下。

     2. ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/].png]]平滑核选多少，,后面整理pipeline的时候重新做这个

        1. 空间平滑（Smooth）：原理： Smooth可以降低仿射变换的影响，并提高统计效力（平滑核大小一般建议为体素大小的2倍） 一般推荐6 6 6的平滑和，范围在4-10之间（也可以参考前人的文献的具体数据）

        2. 本数据的体素大小：2.5x2.5x2.5 mm ，用5 5 5。按照一般推荐 [6 6 6]也可以接受

     3. ![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/Image.png]]

     4. output：ssub-RTNF001_ses-d1_task-SMA_acq-mb5_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii

  6. 几个设置都保存了，之后把整个workflow整理成脚本即可

  7.   


  8.   





  


几个问题：

![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/].png]]

![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/first-level_files/].png]]
