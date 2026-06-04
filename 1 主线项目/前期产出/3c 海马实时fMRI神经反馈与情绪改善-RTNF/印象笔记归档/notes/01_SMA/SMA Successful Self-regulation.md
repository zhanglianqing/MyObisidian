---
title: "SMA: Successful Self-regulation"
source: evernote_html
source_html: "SMA Successful Self-regulation.html"
category: "01_SMA"
imported: 2026-05-23
---

# SMA: Successful Self-regulation

参考 [[Paper 阅读：Manipulating motor performance and m|Paper 阅读：Manipulating motor performance and memory through real-time fMRI neurofeedback -]]

文中，定义successful self-regulation的方式：

After each run, self-regulation performance was quantified in SPM99 using a GLM consisting of 2 regressors indicating up- and down-regulation. Motion parameters (translation, rotation) were included as covariates to reduce the impact of residual motion artifacts. This GLM was not applied to the whole brain but only to the high-pass filtered (5.55 × 10−3 Hz) differential feedback signal. Both regressors were contrasted to determine signal differences between up- and down-regulation and the corresponding t-values were calculated. This analysis was carried out only to determine the further course of the experiment, and was not presented to the participants. Also, for the offline analysis, different statistical procedures were used. The neurofeedback training procedure was repeated until participants achieved a pre-defined criterion of successful self-regulation, i.e. when a t-value higher than 3.1 (which is equivalent to p < 0.001) was reached. Across participants, the training objectives were reached within 12–22 runs spread over the course of 4–6 days.

  1. feedback signal 做 high-pass filtered (5.55 × 10−3 Hz)

  2. 建立GLM: high-pass filtered signal ~ block design + HMP

  3. t-value > 3.1 ( p < 0.001) 为成功




  


复现上述操作代码位置：

"H:\RTNF\test2-bids\realtime-data\SMA\SuccessfulRegulation.py"

结果在同文件夹内。

  
| 总人数| 到达阈值| 未到达阈值  
---|---|---|---  
无经验组| 6| 1| 5  
有经验组| 10| 5| 5  
  
乍一看这个达标率两组差异还是挺高的，

少了两个？

Subject| SMAgroup| subject_dir| Name| Age| Gender| Edu_yrs| t_value| p_value| 是否到达阈值  
---|---|---|---|---|---|---|---|---|---  
sub-RTNF002| 1| xia_liying_20240518| 夏莉颖| 21| 女| 15| -6.872912827| 0|   
  
sub-RTNF005| 1| XuYijing_20240525| 许怡谨| 22| 男| 16| 6.377876827| 0| 达到阈值  
sub-RTNF006| 1| BaoRong_20240525| 包蓉| 22| 女| 16| 3.470928809| 0.0006| 达到阈值  
sub-RTNF007| 1| LiXintong_20240601| 李欣橦| 24| 女| 17| 0.179936349| 0.8573|   
  
sub-RTNF008| 1| DaiYingying_20240601| 代盈盈| 23| 女| 17| 9.805538928| 0| 达到阈值  
sub-RTNF009| 1| Zeng_yan_20240608| 曾妍| 21| 女| 18| -5.237987093| 0|   
  
sub-RTNF010| 1| Lu_xuan_20240608| 陆萱| 22| 女| 16| 6.284958318| 0| 达到阈值  
sub-RTNF011| 1| ZhangZiwei_20240615| 张子为| 21| 男| 16| 3.358143374| 0.0008| 达到阈值  
sub-RTNF012| 1| BaiHexiang_20240615| 白鹤翔| 22| 男| 17| 0.883834129| 0.3772|   
  
sub-RTNF014| 1| ZhangChen_20240622| 张晨| 21| 女| 16| -5.676842622| 0|   
  
sub-RTNF015| 2| XieChengyang_20240629| 谢承洋| 20| 男| 18| -1.269018107| 0.2051|   
  
sub-RTNF016| 2| LiYihua_20240629| 李宜华| 20| 女| 15| 1.222654887| 0.2221|   
  
sub-RTNF017| 2| ChenLiang_20240706| 陈亮| 23| 男| 17| -0.490856676| 0.6238|   
  
sub-RTNF018| 2| WangYuting_20240706| 王雨婷| 22| 女| 16| 2.509173432| 0.0124|   
  
sub-RTNF019| 2| WangYutong_20240713| 王禹童| 21| 男| 16| 11.21174181| 0| 达到阈值  
sub-RTNF020| 2| LiuYukun_20240713| 刘玉锟| 20| 女| 15| 2.95447901| 0.0033|
