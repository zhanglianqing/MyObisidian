---
title: "Real-Time fMRI Pattern Decoding and Neurofeedback Using FRIEND: An FSL-Integrated BCI Toolbox"
source: evernote_html
source_html: "Real-Time fMRI Pattern Decoding and Neurofeed.html"
category: "05_文献阅读"
imported: 2026-05-23
---

# Real-Time fMRI Pattern Decoding and Neurofeedback Using FRIEND: An FSL-Integrated BCI Toolbox

## Materials and Methods

### Ethics statement

All participants provided written consent for participating in these studies. This study and all data herein presented was approved by the local ethics committees (Copa D’Or CEP#137/09 and UFRJ CEP#159.709).

### FRIEND Toolbox Overview

FRIEND was developed at the Cognitive and Behavioral Neuroscience Unit, D’Or Institute for Research and Education (<http://idor.org/neuroinformatics/friend>[](http://idor.org/neuroinformatics/friend)), Rio de Janeiro, Brazil. The package was coded in Object PASCAL (Delphi® 2007 and Lazarus 1.0.10) and C2+ (Microsoft Visual Studio® 2008 Professional and GNU Compiler Collection 4.8.1). FRIEND is multiplatform, running on Microsoft Windows® (XP or later), Apple Macintosh (OS X 10.8 and above) and Linux (Debian, CentOS 6.4). A mid/high end workstation is required (e.g. PC: Quad-core i7, 8 GB RAM or above, Macintosh: Quad-core Intel Core i5, 8 GB RAM or above) in order to enable smooth online data preprocessing, classification and contingent stimulus delivery. FRIEND employs multithread coding for speeded up processing in multiple core workstations. This feature is implemented by calling embedded FSL routines ([http://www.fmrib.ox.ac.uk/fsl/](http://www.fmrib.ox.ac.uk/fsl/)) into different threads. The original FSL codes were not modified for parallel processing. All steps of image registration, motion correction, feature selection (based on either SVM or general linear model [GLM] “functional localizers”, or on _a priori_ ROIs) and SVM classification can generally be performed within a TR of 1.5 seconds or less (single-shot EPI, 64x64 to 80x80 matrix, 22-37 slices.

The real-time preprocessing module includes options for univariate (ROI-based) and multivariate SVM data analysis [[24](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B24),[25](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B25)] and/or classification, coupled with the visual neurofeedback module. This enables participants to use their own local (single ROI or combined ROIs) or distributed brain signals (correlation among ROIs or multivoxel pattern-based brain decoding using SVM) to modulate performance in a wide range of behavioral (e.g., motor task), cognitive (e.g., motor imagery) or emotional tasks (e.g., basic, social or moral emotions). [Figure 1](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g001) shows a flowchart describing FRIEND’s main pipeline elements.

![[journal.pone.0081658.g001]]

[[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Real-Time fMRI Pattern Decoding and Neurofeed_files/journal.pone.0081658.g001 "Click for larger image"|journal.pone.0081658.g001 "Click for larger image"]]

Download: 

  * [PPTPowerPoint slide](https://journals.plos.org/plosone/article/figure/powerpoint?id=info:doi/10.1371/journal.pone.0081658.g001)
  * [PNGlarger image](https://journals.plos.org/plosone/article/figure/image?download&size=large&id=info:doi/10.1371/journal.pone.0081658.g001)
  * [TIFForiginal image](https://journals.plos.org/plosone/article/figure/image?download&size=original&id=info:doi/10.1371/journal.pone.0081658.g001)



Figure 1.  Flowchart of three FRIEND processing pipelines for neurofeedback.

(1) BOLD level real-time display from pre-defined ROIs; (2) Real-time functional connectivity neurofeedback based on the correlation between the signals from different ROIs; (3) Support Vector Machine based neurofeedback, defined on the basis of projected values onto the discriminative hyperplane.

[ https://doi.org/10.1371/journal.pone.0081658.g001](https://doi.org/10.1371/journal.pone.0081658.g001)

The FRIEND toolbox currently embeds components from the FSL ([[26](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B26)]; <http://www.fmrib.ox.ac.uk/fsl/>[](http://www.fmrib.ox.ac.uk/fsl/)) and from the libSVM ([[27](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B27)]; <http://www.csie.ntu.edu.tw/~cjlin/libsvm/>[](http://www.csie.ntu.edu.tw/~cjlin/libsvm/)) libraries, both freely available packages with stable releases that have been extensively validated by the scientific community. FRIEND also incorporates a number of modules and routines designed specifically to simplify the conduction of real-time fMRI neurofeedback experiments, while allowing extensive control of parameters and quality control. Furthermore, to allow for controlled studies, FRIEND offers the option of running an experiment with contingent (“real”) or non-contingent (e.g., random or non-informative) neurofeedback. Thus, participants may be randomly assigned to a neurofeedback or to a control / non-feedback group.

### Data Acquisition and Processing Overview

Data collection begins with the acquisition of a high-resolution gradient-echo T1-weighted structural anatomical volume (reference anatomical image, RAI) and one high signal-to-noise echo-planar (EPI) volume (reference functional image, RFI), which are used as image registration references. Functional images are then obtained using the real-time acquisition pipeline. The experimental design is described in an ASCII design file while other parameters (preprocessing parameters, type of feature selection, if any, and feedback characteristics) are entered into the software interface window ([Figure 2](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g002)). 

![[journal.pone.0081658.g002]]

[[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Real-Time fMRI Pattern Decoding and Neurofeed_files/journal.pone.0081658.g002 "Click for larger image"|journal.pone.0081658.g002 "Click for larger image"]]

Download: 

  * [PPTPowerPoint slide](https://journals.plos.org/plosone/article/figure/powerpoint?id=info:doi/10.1371/journal.pone.0081658.g002)
  * [PNGlarger image](https://journals.plos.org/plosone/article/figure/image?download&size=large&id=info:doi/10.1371/journal.pone.0081658.g002)
  * [TIFForiginal image](https://journals.plos.org/plosone/article/figure/image?download&size=original&id=info:doi/10.1371/journal.pone.0081658.g002)



Figure 2.  Typical parameters for a study session in FRIEND (anatomical and functional volumes of reference, number of volumes, and statistical thresholds, among others).

Additional parameters (e.g., % of higher voxels for GLM feature selection, inclusion of motion parameter variables in the GLM model, FWHM values) can be modified by editing an input text file. 

[ https://doi.org/10.1371/journal.pone.0081658.g002](https://doi.org/10.1371/journal.pone.0081658.g002)

FRIEND's real-time functionalities inherently require proper access to the functional volumes as soon as they are acquired. Thus, real-time fMRI data (single EPI volumes) must be available from the MR scanner in a suitable data format immediately following reconstruction. It should be noted that FRIEND does not access the imaging data directly from the scanner. Instead, it reads the data from a shared folder where the reconstructed images are saved in real time. To the best of our knowledge, real-time data reconstruction and export (or online access to reconstructed images) is currently available from at least three of the main manufacturers (Philips Medical Systems, Siemens Medical Solutions and GE Medical Systems). Siemens has a built-in tool, which is standard starting from release VB15 [[20](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B20)]. Philips provides the DRIN-dumper as a clinical research tool, and real-time solutions for GE scanners are also available ([[28](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B28)]; see also [https://github.com/cni/rtfmri](https://github.com/cni/rtfmri)). In addition to the proprietary software mentioned above, there are also other options for real-time data handling (e.g., FieldTrip, [http://fieldtrip.fcdonders.nl](http://fieldtrip.fcdonders.nl/)). So far, FRIEND has been tested with Philips and Siemens scanners. 

In its current implementation, FRIEND requires at least one condition of no interest (i.e., baseline), which should be included between blocks of the main experimental conditions, in order to allow for online signal normalization and detrending. These steps are important to minimize the effects of MRI signal drifts (see [12](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B12)). 

The graphical user interface (GUI) control window includes online charts for functional image registration to the reference volume (including translation, rotation and root mean square error [RMS]). Accuracy estimates (correct classification of individual functional volumes when using SVM), normalized signal in selected ROIs (i.e., BOLD changes) and sliding window correlations among ROIs can be dynamically evaluated in the same control window during real-time fMRI ([Figure 3](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g003)).

![[journal.pone.0081658.g003]]

[[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Real-Time fMRI Pattern Decoding and Neurofeed_files/journal.pone.0081658.g003 "Click for larger image"|journal.pone.0081658.g003 "Click for larger image"]]

Download: 

  * [PPTPowerPoint slide](https://journals.plos.org/plosone/article/figure/powerpoint?id=info:doi/10.1371/journal.pone.0081658.g003)
  * [PNGlarger image](https://journals.plos.org/plosone/article/figure/image?download&size=large&id=info:doi/10.1371/journal.pone.0081658.g003)
  * [TIFForiginal image](https://journals.plos.org/plosone/article/figure/image?download&size=original&id=info:doi/10.1371/journal.pone.0081658.g003)



Figure 3.  FRIEND’s control window, including: the main menu (A), training and feedback buttons (B), current experimental condition (C), rotation in radians (D), translation in mm (E) and root mean square error from motion parameters (F).

User-defined neurofeedback stimuli to be presented to participants (a thermometer in this case) are displayed when the feedback option is selected (G). For single ROI processing, time-course, mean signal within specified ROIs, signal change and condition blocks will be shown (H). In the case of sliding-window ROI correlation analysis, a similar graph shows the level of correlation, sliding window size and upper and lower bounds of correlation targets (I). During the SVM classification sessions, the interface shows the classification phase, the current scan and the model-based cumulative classification accuracy (J). 

[ https://doi.org/10.1371/journal.pone.0081658.g003](https://doi.org/10.1371/journal.pone.0081658.g003)

### Real-time Image Preprocessing

The first step consists of an affine co-registration of RFI to RAI (12 degrees of freedom, using the FLIRT routine (<http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FLIRT>[](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FLIRT)). This transformation is subsequently used to adjust incoming EPI images during the functional runs both to the RFI (for pipeline processing) and RAI (for real-time activation map overlay) via the real-time motion correction routine based on FSL routines. Motion estimation and correction can be performed using the embedded MCFLIRT ([[29](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B29)]; <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/MCFLIRT>[](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/MCFLIRT)) library (-cost is set to normcorr and interpolation to trilinear sampling, which are the default options in MCFLIRT). Following image registration, spatial Gaussian smoothing of the EPI volumes based on a user-defined FWHM parameter can also be carried out. In order to minimize MRI signal trends, voxel intensities are mean-corrected by the average signal from the previous baseline condition, specified in a design matrix file.

### Functional Localizers and Feature Selection

When using ROI or SVM-based neurofeedback, users may opt for running General Linear Model (GLM)-based statistics [[30](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B30)] on the initial dataset (e.g., first functional run) to be used as a functional localizer for single-region neurofeedback, for dual-region correlation analysis or before SVM training. This step employs embedded routines from the FSL library (_feat_model_ and _fsl_glm, see_ <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT>[](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT)), allowing for _a priori_ -defined statistical contrasts, which can be used for optional feature selection/masking of relevant voxels identified by a functional localizer or training session (see [[31](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B31)]). It is important to note that because this is a feature selection step, the GLM is carried out off-line (not in real-time) after the first run (“training session”). This is an important step for the following reasons: (i) for single ROI neurofeedback or dual-ROI real-time correlation, using a percentage of the more active voxels within selected anatomical ROIs can better capture individual differences; (ii) whole brain classification analysis leads to high dimensionality of the data, including confounders and irrelevant variables, so a feature selection step (e.g., using a combination of _a priori_ ROIs, GLM and/or SVM-based thresholded maps) helps reducing dimensionality; and (iii) these procedures minimize the possibility that artifactual or uninformative voxels bias the results. 

### Support Vector Machines (SVM)

#### Training SVM Classifiers.

The rationale for the use of SVM is its intrinsic ability to deal with the typical fMRI datasets, which contain typically tens of thousands voxels, i.e., when the number of features far exceeds the number of measurements. Ultimately, the goal of machine learning methods applied to fMRI data is to maximize the ability to make predictions about new, unobserved data, i.e., to allow generalization from observed data (“training”) to new datasets [[32](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B32),[33](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B33)].

In FRIEND’s control window ([Figure 3](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g003)), when the “training” checkbox is selected, the SVM classifier will be initially trained with brain activation patterns associated with the specified conditions of interest in the training fMRI dataset. In addition, in order to increase the signal-to-noise ratio, each example is built by computing an average volume over three (or another user-defined number) previous volumes (sliding window average).

The main concept behind the two-class SVM methodology is to determine a mapping from input data (activation pattern) to output experimental condition in order to correctly classify it. Once this function is estimated, it can be used to obtain scores for predictions of the classes of new observations [[12](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B12)], based on their input data (see [Figure 4](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g004); [[34](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B34),[35](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B35)]). The input data is the normalized BOLD signal intensity of input voxels.

![[journal.pone.0081658.g004]]

[[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Real-Time fMRI Pattern Decoding and Neurofeed_files/journal.pone.0081658.g004 "Click for larger image"|journal.pone.0081658.g004 "Click for larger image"]]

Download: 

  * [PPTPowerPoint slide](https://journals.plos.org/plosone/article/figure/powerpoint?id=info:doi/10.1371/journal.pone.0081658.g004)
  * [PNGlarger image](https://journals.plos.org/plosone/article/figure/image?download&size=large&id=info:doi/10.1371/journal.pone.0081658.g004)
  * [TIFForiginal image](https://journals.plos.org/plosone/article/figure/image?download&size=original&id=info:doi/10.1371/journal.pone.0081658.g004)



Figure 4.  Illustration of how neurofeedback stimuli are defined based on the calculated projections on the SVM discriminant hyperplane.

The black and white circles are observations of two different types of stimuli (e.g., positive and negative emotional condition). The basic concept is that after training a two-class linear SVM, a discriminant hyperplane is defined (in light blue). Next, each new fMRI volume is projected on this hyperplane (decision function) and a score is attributed, reflecting the relative distance from the classification boundary (intersection with separating hyperplane). This score is then categorized in order to determine which visual image will be displayed to the participant as a feedback.

[ https://doi.org/10.1371/journal.pone.0081658.g004](https://doi.org/10.1371/journal.pone.0081658.g004)

The brain voxels of an fMRI image volume are first mapped onto an input vector _x_ , and this vector is then labeled according to the respective experimental condition when this scan was acquired [[19](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B19),[20](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B20)]. This initial data is used to train the classifier to discriminate between the experimental conditions of interest (currently, a two-class SVM classifier is implemented). The trained SVM is then used in the subsequent brain decoding sessions (testing sessions), in which participants engage in the same tasks and conditions of interest. 

#### Real-time Classification and Neurofeedback.

After training a SVM on the initial dataset, predictions about the current cognitive/neural state of the subject can be made in real-time based on incoming fMRI image volumes. At this stage, neurofeedback is delivered by presenting visual feedback stimuli that are contingent on SVM classification. Although the classification is based on categorical output data, linear SVM can provide the distance of a new observation to the separating hyperplane, the classification boundary between conditions [[35](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B35)]; this projection (“decision value”) is then used to define the neurofeedback display. The projection of a new image volume on the discriminating hyperplane is given by (_x_ _T_ _w_ +_b_), where _w_ is a vector containing the hyperplane coefficients and _b_ is a constant. In other words, the relative position of the input data projection to the classification boundary of the discriminative hyperplane is the measure that will define which figure (from a bitmap-grid stimulus set) will be displayed as a proxy of the underlying cognitive state of the participant. Further information about real-time classification/projection can be found in [[12](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B12),[19](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B19),[34](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B34),[35](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B35)]. 

In [Figure 5](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g005) (right panel), the shape of the ring changes progressively from a distorted to a perfect ring according to the two-class SVM classification (decision function values). In this example, the most distorted shape is associated with incorrect classification, and the progressively smoother rings are associated with increasing distance of the correctly classified example from the SVM decision boundary. Increasing distance from the SVM decision boundary indicates that the activation pattern is more distinctive of one category (cognitive state) as compared with the other. [Figure 6](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g006) depicts the display interface for real-time activation maps (image voxel intensity of current scan normalized by the previous _n_ -averaged baseline condition images, which can be scrolled in real-time).

![[journal.pone.0081658.g005]]

[[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Real-Time fMRI Pattern Decoding and Neurofeed_files/journal.pone.0081658.g005 "Click for larger image"|journal.pone.0081658.g005 "Click for larger image"]]

Download: 

  * [PPTPowerPoint slide](https://journals.plos.org/plosone/article/figure/powerpoint?id=info:doi/10.1371/journal.pone.0081658.g005)
  * [PNGlarger image](https://journals.plos.org/plosone/article/figure/image?download&size=large&id=info:doi/10.1371/journal.pone.0081658.g005)
  * [TIFForiginal image](https://journals.plos.org/plosone/article/figure/image?download&size=original&id=info:doi/10.1371/journal.pone.0081658.g005)



Figure 5.  Example of feedback figures displayed in motor imagery (left) and emotional (right) neurofeedback protocols.

FRIEND provides default neurofeedback figures (thermometer and rings), but user-defined ones may be used instead. The displayed words (GO/STOP and positive/negative) are cues for the specific task to be performed by participants.

[ https://doi.org/10.1371/journal.pone.0081658.g005](https://doi.org/10.1371/journal.pone.0081658.g005)

![[journal.pone.0081658.g006]]

[[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/印象笔记归档/attachments/Real-Time fMRI Pattern Decoding and Neurofeed_files/journal.pone.0081658.g006 "Click for larger image"|journal.pone.0081658.g006 "Click for larger image"]]

Download: 

  * [PPTPowerPoint slide](https://journals.plos.org/plosone/article/figure/powerpoint?id=info:doi/10.1371/journal.pone.0081658.g006)
  * [PNGlarger image](https://journals.plos.org/plosone/article/figure/image?download&size=large&id=info:doi/10.1371/journal.pone.0081658.g006)
  * [TIFForiginal image](https://journals.plos.org/plosone/article/figure/image?download&size=original&id=info:doi/10.1371/journal.pone.0081658.g006)



Figure 6.  Real-time brain activation mapping, depicting the ratio [(average BOLD signal of the ROI during the three last scans) – (average BOLD signal of the ROI during the previous baseline condition)] / (average BOLD signal of the ROI during the previous baseline condition) for each voxel on the participant’s native space using an arbitrary image threshold.

[ https://doi.org/10.1371/journal.pone.0081658.g006](https://doi.org/10.1371/journal.pone.0081658.g006)

### ROI-based Neurofeedback

In the case of model-driven experiments, FRIEND allows the use of ROIs not only for real-time visualization of online brain activity but also for ROI-based neurofeedback. The GUI allows selecting ROIs from standard atlases (MNI, AAL, etc), from a mask file or from the GLM results of a functional localizer scan, which can be saved as ROIs for subsequent use. A moving-average BOLD signal from these regions can then be displayed (e.g., as a thermometer or a moving ring). As demonstrated in previous studies, participants can modulate BOLD activity of specific ROIs, guided by neurofeedback signals [[11](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B11),[28](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B28),[36](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B36)]. The basic concept is to use a block-design paradigm in which participants are instructed to try to increase or decrease BOLD signal averaged within an ROI, with the aid of a feedback display (see [Video S1](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone.0081658.s001)). The feedback values are given by the ratio [(average BOLD signal of the ROI) – (average BOLD signal of the ROI during the previous baseline condition)] / (average BOLD signal of the ROI during the previous baseline condition) rescaled to the interval 0-100%.

[Figure 5](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g005) depicts two experimental designs using a thermometer and rings as feedback. Users may easily create and specify their own visual stimuli (JPEGs) to be employed as contingent feedback signals. In [Figure 5](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone-0081658-g005) (left panel), the thermometer level is specified by the change in ROI-based image intensity of the current EPI image, normalized by the signal average of the _n_ -preceding baseline volumes (_n_ being the number of volumes to be averaged in the preceding block of the user-defined baseline condition).

### ROI-based Functional Connectivity Neurofeedback

FRIEND also allows functional connectivity-based neurofeedback using a sliding window and Pearson correlation coefficients of the signal between two ROIs. In the current version, only two ROIs are employed, thus whole brain functional connectivity maps are not available in real-time (though this feature can be implemented by advanced users). This approach enables experiments probing the effects of endogenous modulation of the connectivity between user-defined ROIs (including cortico-subcortical connectivity that cannot be assessed using non-invasive EEG-based methods). At each new volume acquisition, the coefficient is iteratively calculated over the last _L_ scans (a user-defined parameter). To accomplish this, the mean intensity ro⎯⎯i=∑i=1:mxi/m is calculated over the _m_ voxels of the ROI, ro⎯⎯i at each time point _t_ for subsequent calculation of the ROI mean ro⎯⎯i=∑t=1:Lro⎯⎯it/L. Thus, for ROIs A and B, the Pearson correlation coefficient over a _L_ -sliding window at time _t_ is:

ρ(A,B)t=∑Lk=1(A⎯⎯⎯t−k−A⎯⎯⎯)(B⎯⎯⎯t−k−B⎯⎯⎯)∑Lk=1(A⎯⎯⎯t−k−A⎯⎯⎯)2√∑Lk=1(B⎯⎯⎯t−k−B⎯⎯⎯)2√

Our pilot studies indicate that more stable values of _ρ_(correlations) are obtained with _L=_[_10,…,15_]. This real-time functional connectivity measure can then be displayed as a feedback to the participant via user-defined visual cues (e.g., a thermometer). The mean value of the time-varying correlation scale (used to set the midline value of the feedback thermometer) employs a sigmoid-weighting discounting function (slope=1), which provides estimates that are more influenced by more recent values, relative to earlier ones (the number of volumes entered in this weighting function can be set by the user, but our experience suggests that a value of 10 volumes may be adequate). The upper and lower bounds of the correlation scale (which define the top and bottom levels of the thermometer) are defined on the basis of the calculated standard deviation of the correlation coefficients over the last L (e.g., 10) volumes. The multiplier of standard deviations is set to 1 by default, but can be changed as well. This provides a smooth and flexible control of the feedback thermometer feedback, and a more “natural” experience for participants whilst they attempt to modulate their own ROI-based correlations. An illustration of functional connectivity neurofeedback is shown in [Video S2](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone.0081658.s002).

### Performance Optimization and Quality Monitoring

All image processing steps, including network communication and image transfer, image registration, feature selection and post-processing (based on single ROI BOLD, SVM or dual-ROI sliding correlation) and neurofeedback GUI display can be performed in under 1.5 seconds (generally within 1 second) on a proper workstation. For this purpose, a number of optimizations were conducted. 

In the Windows version, a DLL containing the FSL 4.1 commands was built to enable full control of command execution. Another reason to build a DLL is the simplified creation of functions related to the pipeline that receives internal memory data structures. This avoids excessive read/write files from disk by exchanging between functions instead of files, by using pointers to already allocated memory, leading to improved performance. Furthermore, having one DLL file replacing sets of different binaries is another advantage. The libSVM DLL was incremented with functions that enable direct reading of Analyze/NIfTI files and of memory data structures. Additionally, an experimental, optional automatic motion detection routine was implemented in FRIEND, based on root mean squared deviations (RMS) from a moving average over _n_ scans (currently set to 40, according to our initial experience). This feature may be useful both to allow the experimenter to monitor a participant’s motion online and to notify the participant if he/she is moving beyond tolerable ranges during image acquisition. The threshold for the excessive movements is user-defined, but we are currently employing an RMS threshold of .4 (absolute deviation from the mean RMS), based on Jenkinson [[37](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B37)] and on our own piloting observations. Furthermore, this same threshold can be used by FRIEND to automatically discard volumes associated with head movement events, therefore minimizing contamination of single ROI, correlation or SVM estimates during real-time fMRI neurofeedback experiments. A similar approach of discarding unreliable scans has been employed in a recent study [[38](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#B38)]. Furthermore, when significant motion is detected, FRIEND’s motion detection module communicates with the feedback module, “freezing” the feedback (i.e., the displayed ring or thermometer level), therefore visually informing participants about their own excessive movement (this is illustrated in [Video S2](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0081658#pone.0081658.s002)).

In terms of performance, considering the acquisition of EPI volumes with 64x64x22 voxel resolution (3.75x3.75x5mm using an FOV=240mm) and whole brain analysis, and employing a PC Intel Core i7 3930v (12 cores), 16GB RAM, SSD 128GB, the processing time for each step was approximately as follows: head motion correction = 562ms; SVM training (including GLM for feature selection) = 10s; SVM testing < 100ms.
