---
title: "Installation via PyCharm — OpenNFT 1.0.0 documentation"
source: evernote_html
source_html: "Installation via PyCharm — OpenNFT 1.0.0 docu.html"
category: "06_方案与基建"
imported: 2026-05-23
---

# Installation via PyCharm — OpenNFT 1.0.0 documentation

[Installation via PyCharm — OpenNFT 1.0.0 documentation](https://opennft.readthedocs.io/en/latest/install_pycharm.html)

OpenNFT 安装测试笔记

![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Installation via PyCharm — OpenNFT 1.0.0 docu_files/en_todo.png]]安装：

  1. 安装matlab2017b及相关toolbox

     1. spm12 #联影修改版spm，可读取联影dicom # addpath

     2. Psychophysics Toolbox Version 3 (PTB-3) 链接：<http://psychtoolbox.org/download>

        1. Download the [Psychtoolbox installer](https://raw.github.com/Psychtoolbox-3/Psychtoolbox-3/master/Psychtoolbox/DownloadPsychtoolbox.m.zip) to your desktop. 直接下载zip包：<https://github.com/Psychtoolbox-3/Psychtoolbox-3>

        2. 下载并安装 the [64-Bit GStreamer-1.18.5](https://gstreamer.freedesktop.org/data/pkg/windows/1.18.5/msvc/gstreamer-1.0-msvc-x86_64-1.18.5.msi)[ ](https://gstreamer.freedesktop.org/data/pkg/windows/1.18.5/msvc/gstreamer-1.0-msvc-x86_64-1.18.5.msi)[MSVC](https://gstreamer.freedesktop.org/data/pkg/windows/1.18.5/msvc/gstreamer-1.0-msvc-x86_64-1.18.5.msi) runtime 

        3. [install the Microsoft Runtime Libraries for MSVC 2015-2019 ](https://github.com/Psychtoolbox-3/Psychtoolbox-3/raw/master/Psychtoolbox/PsychContributed/vcredist_x64_2015-2019.exe)

        4. cd('C:\Users\chenxuanli\Downloads\OpenNFT\PTB3\Psychtoolbox-3-3.0.18.9\Psychtoolbox')

SetupPsychtoolbox

     3. jsonlab  [link](https://github.com/fangq/jsonlab) #addpath

        1. 2022/10/12 注意版本问题：需要用稍旧一点的版本，下载最新版后发现新版的修改了json文件读取后存储的形式，导致openNFT代码出了点问题

addpath('C:\Users\<login>\Documents\MATLAB\spm12')

  2. 用pycharm 安装

     1. fork repo: <https://github.com/zhanglianqing/OpenNFT>

     2. 通过 pycharm 安装： [https://opennft.read、thedocs.io/en/latest/install_pycharm.html](https://opennft.readthedocs.io/en/latest/install_pycharm.html)

     3. python版本问题：安装的matlab是2017b，对应的 matlabengineforpython 只支持到python3.6，于是python=3.6

  3. 显示feedback 会报依赖库问题：基本上是PTB安装没到位。PTB要严格按照上面的要求安装




  


![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Installation via PyCharm — OpenNFT 1.0.0 docu_files/].png]]下载openNFT Demo data 并运行：

  1. Memory相关问题：比较吃内存，首先pycharm设置最大memory limit设高一点。如果其他东西开得比较多就重启后直接开openNFT，或者硬件加内存




![[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Installation via PyCharm — OpenNFT 1.0.0 docu_files/].png]]试跑UI sample data：

  1. ROI问题：目前测试用，只是随便画了一个ROI

     1. 不能在结构像上画ROI，会有比较大的distortion。或者reference直接用T1？

     2. 后续需要考虑：如果手画ROI，需要在扫描时非常迅速的勾上。要把itk-snap手画ROI迅速打通。如果直接套模板，则要work out快速自动分析代码

     3. 目前常用的画ROI的方法？

  2. 计算时间问题：由于UI给的matrix是140*140，而NFT sample是70*70，所以这个processing time高达1.9s。明天把数据给潘洋在外星人上测试一下，看CPU性能上去之后能不能好一些。如果这个不能解决，就只能降matrix

  3. 需要清理一下workflow。开始扫描后做什么、怎么做，哪些内容能写成代码完成？

     1. 扫描3D-T1完成后，格式转换 dcm2niix

     2. 扫描rest完成后，取第一个volume作为reference （或者单独扫一个reference），进行格式转换

     3. ROI确定？

     4. 看要不要写一个自动生成init文件的东西，主要是读取matrix和TR
