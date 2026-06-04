---
auto_generated: true
digest_mode: full
source_docx: manuscript_RadAdv.docx
generator: pandoc
updated: 2026-05-22 13:11
---
> Full archive. For daily AI use `manuscript_digest.md` (slim). Rerun this script after Word edits.

**Title:**  Predictive Value of Macro- versus Micro-scale Hippocampal Segmentation for Antidepressant Response in Major Depressive Disorder

**Article Type:** Original Research

**Summary Statement:** Macro-scale segmentation of the posterior hippocampus on MRI outperforms micro-scale subfields in predicting antidepressant response in major depressive disorder, with responders showing smaller pretreatment volumes relative to non-responders.

**Key Results:**

1.Macro-scale regional and composite measures generally outperformed fine-grained micro-scale subfields in predicting 6-week treatment response.

2.Smaller pretreatment volumes in the left posterior hippocampus (body and tail) and hippocampal formation composite were significantly associated with better treatment outcomes.

3.Machine learning models utilizing these macro-scale features achieved an area under the receiver operating characteristic curve of up to 0.72, identifying robust prognostic markers.

**Authors: \[blinded\]**

**Academic Affiliations: \[blinded\]**

**\*Corresponding author：\[blinded\]**

**Abbreviations:\**
AI = Asymmetry Index\
AUC = Area Under the Receiver Operating Characteristic Curve\
FDR = False Discovery Rate\
HAMD = Hamilton Depression Rating Scale\
HC = Healthy Control\
MDD = Major Depressive Disorder\
MRI = Magnetic Resonance Imaging\
PCA = Principal Component Analysis\
ROC = Receiver Operating Characteristic\
TabPFN = Tabular Prior-Data Fitted Network

**Abstract**

**Background:** Methodological uncertainty surrounds hippocampal volumetric segmentation strategies along transverse or longitudinal axes. This ambiguity poses a major challenge for clinical application in psychoradiology such as predicting antidepressant response in major depressive disorder (MDD). It remains unclear which segmentation strategy with different level of anatomical granularity could best captures the neurobiological substrate of therapeutic efficacy in MDD.

**Purpose:** We aimed to systematically evaluate and compare the predictive performance of three hippocampal segmentation strategies, in order to identify the most clinically relevant neuroanatomical substrate for antidepressant response.

**Methods:** Pretreatment high-resolution 3T MRI data were collected from 56 medication-free patients with MDD and 70 healthy controls (HCs). Patients were treated with antidepressants, and responders were defined by a ≥50% reduction in Hamilton Depression Scale after 6 weeks of treatment. Hippocampal substructures were automatically segmented using FreeSurfer 7.1.1 and grouped according to three protocols: (1) composite (anatomical aggregation), (2) regional (head, body, tail), and (3) local (histological subfields). Measures were Z-score standardized relative to HCs. Predictive efficacy was evaluated using a dual-framework of group-level inference (ANCOVA, adjusted for age, sex and ICV) and individual-level machine learning classification (TabPFN with nested leave-one-out cross-validation).

Results: Responders exhibited smaller pretreatment volumes, whereas non-responders showed larger volumes relative to HCs. Macro-scale measures (regional and composite protocols) generally outperformed micro-scale local subfields. Specifically, the left posterior hippocampus (regional body and tail) and the hippocampal formation composite exhibited robust predictive signals (PFDR\<0.05; AUCs 0.70–0.72). In contrast, local protocol failed to show independent predictive value.

**Conclusions:** We demonstrated that macro-scale segmentation strategies offer superior predictive utility, and further identified the smaller left posterior hippocampus (body and tail) associated with better for antidepressant response. These findings establish an evidence-based rationale for optimizing segmentation protocols in translational research and highlight the left posterior hippocampus as a predictive marker.

**Keywords:**

antidepressant response; composite volume; hippocampus; major depressive disorder (MDD); sub-field; sub-region;

**Introduction**

The human hippocampus, a limbic structure central to memory consolidation and emotion regulation, has long served as a primary region of interest in neuropsychiatric imaging, particularly in major depressive disorder (MDD)(1, 2). However, its structural complexity poses significant challenges for standardization in imaging, severely impeding clinical translation of research findings. Uncertainty begins at the global level: definitions of the "whole" hippocampus vary widely, ranging from restricted groupings of the cornu ammonis (CA) to broader anatomical formations that include adjacent areas such as the entorhinal and parahippocampal cortices, the fimbria and fornix(3). In an early review, approximately 60 different anatomical guidelines were used in 423 hippocampal MRI studies(4). Roddy et al. demonstrated that the statistical significance of volumetric differences in MDD is highly dependent on how strictly the "global" hippocampus is defined, suggesting that broader definitions may inadvertently dilute focal pathological signals by including non-informative tissue(5).

Beyond the definition of its outer boundaries, the hippocampus is also characterized by complex internal heterogeneity, leading to divergent segmentation models (6). Traditionally, anatomical models have emphasized the transverse (medial-lateral) axis(6). In this framework, the hippocampus is subdivided into discrete histological subfields, including the cornu ammonis (CA1–CA4), dentate gyrus (DG), and subiculum, which correspond to ex vivo investigations in both animal models and humans. With the widespread adoption of automated segmentation tools like FreeSurfer(7, 8), neuroimaging research has increasingly favoured this approach, attempting to map in vivo pathology onto specific histological subfields(5, 9). Conversely, accumulating human functional parcellation and gradient evidence highlights the importance of the longitudinal (anterior-posterior) axis, where the hippocampus is segregated into the head, body, and tail(6, 10). Prior works suggest that these two axes capture distinct neurobiological dimensions: while the transverse axis reflects the intrinsic micro-circuitry and histological properties of hippocampal subfields (e.g., the high neurogenic potential of the dentate gyrus), the longitudinal axis manifests a functional gradient, with the anterior hippocampus primarily involved in emotional processing and the posterior segments more dedicated to cognitive functions and flexibility(6). However, it remains unclear whether micro‑scale local subfields or macro‑scale regional partitions better capture the neurobiological alterations that underlie psychiatric disorders, including MDD.

This ambiguity regarding the most relevant structural dimension is particularly acute in the context of predicting antidepressant response in MDD. Current treatment strategies rely heavily on empirical trial-and-error, with initial response rates hovering around 30–50% (11, 12). To move beyond this inefficient paradigm, translational neuroscience seeks robust pretreatment biomarkers. The hippocampus is a central candidate, theoretically grounded in neurobiological models of hypothalamic-pituitary-adrenal (HPA) axis dysregulation and compromised adult neurogenesis—processes essential for antidepressant efficacy. While a meta-analysis of 374 patients suggests that smaller global hippocampal volumes (both left and right) predict poorer treatment outcomes(13-16), however, conflicting findings continue to be reported (17, 18). Furthermore, the lateralization of these effects is highly variable. Individual studies have reported predictive associations localized to the left(19), right(20), or bilateral(21) hippocampus, which further complicating the identification of a reproducible biomarker. Regarding the substructural level analyses, while the hippocampal tail has emerged as a relatively reproducible marker for antidepressant treatment response, findings regarding other subfields remain fragmented(14, 22). However, it remains unclear which level of granularity in hippocampal segmentation best captures the neurobiological substrates that underlie treatment response and provides robust predictive power at the individual level.

Therefore, in this study, we used antidepressant treatment response in MDD to determine which hippocampal definition and segmentation strategy best captures the pretreatment neuroanatomical substrate of treatment response. The primary objective was to systematically evaluate and compare predictive utility across three defined levels of granularity: at the “global” level, (1) the composite protocol (varying global definitions derived from anatomical aggregation); and at the “parts” level, (2) the regional protocol (macro-scale segmentation along the longitudinal axis into head, body, and tail) and (3) the local protocol (micro-scale segmentation along the transverse axis into discrete histological subfields). By comparing these approaches, we aimed to identify the specific hippocampal definition or subregion most strongly associated with treatment outcome and quantify its predictive performance. We hypothesized that while micro-scale subfields offer greater anatomical detail, macro-scale measures would provide more robust and reproducible predictive signals under standard 3T clinical imaging conditions, as they may be less sensitive to the segmentation noise inherent in fine-grained analysis.**\**

**Materials and methods**

The prospective study was approved by the local Research Ethics Committee, and fully informed written consent was obtained from all participants. The 56 patients with MDD were Han Chinese population. All data were collected between 2008 and 2012. The inclusion criteria for patients were as follows (i) aged 18–60 years, (ii) MDD diagnosed via the Structured Clinical Interview for DSM-IV Axis I Disorders (SCID) by one or other of two experienced psychiatrists, (iii) a total score of 18 or higher on the Hamilton Depression Scale (HAMD), (iv) medication naive or had a wash-out period of at least five half-lives for antidepressant treatment, (v) no neurological diseases or ailments (vi) no heart disease, renal disease, or other major systemic illness (vii) no substance abuse and no contraindication to magnetic resonance imaging (MRI). In addition, 70 age- and sex-matched healthy control participants (HCs) were recruited. The HCs were examined with the SCID (non-patient edition) and were required to have no psychiatric illnesses, no family history of psychiatric illness among first-degree relatives, and to also fulfil criteria (v), (vi) and (vii) as stated above. A subset of this cohort (N=38) was previously reported using FreeSurfer v5.3 (18); however, the present study utilizes v7.1.1 to leverage its improved subfield atlas and longitudinal segmentation capabilities required for the macro-scale benchmarking in the current study(23). (23)

**Magnetic Resonance Imaging (MRI)**

MRI investigations were performed using a 3 T MRI system (EXCITE, GE Signa, Milwaukee, Wisconsin, USA) equipped with an 8-channel phased-array head coil. Soft earplugs were used by each participant to reduce noise from the MRI system to an appropriate level and foam cushions were positioned to minimize head movement. Following a localizer scan, a high-resolution 3D T1 weighted image was a obtained using a spoiled gradient-recalled (SPGR) sequence with the following acquisition parameters, repetition time (TR) 8.5 msec, echo time (TE) 3.4 msec, 156 axial slices, 1 mm section thickness, flip angle 12, axial field of view (FOV) 24 cm × 24 cm and 256 × 256 matrix.

**Hippocampal Segmentation Strategies**

The segmentation of the hippocampus was performed automatically using FreeSurfer software (v.7.1.1) (http://surfer.nmr.mgh.harvard.edu/)(24, 25). Firstly, the 3D T1 weighted structural MR image was processed using the recon-all pipeline. This is a standard workflow for volumetric analysis, and which included removal of non-brain tissue, correction for head motion, and alignment of the image with the Talairach template. Next the signal intensity of the image was normalized and segmentation of the hippocampus and substructures was performed using a Bayesian-inference-based statistical model. Finally, intra-cranial volume (ICV) was extracted for covariate correction.

The segmentation of hippocampal substructures was performed using a special module in FreeSurfer that employs a tetrahedral mesh-based probabilistic atlas built from manually delineated hippocampus maps based on in vivo and ex vivo data(7). To ensure data quality, all segmentations were visually inspected slice-by-slice by a radiologist experienced in neuroanatomy to detect segmentation errors; no subjects required exclusion based on segmentation failure. The hippocampal fissure was excluded from all analyses due to lower segmentation reliability (26). To systematically evaluate the impact of segmentation granularity, hippocampal measures were organized into two hierarchical levels (Details on boundary definitions are illustrated in Figure 1):

1.  **The** **"Global" Level (Composite Strategies)**

To evaluate the utility of different “global hippocampal volume”, we calculated distinct composite volumes constitutes of varying degrees of anatomical inclusion (e.g., Hippocampal Proper, Hippocampal Formation, and Hippocampal Extended). Additional composites were also examined including Combined Dentate (CA4 and DG), CA only, Combined dentate gyrus /CA (CA and DG), and CA2-4. The detailed formulas for calculating these composite volumes are provided in the Supplementary Material Table1.

2.  **The "Parts" Level**

This level focuses on specific anatomical substructures defined along two distinct axes(The detailed formulas see Supplementary Material Table1):

- Local Protocol (Transverse Axis): Segmentation was based on histological boundaries utilizing the ex vivo atlas. This yielded 12 fine-grained subfields: parasubiculum, presubiculum, subiculum, CA1, CA3, CA4, granule cell layer of the dentate gyrus (GC-ML-DG), molecular layer, HATA, fimbria, and the hippocampal tail.

- Regional Protocol (Longitudinal Axis): Segmentation was based on functional anterior-posterior differentiation along the long axis of the hippocampus, yielding 3 macro-regions: the Head, Body, and Tail.

**Assessment of antidepressant treatment responses**

After clinical assessments and MRI had been performed, all MDD patients commenced antidepressant therapy according to one of three potential classes of treatment regimens, namely, tricyclics (n=9), typical serotonin-norepinephrine reuptake inhibitors (n=13) and typical selective serotonin reuptake inhibitors (n=34) as decided by the treating psychiatrist. The patients were reassessed after 6 weeks, using the same psychiatric instruments. Treatment responses were evaluated by calculating the change in the HAMD score (reduction rate of the HAMD score, HAMD RRS) after 6 weeks according to the following formula: RRS = \[(HAMD_baseline – HAMD_6_weeks)/HAMD_baseline\]. Those patients for whom HAMD RRSs ≥ 50% were classified as responders **(RES)** , whereas patients with HAMD RRSs \< 50% were classified as non-responders**(NRES)**(18, 27).

**Data Post-processing and Derivative Calculation**

**Z-score Transformation:** To quantify the degree of structural deviation in patients relative to a healthy baseline and to enhance the comparability of metrics across different segmentation protocols, volumes were Z-score Transformed against the entire HC group. For every hippocampal sub-structure volume (local, regional) and composites, raw values were transformed into Z-scores using the mean ($`\mu_{HC}`$) and standard deviation ($`\sigma_{HC}`$) of the HC group:

``` math
Z_{patient} = \frac{Volume_{patient} - \mu_{HC}}{\sigma_{HC}}
```

Consequently, a Z-score of 0 represents the average volume of the healthy population, while negative and positive values indicate smaller and larger volume, respectively.

**Asymmetry Index (AI) calculation:** We calculated the Asymmetry Index (AI) for all segmented regions to evaluate inter-hemispheric imbalance. The AI was defined as:

``` math
AI = \frac{Left - Right}{Left + Right} \times 100
```

To ensure consistency, the raw AI values were also converted into Z-scores based on the asymmetry distribution of the HC group, utilizing the same normative modeling procedure described above.

**Dimensionality Reduction (PCA)：**Given the high correlation among 12 subfields from local protocol, we additionally conducted a PCA with Varimax rotation on the Z-scored volumes of the local subfields as a data-driven strategy to extract orthogonal latent anatomical factors. This was conducted separately for the left and right hemispheres. Components with eigenvalues \> 1 (Kaiser criterion) were retained. The resulting Component Scores were used as independent variables for further statistical analyses.

**Statistical analysis**

**Group Comparisons and Correlation**

Differences in demographic and clinical characteristics between RES and NRES were assessed using independent sample t-tests (for continuous variables) and chi-square tests (for categorical variables).

For the hippocampal volumetric analysis, Analysis of Covariance (ANCOVA) was performed to compare the Z-scores (both volume and asymmetry) between the RES and NRES groups, with age, sex and ICV corrected. Raw volumes, raw AI values and components extracted from PCA were also tested additionally. Benjamini-Hochberg False Discovery Rate (FDR) correction method was applied within each segmentation protocol (i.e., Local, Regional, and Composite). A two-tailed FDR-corrected *P*-value \< 0.05 was considered statistically significant. Effect sizes for the group differences were estimated using Partial Eta Squared ($`\eta_{p}^{2}`$), classified as small (0.01), medium (0.06), or large (0.14) effects. Partial correlation analyses were performed between HAMD RRS values and aforementioned metrics adjusting for age, sex and ICV (p ＜0.05 was considered statistically significant). All statistical analyses were conducted using Python (v3.9) with the statsmodels and pandas libraries.

**Machine Learning Classification of Treatment Response**

To systematically evaluate and compare the predictive utility across different segmentation protocols, we employed the TabPFN (Tabular Prior-Data Fitted Network) classifier(28). TabPFN is a Transformer-based model pre-trained on a vast array of synthetic datasets to perform in-context learning. Unlike traditional algorithms (e.g., Random Forest or SVM) that often require iterative training and extensive hyperparameter tuning—posing a high risk of overfitting in small-to-medium datasets—TabPFN is explicitly optimized for such scenarios, providing robust probabilistic predictions without the need for manual hyperparameter optimization.

To strictly isolate the contribution of hippocampal features from potential confounders, we implemented a Leave-One-Out Cross-Validation (LOOCV) scheme. Within each fold of the cross-validation loop, a linear regression model was fitted solely on the training set (N−1) to estimate the effects of covariates (age, sex, and ICV). These coefficients were then applied to compute residuals for the held-out test subject, ensuring a rigorous prevention of data leakage. Model performance was primarily evaluated using the Area Under the Receiver Operating Characteristic Curve (AUC). Binary metrics, including sensitivity, specificity, PPV and NPV, were calculated based on the optimal decision threshold defined by Youden’s Index. Feature sets were defined as following:

**Composite Protocol:** Given that composite measures are anatomically nested (e.g., HF contains HP), combinatorial features would introduce redundancy. Therefore, models were trained on single composite Z-scores and their corresponding Asymmetry Indices (AI).

**Regional Protocol:** We evaluated predictive performance at three levels of integration: (1) Unilateral Features (Single Left/Right regions); (2) Bilateral Homotopic Pairs (e.g., L-Body + R-Body); and (3) Combined Posterior Features (e.g., L-Body + L-Tail; AI-Body + AI-Tail). This focus on posterior segments was informed by the significant group differences identified in the preceding statistical analysis.

**Local Protocol:** two distinct approaches were compared: (1) Anatomical Subfields, where models were trained on single subfields as well as aggregated sets of the top-3 and top-5 left-sided subfields (ranked by their effect sizes in the preceding group comparison); and (2) Latent Factors, utilizing Principal Components (e.g., PC1). Crucially, PCA was performed in a nested manner within the cross-validation loop—deriving eigenvectors solely from the training fold—to prevent data leakage.

All candidate models initially underwent LOOCV to obtain raw AUCs. Subsequently, the top 5 performing models within each protocol were subjected to 1,000 bootstrapping iterations to estimate stability (reporting mean AUC with 95% Confidence Intervals) and 1,000 permutation tests to generate empirical *P*-values. DeLong’s tests were performed on the paired risk scores derived from the LOOCV framework for the top-performing models within each protocol using pROC package in R.

In addition, to corroborate the findings from the machine learning model and assess the discriminative capacity of individual hippocampal subregions using standard clinical statistical methods, conventional Receiver Operating Characteristic (ROC) curve analyses were performed. This analysis was conducted using the pROC package in R. For each region identified as significant in the primary analysis, we calculated the Area Under the Curve (AUC), sensitivity, specificity, and optimal cutoff values based on the Youden Index. This step served to verify that the predictive signal stems from robust anatomical differences rather than complex algorithmic artifacts.~~\~~

**Results**

**Demographic and clinical characteristics**

The clinical and demographic characteristics of the patients with MDD and HCs are presented in Table 1. There were no significant age or sex differences between the patients with MDD and HC groups (p \> 0.05). After 6 weeks of treatment with antidepressant, 67.86% (38/56) of the patients with MDD experienced remission of depressive symptoms, corresponding to HAMD RRS≥0.5. These so-called responders did not differ from the non-responders in terms of duration of illness, number of episodes of illness, HAMD score at baseline or the distribution of antidepressant classes (all P \> 0.05).

**Group Differences in Volumetric and Asymmetry Metrics**

A consistent divergent pattern relative to the normative baseline was observed: RES exhibited smaller volumes (negative Z-scores), whereas NRES exhibited larger volumes (positive Z-scores). This pattern was most pronounced in the left hemisphere within the regional and composite protocols (Figure 2). Raw volumes of RES, NRES and HCs were reported in (Supplementary Table 3).

At the "Whole" level, all Composite measures on the left hemisphere successfully differentiated the groups. The largest effect sizes were found in the left Hippocampal Formation (HF) (*P*<sub>FDR</sub>=0.025, partial eta squared=0.18) and Hippocampal Extended (L-HE) *P*<sub>FDR</sub> =0.031, partial eta squared=0.15, Table 2).

At the "Parts" level, ANCOVA revealed that the regional protocol (longitudinal axis) yielded the most robust differentiations (Table 2). Specifically, the left hippocampal body (*P*<sub>FDR</sub> =0.014, partial eta squared=0.16) and tail (*P*<sub>FDR</sub> =0.014, partial eta squared=0.15) showed significant differences with large effect sizes.

In contrast, no single subfield within the local protocol (transverse axis) survived FDR correction for multiple comparisons. PCA on the left local subfields extracted two orthogonal components (eigenvalues \> 1). Principal component 1 (PC1) accounted for the majority of the variance and was characterized by high positive loadings (\> 0.85) from the CA subfields (CA1, CA3, CA4), molecular layer, and GC-ML-DG (Figure 3A), effectively representing a latent "Core Hippocampal Factor." In group comparisons, the left PC1 score exhibited a highly significant reduction in RES compared to NRES (uncorrected *P* =0.004, partial eta squared=0.15), with RES showing negative scores (smaller latent volume). This effect size was comparable to the best regional metric (left body or tail) and superior to any single local subfield (Figure 3C). In contrast, left-PC2 (loaded primarily by fimbria and presubiculum) and right hemisphere components showed no significant group differences or associations with treatment response (Supplementary Figure 1).

Aforementioned significant volumetric differences were restricted to the left hemisphere, suggesting a lateralized effect. This was confirmed by the asymmetry index (AI) analyses (Table 4), where significant differences were found for the regional body ((*P*<sub>FDR</sub> =0.042) and tail ((*P*<sub>FDR</sub> =0.042), as well as global composite AIs (e.g., AI-HF, (*P*<sub>FDR</sub> =0.020, Table 3). All aforementioned significant group differences remained consistent when illness duration was included as an additional covariate in the ANCOVA models, indicating that the observed volumetric patterns were not significantly confounded by disease duration.

**Correlation between Hippocampal Metrics and Treatment Response**

Consistent with the ANCOVA findings, partial correlation analyses revealed significant negative correlations between the HAMD reduction rate (RRS) and the Z-scores of left-sided composite and regional measures (Figure 3). However, no significant linear correlations were found between the AI and RRS except for left HE.

Additionally, the majority of local subfields (especially CA1 and molecular layer) displayed associations with RRS with nominal level significance (uncorrected p \< 0.05). Left-PC1 extracted from left local subfields showed significant correlation with RRS (pr=−0.356, P=0.007). These associations did not survive FDR correction and should be interpreted with caution, specific r and p values were reported in Supplementary Table 4.

**Predictive Performance of Segmentation Protocols**

Using the TabPFN classifier with LOOCV, we evaluated the diagnostic utility of the three segmentation strategies. In the composite protocol, consistent with the group-level analyses, the left HF was the most predictive composite measure, achieving the highest AUC of 0.718 (95% CI: 0.578–0.864, P=0.005). It demonstrated high specificity (0.94) but moderate sensitivity (0.55). The AI of HF also performed well (AUC = 0.675, P=0.017).

In the regional protocol, the combination of bilateral hippocampal body emerged as a top performer (AUC = 0.703, P=0.008), followed closely by the AI of the posterior hippocampus (body + tail), which achieved an AUC of 0.702 (95% CI: 0.549–0.843, P=0.004). In the local protocol, among individual subfields, the left tail showed the highest discriminative power (AUC = 0.683, P=0.010). Aggregating micro-features (Top-3 left subfields) yielded a comparable AUC of 0.677 (P=0.017) but did not outperform the single tail region. The latent factor model (Left PC1+PC2) achieved an AUC of 0.648 (P=0.043).

Overall, the left hippocampal formation (composite) and posterior regional measures (bilateral body / AI-posterior) demonstrated the optimal predictive performance, with permutation P-values \<0.01 and AUCs exceeding 0.70. Performance metrics for top-performing models are summarized in Figure 5 and Table 4, with a comprehensive list of all tested feature sets provided in Supplementary Table 5. Pairwise statistical comparisons of the AUCs using DeLong’s test revealed no significant differences between the top-performing models of the three protocols (all uncorrected P\>.70). Consistent with the machine learning results, conventional univariate ROC analysis confirmed the high discriminative value of posterior hippocampal structures. L-body, L-tail, L-HE and L-HF showed diagnostic performance with areas under the ROC curve＞0.7 (all p\<0.05, ROC curve see supplementary fig 2 and Supplementary Table 6).

**Discussion**

Using both group-level statistics and individual-level machine learning, our study yielded two key findings. (1)First, regarding segmentation strategy, we demonstrate that macro-scale measures (the composite protocols and regional) offer sufficient predictive utility and generally outperformed micro-scale local subfields in the context of standard whole-brain 3D-T1 imaging. Increasing resolution to the subfield level did not provide additional informative value for treatment prediction, even when latent factors were extracted via dimensionality reduction (PCA). (2)Second, we identified the left posterior hippocampus (Body and Tail) and the Hippocampal Formation as the structural loci carrying the strongest predictive signal. Taken together, we revealed a divergent pattern of structural deviation: treatment responders exhibited smaller pretreatment hippocampal volumes, whereas non-responders showed enlarged or comparable volumes. Furthermore, we confirmed a left-hemispheric dominance in these effects. The resulting asymmetry index (AI) thus proved to be a sensitive state marker for classifying clinical outcomes.

First, we found that macro-scale measures generally outperformed micro-scale local subfields. Despite the popularity of the local protocol, individual subfield volumes (e.g., CA1, CA2/3) did not independently predict antidepressant efficacy. These measures were not devoid of signal, as several subfields (e.g., CA1, molecular layer) displayed medium-to-large effect sizes and nominal correlations with outcomes. However, the lack of significance after multiple comparison correction suggests that predictive variance is distributed across collinear structures rather than isolated within discrete boundaries. This aligns with imaging-genetics evidence indicating that core subfields (e.g., CA1-4, dentate gyrus) share 82–90% of their genetic variance with the whole hippocampus (29, 30). Indeed, our PCA recovered the statistical significance lost in univariate analysis through a primary factor (left-PC1) capturing this shared variance. Conversely, subfields known to possess higher genetic specificity (e.g., fimbria, parasubiculum)(29) loaded onto the secondary component (PC2), which showed no predictive utility. This suggests that the variance critical for treatment prediction is effectively aggregated at the macro-scale. From a practical standpoint, this sufficiency of macro-scale markers implies that the significant computational expertise and visual segmentation quality checking often required for micro-scale subfield segmentation may not yield incremental prognostic value in clinical settings.

In line with previous studies(14, 22, 31), we found that posterior hippocampal volumes (specifically the regional body and tail) demonstrated the highest predictive efficacy among the tested population. While prior research has tentatively attributed this to the vascular vulnerability or high CA1 density of the tail(14, 22), these local physiological features alone do not fully explain why our specific subfield measures (e.g., CA1) failed to outperform regional metrics. This posterior localization contrasts with animal models, where the ventral (anterior) hippocampus serves as the primary regulator of stress and emotion, and where neurogenesis is functionally required for the behavioural effects of antidepressants (32). This discrepancy suggests a distinction between the immediate molecular targets of medication and the structural substrate required for clinical remission. According to commonly accepted functional frameworks, while the anterior hippocampus regulates emotion, the posterior segment is preferentially engaged in cognitive functions that support cognitive flexibility(6, 33).  Impaired cognitive flexibility is strongly related to depression, more importantly, is associated with slower recovery and faster relapse(34, 35). Herein, we propose that a plasticity-conducive structural profile in the posterior hippocampus provides the necessary substrate to reorganize maladaptive cognitive circuits in depression. This restoration of flexibility effectively enables the brain to translate acute pharmacological effects into sustained symptomatic improvement. However, given our modest sample size, particularly the limited number of non-responders, these interpretations remain exploratory. Further research with larger, multi-site cohorts is required to validate why the posterior hippocampus serves as such a robust potential target for antidepressant treatment  (14, 15, 36).

Second, regarding the directionality of prediction, the Z-score analysis revealed a divergent pattern of deviation from the normative baseline: non-responders tended toward positive Z-scores (volumes relatively larger than the normative mean), whereas responders exhibited negative Z-scores in substructures showing predictive value. This group-level distinction was underpinned by a continuous linear relationship, where lower Z-scores significantly correlated with greater symptom reduction rates. This finding is consistent with our previous report in a subset of this cohort, where non-responders similarly displayed a trend of volumetric preservation or subtle enlargement in specific subfields using an earlier segmentation atlas(18). Notably, while this pattern initially appears to contrast with previous studies reporting that larger hippocampal volumes predict better treatment outcomes, we posit that this discrepancy is primarily rooted in divergent population characteristics.(14, 22). Specifically, Maller et al. found that larger baseline volumes predicted remission in a chronic MDD cohort (mean illness duration \>10 years) (22).  Similar trends were replicated by Nogovitsyn et al., although specific illness duration was not explicitly characterized in that sample(14). This discrepancy likely reflects the dynamic trajectory of hippocampal morphology throughout the disease course: while volume reductions in chronic or recurrent depression are consistently reported, findings in early-stage depression remain heterogeneous, with reports of preserved (37, 38) or smaller(39, 40) volumes.  Our results extend this perspective by suggesting that a divergent volumetric pattern exists already at the early stage, where a relative positive deviation (compared to the normative baseline) specifically characterizes the non-responsive phenotype. From a mechanistic standpoint, , this subtle volumetric excess in non-responders might reflect active inflammatory processes (e.g., edema) or neurodevelopmental anomalies (e.g., insufficient pruning) that fundamentally differ from the "neurogenic exhaustion" seen in chronic atrophy, thereby conferring resistance to standard antidepressant mechanisms(41, 42). Beyond clinical heterogeneity, methodological variations across studies—such as the adoption of updated segmentation algorithms (FreeSurfer v7.1.1 versus v6.0), differing definitions of clinical outcome metrics, and variations in statistical modeling frameworks—may also account for the divergent results observed across the literature.

Our finding revealed a consistent left-hemisphere dominance through the spatial distribution of predictive signals. This left-lateralization aligns with the majority of prior studies reporting left hippocampus as predictor of antidepressant efficacy(14, 43-46), although reports of no significant lateralized effect exist (22, 31).  Interestingly, while preclinical rodent models rarely exhibit lateralized antidepressant effects, human functional neuroimaging provides compelling convergent evidence(47). For instance, Toki et al. demonstrated that blunted activation specifically in the left posterior hippocampus during positive memory encoding was predictive of poor treatment response(44). This functional deficit in the left posterior hub mirrors the structural volumetric deviation identified in our study, aligning with the possibility that the left posterior hippocampus may serve as a potential interface for the cognitive-emotional integration required for recovery. Further, a distinct pattern emerged: while AI significantly differentiated responders from non-responders, it showed minimal linear correlation with the degree of symptom improvement. This dissociation suggests that inter-hemispheric imbalance may function as a threshold-dependent "state marker" rather than a continuous dose-dependent predictor.

Several limitations of the present study should be acknowledged. First, although the sample size (n = 56) was sufficient for group-level inference, it remains modest for machine learning applications. To mitigate the risk of overfitting, we employed the TabPFN classifier—specifically optimized for small tabular datasets—and validated our findings using rigorous LOOCV and permutation testing. These findings were consistent with AUCs obtained from conventional ROC analysis, reinforcing the robustness of our predictive models. Nevertheless, external validation in larger, multi-site cohorts is essential to confirm generalizability. Second, we only assessed hippocampal morphology once at a single pretreatment time point. Thus, we cannot determine whether the volumetric patterns that differentiated responders from non-responders represent stable traits or transient state markers, nor can we address longer-term outcomes such as relapse or recurrence. Third, our evaluation was based on clinical standard 3T T1-weighted MRI. Finally, our analysis relied on clinically standard 3T T1-weighted MRI, which may limit the signal-to-noise ratio for segmenting fine-grained subfields. Future validation with high-resolution T2-weighted imaging or ultra-high-field (e.g., 7T) imaging could explore whether more subtle predictive value in local subfields, though 7T scanners may not be widely available clinically in the near future.

**Conclusions**

In conclusion, this study demonstrates that macro-scale segmentation strategies (the regional and composite protocols)  are sufficient and provide  superior predictive utility for antidepressant response compared to fine-grained segmentation (the local protocol) in the context of psychoradiology studies. We identified the smaller left posterior hippocampus (body and tail) as a salient neuroanatomical substrate associated with better treatment outcomes. In addition to contributing to our understanding of the relationship between depression etiology, neuropathology, and hippocampal substructure, these findings establish an evidence-based rationale for optimizing hippocampal segmentation protocols in future translational research, potentially simplifying the path toward imaging-guided precision psychiatry.

**Data Availability Statement**

The raw data and codes that were used to obtain the findings reported in this study will be provided upon reasonable request to the corresponding author.

**Acknowledgements**

**\[blinded\]**

**Reference**

1\. Geuze E, Vermetten E, Bremner JD. MR-based in vivo hippocampal volumetrics: 2. Findings in neuropsychiatric disorders. Molecular psychiatry. 2005;10:160-184.

2\. Tartt AN, Mariani MB, Hen R, Mann JJ, Boldrini M. Dysregulation of adult hippocampal neuroplasticity in major depression: pathogenesis and therapeutic implications. Molecular psychiatry. 2022;27:2689-2699.

3\. Morris RG, Amaral DG, Bliss T, Duff K, O'Keefe J: The hippocampus book, Oxford university press; 2024.

4\. Geuze E, Vermetten E, Bremner JD. MR-based in vivo hippocampal volumetrics: 1. Review of methodologies currently employed. Molecular psychiatry. 2005;10:147-159.

5\. Roddy DW, Farrell C, Doolin K, Roman E, Tozzi L, Frodl T, O'Keane V, O'Hanlon E. The Hippocampus in Depression: More Than the Sum of Its Parts? Advanced Hippocampal Substructure Segmentation in Depression. Biological psychiatry. 2019;85:487-497.

6\. Genon S, Bernhardt BC, La Joie R, Amunts K, Eickhoff SB. The many dimensions of human hippocampal organization and (dys)function. Trends in neurosciences. 2021;44:977-989.

7\. Iglesias JE, Augustinack JC, Nguyen K, Player CM, Player A, Wright M, Roy N, Frosch MP, McKee AC, Wald LL, Fischl B, Van Leemput K. A computational atlas of the hippocampal formation using ex vivo, ultra-high resolution MRI: Application to adaptive segmentation of in vivo MRI. NeuroImage. 2015;115:117-137.

8\. Van Leemput K, Bakkour A, Benner T, Wiggins G, Wald LL, Augustinack J, Dickerson BC, Golland P, Fischl B. Automated segmentation of hippocampal subfields from ultra-high resolution in vivo MRI. Hippocampus. 2009;19:549-557.

9\. Cao B, Passos IC, Mwangi B, Amaral-Silva H, Tannous J. Hippocampal subfield volumes in mood disorders. Molecular psychiatry. 2017;22(9): 1352-1358.

10\. Strange BA, Witter MP, Lein ES, Moser EI. Functional organization of the hippocampal longitudinal axis. Nature reviews Neuroscience. 2014;15:655-669.

11\. Rush AJ, Trivedi MH, Wisniewski SR, Nierenberg AA, Stewart JW, Warden D, Niederehe G, Thase ME, Lavori PW, Lebowitz BD, McGrath PJ, Rosenbaum JF, Sackeim HA, Kupfer DJ, Luther J, Fava M. Acute and longer-term outcomes in depressed outpatients requiring one or several treatment steps: a STAR\*D report. The American journal of psychiatry. 2006;163:1905-1917.

12\. Kupfer DJ, Frank E, Phillips ML. Major depressive disorder: new clinical, neurobiological, and treatment perspectives. Lancet (London, England). 2012;379:1045-1055.

13\. Zhou YL, Wu FC, Liu WJ, Zheng W, Wang CY, Zhan YN, Lan XF, Ning YP. Volumetric changes in subcortical structures following repeated ketamine treatment in patients with major depressive disorder: a longitudinal analysis. Translational psychiatry. 2020;10:264.

14\. Nogovitsyn N, Muller M, Souza R, Hassel S, Arnott SR, Davis AD, Hall GB, Harris JK, Zamyadi M, Metzak PD, Ismail Z, Downar J, Parikh SV, Soares CN, Addington JM, Milev R, Harkness KL, Frey BN, Lam RW, Strother SC, Rotzinger S, Kennedy SH, MacQueen GM. Hippocampal tail volume as a predictive biomarker of antidepressant treatment outcomes in patients with major depressive disorder: a CAN-BIND report. Neuropsychopharmacology : official publication of the American College of Neuropsychopharmacology. 2020;45:283-291.

15\. Maller JJ, Broadhouse K, Rush AJ, Gordon E, Koslow S, Grieve SM. Increased hippocampal tail volume predicts depression status and remission to anti-depressant medications in major depression. Molecular psychiatry. 2018;23:1737-1744.

16\. Colle R, Dupong I, Colliot O, Deflesselle E, Hardy P, Falissard B, Ducreux D, Chupin M, Corruble E. Smaller hippocampal volumes predict lower antidepressant response/remission rates in depressed patients: A meta-analysis. World J Biol Psychiatry. 2018;19:360-367.

17\. Joshi SH, Espinoza RT, Pirnia T, Shi J, Wang Y, Ayers B, Leaver A, Woods RP, Narr KL. Structural Plasticity of the Hippocampus and Amygdala Induced by Electroconvulsive Therapy in Major Depression. Biol Psychiatry. 2016;79:282-292.

18\. Hu X, Zhang L, Hu X, Lu L, Tang S, Li H, Bu X, Gong Q, Huang X. Abnormal Hippocampal Subfields May Be Potential Predictors of Worse Early Response to Antidepressant Treatment in Drug-Naïve Patients With Major Depressive Disorder. Journal of magnetic resonance imaging : JMRI. 2019;49:1760-1768.

19\. Sämann PG, Höhn D, Chechko N, Kloiber S, Lucae S, Ising M, Holsboer F, Czisch M. Prediction of antidepressant treatment response from gray matter volume across diagnostic categories. European Neuropsychopharmacology. 2013;23:1503-1515.

20\. Fu CH, Steiner H, Costafreda SG. Predictive neural biomarkers of clinical response in depression: a meta-analysis of functional and structural neuroimaging studies of pharmacological and psychological therapies. Neurobiology of disease. 2013;52:75-83.

21\. Paolini M, Harrington Y, Colombo F, Bettonagli V, Poletti S, Carminati M, Colombo C, Benedetti F, Zanardi R. Hippocampal and parahippocampal volume and function predict antidepressant response in patients with major depression: A multimodal neuroimaging study. Journal of Psychopharmacology. 2023;37:1070-1081.

22\. Maller JJ, Broadhouse K, Rush AJ, Gordon E, Koslow S, Grieve SM. Increased hippocampal tail volume predicts depression status and remission to anti-depressant medications in major depression. Molecular psychiatry. 2018;23:1737-1744.

23\. Wisse LEM, Biessels GJ, Geerlings MI. A Critical Appraisal of the Hippocampal Subfield Segmentation Package in FreeSurfer. Frontiers in Aging Neuroscience. 2014;6.

24\. Fischl B, Salat DH, Busa E, Albert M, Dieterich M, Haselgrove C, van der Kouwe A, Killiany R, Kennedy D, Klaveness S, Montillo A, Makris N, Rosen B, Dale AM. Whole brain segmentation: automated labeling of neuroanatomical structures in the human brain. Neuron. 2002;33:341-355.

25\. Fischl B, Salat DH, van der Kouwe AJ, Makris N, Segonne F, Quinn BT, Dale AM. Sequence-independent segmentation of magnetic resonance images. NeuroImage. 2004;23 Suppl 1:S69-84.

26\. Sämann PG, Iglesias JE, Gutman B, Grotegerd D, Leenings R, Flint C, Dannlowski U, Clarke-Rubright EK, Morey RA, van Erp TGM, Whelan CD, Han LKM, van Velzen LS, Cao B, Augustinack JC, Thompson PM, Jahanshad N, Schmaal L. FreeSurfer-based segmentation of hippocampal subfields: A review of methods and applications, with a novel quality control procedure for ENIGMA studies and other collaborative efforts. Human brain mapping. 2022;43:207-233.

27\. Lui S, Wu Q, Qiu L, Yang X, Kuang W, Chan RC, Huang X, Kemp GJ, Mechelli A, Gong Q. Resting-state functional connectivity in treatment-resistant depression. American Journal of Psychiatry. 2011;168:642-648.

28\. Hollmann N, Müller S, Purucker L, Krishnakumar A, Körfer M, Hoo SB, Schirrmeister RT, Hutter F. Accurate predictions on small data with a tabular foundation model. Nature. 2025;637:319-326.

29\. Hansell NK, Strike LT, van Eijk L, O’Callaghan V, Martin NG, de Zubicaray GI, Thompson PM, McMahon KL, Wright MJ. Genetic specificity of hippocampal subfield volumes, relative to hippocampal formation, identified in 2148 young adult twins and siblings. Twin Research and Human Genetics. 2022;25:129-139.

30\. Elman JA, Panizzon MS, Gillespie NA, Hagler Jr DJ, Fennema‐Notestine C, Eyler LT, McEvoy LK, Neale MC, Lyons MJ, Franz CE. Genetic architecture of hippocampal subfields on standard resolution MRI: How the parts relate to the whole. Human brain mapping. 2019;40:1528-1540.

31\. MacQueen GM, Yucel K, Taylor VH, Macdonald K, Joffe R. Posterior hippocampal volumes are associated with remission rates in patients with major depressive disorder. Biological psychiatry. 2008;64:880-883.

32\. Tanti A, Belzung C. Neurogenesis along the septo-temporal axis of the hippocampus: Are depression and the action of antidepressants region-specific? Neuroscience. 2013;252:234-252.

33\. Anacker C, Hen R. Adult hippocampal neurogenesis and cognitive flexibility - linking memory and mood. Nature reviews Neuroscience. 2017;18:335-346.

34\. Figueroa CA, DeJong H, Mocking RJT, Fox E, Rive MM, Schene AH, Stein A, Ruhé HG. Attentional control, rumination and recurrence of depression. Journal of affective disorders. 2019;256:364-372.

35\. Gao W, Yan X, Chen Y, Yang J, Yuan J. Situation covariation and goal adaptiveness? The promoting effect of cognitive flexibility on emotion regulation in depression. Emotion (Washington, DC). 2025;25:18-32.

36\. MacQueen GM, Yucel K, Taylor VH, Macdonald K, Joffe R. Posterior hippocampal volumes are associated with remission rates in patients with major depressive disorder. Biological psychiatry. 2008;64:880-883.

37\. MacQueen GM, Campbell S, McEwen BS, Macdonald K, Amano S, Joffe RT, Nahmias C, Young LT. Course of illness, hippocampal function, and hippocampal volume in maj or depression. Proceedings of the National Academy of Sciences. 2003;100:1387-1392.

38\. McKinnon MC, Yucel K, Nazarov A, MacQueen GM. A meta-analysis examining clinical predictors of hippocampal volume in patients with major depressive disorder. Journal of Psychiatry and Neuroscience. 2009;34:41-54.

39\. Cole J, Costafreda SG, McGuffin P, Fu CHY. Hippocampal atrophy in first episode depression: A meta-analysis of magnetic resonance imaging studies. Journal of affective disorders. 2011;134:483-487.

40\. Tang M, Zhang L, Zhou Z, Cao L, Gao Y, Wang Y, Li H, Hu X, Bao W, Liang K, Kuang W, Sweeney JA, Gong Q, Huang X. Divergent effects of sex on hippocampal subfield alterations in drug-naive patients with major depressive disorder. Journal of affective disorders. 2024;354:173-180.

41\. Mahajan GJ, Vallender EJ, Garrett MR, Challagundla L, Overholser JC, Jurjus G, Dieter L, Syed M, Romero DG, Benghuzzi H, Stockmeier CA. Altered neuro-inflammatory gene expression in hippocampus in major depressive disorder. Progress in Neuro-Psychopharmacology and Biological Psychiatry. 2018;82:177-186.

42\. Stockmeier CA, Mahajan GJ, Konick LC, Overholser JC, Jurjus GJ, Meltzer HY, Uylings HBM, Friedman L, Rajkowska G. Cellular changes in the postmortem hippocampus in major depression. Biological psychiatry. 2004;56:640-650.

43\. Abdallah CG, Salas R, Jackowski A, Baldwin P, Sato JR, Mathew SJ. Hippocampal volume and the rapid antidepressant effect of ketamine. Journal of Psychopharmacology. 2014;29:591-595.

44\. Toki S, Okamoto Y, Onoda K, Matsumoto T, Yoshimura S, Kunisato Y, Okada G, Shishida K, Kobayakawa M, Fukumoto T, Machino A, Inagaki M, Yamawaki S. Hippocampal activation during associative encoding of word pairs and its relation to symptomatic improvement in depression: A functional and volumetric MRI study. Journal of affective disorders. 2014;152-154:462-467.

45\. Xiao H, Yuan M, Li H, Li S, Du Y, Wang M, Zhu H, Zhang W, Qiu C, Huang X. Functional connectivity of the hippocampus in predicting early antidepressant efficacy in patients with major depressive disorder. Journal of affective disorders. 2021;291:315-321.

46\. Xue S-W, Kuai C, Xiao Y, Zhao L, Lan Z. Abnormal Dynamic Functional Connectivity of the Left Rostral Hippocampus in Predicting Antidepressant Efficacy in Major Depressive Disorder. Psychiatry investigation. 2022;19:562-569.

47\. Guadalupe T, Mathias SR, vanErp TGM, Whelan CD, Zwiers MP, Abe Y, Abramovic L, Agartz I, Andreassen OA, Arias-Vásquez A, Aribisala BS, Armstrong NJ, Arolt V, Artiges E, Ayesa-Arriola R, Baboyan VG, Banaschewski T, Barker G, Bastin ME, Baune BT, Blangero J, Bokde ALW, Boedhoe PSW, Bose A, Brem S, Brodaty H, Bromberg U, Brooks S, Büchel C, Buitelaar J, Calhoun VD, Cannon DM, Cattrell A, Cheng Y, Conrod PJ, Conzelmann A, Corvin A, Crespo-Facorro B, Crivello F, Dannlowski U, de Zubicaray GI, de Zwarte SMC, Deary IJ, Desrivières S, Doan NT, Donohoe G, Dørum ES, Ehrlich S, Espeseth T, Fernández G, Flor H, Fouche JP, Frouin V, Fukunaga M, Gallinat J, Garavan H, Gill M, Suarez AG, Gowland P, Grabe HJ, Grotegerd D, Gruber O, Hagenaars S, Hashimoto R, Hauser TU, Heinz A, Hibar DP, Hoekstra PJ, Hoogman M, Howells FM, Hu H, Hulshoff Pol HE, Huyser C, Ittermann B, Jahanshad N, Jönsson EG, Jurk S, Kahn RS, Kelly S, Kraemer B, Kugel H, Kwon JS, Lemaitre H, Lesch KP, Lochner C, Luciano M, Marquand AF, Martin NG, Martínez-Zalacaín I, Martinot JL, Mataix-Cols D, Mather K, McDonald C, McMahon KL, Medland SE, Menchón JM, Morris DW, Mothersill O, Maniega SM, Mwangi B, Nakamae T, Nakao T, Narayanaswaamy JC, Nees F, Nordvik JE, Onnink AMH, Opel N, Ophoff R, Paillère Martinot ML, Papadopoulos Orfanos D, Pauli P, Paus T, Poustka L, Reddy JY, Renteria ME, Roiz-Santiáñez R, Roos A, Royle NA, Sachdev P, Sánchez-Juan P, Schmaal L, Schumann G, Shumskaya E, Smolka MN, Soares JC, Soriano-Mas C, Stein DJ, Strike LT, Toro R, Turner JA, Tzourio-Mazoyer N, Uhlmann A, Hernández MV, van den Heuvel OA, van der Meer D, van Haren NEM, Veltman DJ, Venkatasubramanian G, Vetter NC, Vuletic D, Walitza S, Walter H, Walton E, Wang Z, Wardlaw J, Wen W, Westlye LT, Whelan R, Wittfeld K, Wolfers T, Wright MJ, Xu J, Xu X, Yun JY, Zhao J, Franke B, Thompson PM, Glahn DC, Mazoyer B, Fisher SE, Francks C. Human subcortical brain asymmetries in 15,847 people worldwide reveal effects of age and sex. Brain imaging and behavior. 2017;11:1497-1514.

<table>
<colgroup>
<col style="width: 27%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 9%" />
<col style="width: 9%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"></th>
<th rowspan="2" style="text-align: center;">HC</th>
<th rowspan="2" style="text-align: center;"><p>MDD</p>
<p>(baseline)</p></th>
<th colspan="2" style="text-align: center;">MDD(6wks)</th>
<th colspan="2" style="text-align: center;">P value</th>
</tr>
<tr>
<th style="text-align: left;"></th>
<th style="text-align: left;">NRES</th>
<th style="text-align: left;">RES</th>
<th style="text-align: left;">MDD vs. HC</th>
<th style="text-align: left;">NRES vs. RES</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">N</td>
<td style="text-align: center;">70</td>
<td style="text-align: center;">56</td>
<td style="text-align: center;">18</td>
<td style="text-align: center;">38</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">-</td>
</tr>
<tr>
<td style="text-align: left;">Age,mean(SD),years</td>
<td style="text-align: left;">34.87(12.35)</td>
<td style="text-align: left;">35.98(11.37)</td>
<td style="text-align: left;">36.72(11.59)</td>
<td style="text-align: left;">35.63(11.41)</td>
<td style="text-align: center;">0.604</td>
<td style="text-align: center;">0.741</td>
</tr>
<tr>
<td style="text-align: left;">Gender(m/f)</td>
<td style="text-align: left;">30/40</td>
<td style="text-align: left;">24/32</td>
<td style="text-align: left;">8/10</td>
<td style="text-align: left;">16/22</td>
<td style="text-align: center;">1.000</td>
<td style="text-align: center;">0.869</td>
</tr>
<tr>
<td style="text-align: left;">Education,mean(SD),years</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">12.88(3.85)</td>
<td style="text-align: left;">12.94(3.21)</td>
<td style="text-align: left;">12.84(4.16)</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">0.927</td>
</tr>
<tr>
<td style="text-align: left;">Number of episodes, mean(SD),n</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">1.70(1.06)</td>
<td style="text-align: left;">1.53(0.94)</td>
<td style="text-align: left;">1.74(1.11)</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">0.683</td>
</tr>
<tr>
<td style="text-align: left;">illness duration, weeks</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">56.89(74.08)</td>
<td style="text-align: left;">70(77.49)</td>
<td style="text-align: left;">55.42(73.42)</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">0.831</td>
</tr>
<tr>
<td style="text-align: left;">HAMD(baseline)</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">23.52(4.51)</td>
<td style="text-align: left;">22.06(3.61)</td>
<td style="text-align: left;">24.21(4.77)</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">0.077</td>
</tr>
<tr>
<td style="text-align: left;">HAMD(6wks)</td>
<td style="text-align: left;"></td>
<td style="text-align: left;">10.91(3.22)</td>
<td style="text-align: left;">13.56(3.45)</td>
<td style="text-align: left;">9.66(2.22)</td>
<td style="text-align: center;">-</td>
<td style="text-align: center;">＜0.001</td>
</tr>
</tbody>
</table>

Table 1 Demographic and Clinical Characteristics of All Subjects

Note: MDD, major depressive disorder; HCs, healthy control subjects; RES, responders; NRES, non-responders; HAMD, Hamilton Rating Scale for Depression;

Table 2. Group comparison of Z-scores between Responders and Non-responders across hippocampal segmentation strategies

<table>
<colgroup>
<col style="width: 31%" />
<col style="width: 18%" />
<col style="width: 18%" />
<col style="width: 10%" />
<col style="width: 10%" />
<col style="width: 11%" />
</colgroup>
<thead>
<tr>
<th></th>
<th>RES (N=38) mean (S.D.)</th>
<th>NRES (N=18) mean (S.D.)</th>
<th>F</th>
<th>Effect Size</th>
<th>P FDR</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="6"><strong>Composites (“global” hippocampus definitions)</strong></td>
</tr>
<tr>
<td>L-HE</td>
<td>-0.35 (1.16)</td>
<td>0.31 (0.96)</td>
<td style="text-align: right;">8.642</td>
<td style="text-align: right;">0.145</td>
<td>0.031*</td>
</tr>
<tr>
<td>L-HF</td>
<td>-0.35 (1.12)</td>
<td>0.37 (0.95)</td>
<td style="text-align: right;">10.858</td>
<td style="text-align: right;">0.176</td>
<td>0.025*</td>
</tr>
<tr>
<td>L.HP</td>
<td>-0.29 (1.15)</td>
<td>0.31 (0.93)</td>
<td style="text-align: right;">7.128</td>
<td style="text-align: right;">0.123</td>
<td>0.031*</td>
</tr>
<tr>
<td>L-Comb.Dentate</td>
<td>-0.30 (1.19)</td>
<td>0.29 (0.99)</td>
<td style="text-align: right;">5.867</td>
<td style="text-align: right;">0.103</td>
<td>0.038*</td>
</tr>
<tr>
<td>L-CA.Only</td>
<td>-0.29 (1.13)</td>
<td>0.29 (0.92)</td>
<td style="text-align: right;">6.762</td>
<td style="text-align: right;">0.117</td>
<td>0.031*</td>
</tr>
<tr>
<td>L-Comb.Dentate.CA</td>
<td>-0.30 (1.16)</td>
<td>0.30 (0.94)</td>
<td style="text-align: right;">7.041</td>
<td style="text-align: right;">0.121</td>
<td>0.031*</td>
</tr>
<tr>
<td>L-CA2.4</td>
<td>-0.29 (1.09)</td>
<td>0.28 (0.89)</td>
<td style="text-align: right;">6.563</td>
<td style="text-align: right;">0.114</td>
<td>0.031*</td>
</tr>
<tr>
<td>R-HE</td>
<td>-0.00 (1.08)</td>
<td>0.22 (0.87)</td>
<td style="text-align: right;">2.678</td>
<td style="text-align: right;">0.05</td>
<td style="text-align: right;">0.168</td>
</tr>
<tr>
<td>R-HF</td>
<td>0.01 (1.07)</td>
<td>0.26 (0.83)</td>
<td style="text-align: right;">2.982</td>
<td style="text-align: right;">0.055</td>
<td style="text-align: right;">0.158</td>
</tr>
<tr>
<td>R-HP</td>
<td>-0.02 (1.03)</td>
<td>0.10 (0.81)</td>
<td style="text-align: right;">1.361</td>
<td style="text-align: right;">0.026</td>
<td style="text-align: right;">0.304</td>
</tr>
<tr>
<td>R-Comb.Dentate</td>
<td>-0.08 (1.00)</td>
<td>0.01 (0.86)</td>
<td style="text-align: right;">0.967</td>
<td style="text-align: right;">0.019</td>
<td style="text-align: right;">0.356</td>
</tr>
<tr>
<td>R-CA.Only</td>
<td>-0.00 (1.03)</td>
<td>0.12 (0.82)</td>
<td style="text-align: right;">1.364</td>
<td style="text-align: right;">0.026</td>
<td style="text-align: right;">0.304</td>
</tr>
<tr>
<td>R-Comb.Dentate.CA</td>
<td>-0.03 (1.02)</td>
<td>0.08 (0.82)</td>
<td style="text-align: right;">1.293</td>
<td style="text-align: right;">0.025</td>
<td style="text-align: right;">0.304</td>
</tr>
<tr>
<td>R-CA2.4</td>
<td>-0.06 (1.01)</td>
<td>-0.08 (0.85)</td>
<td style="text-align: right;">0.238</td>
<td style="text-align: right;">0.005</td>
<td style="text-align: right;">0.628</td>
</tr>
<tr>
<td colspan="6" style="text-align: left;"><strong>Local</strong> (Hippocampal subfields based on the transverse-axis organization)</td>
</tr>
<tr>
<td>L-parasubiculum</td>
<td>-0.13 (1.28)</td>
<td>-0.28 (0.99)</td>
<td style="text-align: right;">0.167</td>
<td style="text-align: right;">0.003</td>
<td style="text-align: right;">0.792</td>
</tr>
<tr>
<td>L-presubiculum</td>
<td>-0.19 (1.11)</td>
<td>-0.03 (0.97)</td>
<td style="text-align: right;">0.695</td>
<td style="text-align: right;">0.013</td>
<td style="text-align: right;">0.529</td>
</tr>
<tr>
<td>L-subiculum</td>
<td>-0.14 (0.94)</td>
<td>0.37 (0.97)</td>
<td style="text-align: right;">6.934</td>
<td style="text-align: right;">0.12</td>
<td style="text-align: right;">0.061</td>
</tr>
<tr>
<td>L-CA1</td>
<td>-0.26 (1.16)</td>
<td>0.29 (0.93)</td>
<td style="text-align: right;">6.136</td>
<td style="text-align: right;">0.107</td>
<td style="text-align: right;">0.061</td>
</tr>
<tr>
<td>L-CA3</td>
<td>-0.28 (0.99)</td>
<td>0.20 (0.83)</td>
<td style="text-align: right;">5.467</td>
<td style="text-align: right;">0.097</td>
<td style="text-align: right;">0.065</td>
</tr>
<tr>
<td>L-CA4</td>
<td>-0.26 (1.20)</td>
<td>0.36 (0.99)</td>
<td style="text-align: right;">6.249</td>
<td style="text-align: right;">0.109</td>
<td style="text-align: right;">0.061</td>
</tr>
<tr>
<td>L-GC.ML.DG</td>
<td>-0.33 (1.18)</td>
<td>0.24 (0.99)</td>
<td style="text-align: right;">5.453</td>
<td style="text-align: right;">0.097</td>
<td style="text-align: right;">0.065</td>
</tr>
<tr>
<td>L-molecular.layer</td>
<td>-0.30 (1.23)</td>
<td>0.38 (1.01)</td>
<td style="text-align: right;">8.375</td>
<td style="text-align: right;">0.141</td>
<td style="text-align: right;">0.061</td>
</tr>
<tr>
<td>L-HATA</td>
<td>-0.56 (0.97)</td>
<td>-0.32 (0.91)</td>
<td style="text-align: right;">1.577</td>
<td style="text-align: right;">0.03</td>
<td style="text-align: right;">0.394</td>
</tr>
<tr>
<td>L-fimbria</td>
<td>-0.02 (1.01)</td>
<td>0.10 (0.72)</td>
<td style="text-align: right;">0.052</td>
<td style="text-align: right;">0.001</td>
<td style="text-align: right;">0.902</td>
</tr>
<tr>
<td>L-Hippocampal_tail</td>
<td>-0.37 (0.96)</td>
<td>0.27 (0.83)</td>
<td style="text-align: right;">8.796</td>
<td style="text-align: right;">0.147</td>
<td style="text-align: right;">0.061</td>
</tr>
<tr>
<td>R-parasubiculum</td>
<td>-0.05 (1.07)</td>
<td>-0.41 (0.87)</td>
<td style="text-align: right;">1.049</td>
<td style="text-align: right;">0.02</td>
<td style="text-align: right;">0.487</td>
</tr>
<tr>
<td>R-presubiculum</td>
<td>-0.02 (1.08)</td>
<td>0.09 (1.06)</td>
<td style="text-align: right;">0.397</td>
<td style="text-align: right;">0.008</td>
<td style="text-align: right;">0.650</td>
</tr>
<tr>
<td>R-subiculum</td>
<td>-0.08 (0.92)</td>
<td>0.36 (0.88)</td>
<td style="text-align: right;">6.313</td>
<td style="text-align: right;">0.11</td>
<td style="text-align: right;">0.061</td>
</tr>
<tr>
<td>R-CA1</td>
<td>0.01 (1.03)</td>
<td>0.22 (0.83)</td>
<td style="text-align: right;">2.327</td>
<td style="text-align: right;">0.044</td>
<td style="text-align: right;">0.293</td>
</tr>
<tr>
<td>R-CA3</td>
<td>-0.05 (1.02)</td>
<td>-0.17 (0.86)</td>
<td style="text-align: right;">0.000</td>
<td style="text-align: right;">0.000</td>
<td style="text-align: right;">0.989</td>
</tr>
<tr>
<td>R-CA4</td>
<td>-0.07 (1.01)</td>
<td>0.03 (0.86)</td>
<td style="text-align: right;">1.054</td>
<td style="text-align: right;">0.02</td>
<td style="text-align: right;">0.487</td>
</tr>
<tr>
<td>R-GC.ML.DG</td>
<td>-0.08 (1.00)</td>
<td>-0.00 (0.85)</td>
<td style="text-align: right;">0.873</td>
<td style="text-align: right;">0.017</td>
<td style="text-align: right;">0.487</td>
</tr>
<tr>
<td>R-molecular.layer</td>
<td>-0.03 (1.07)</td>
<td>0.21 (0.86)</td>
<td style="text-align: right;">2.878</td>
<td style="text-align: right;">0.053</td>
<td style="text-align: right;">0.234</td>
</tr>
<tr>
<td>R-HATA</td>
<td>-0.18 (0.89)</td>
<td>-0.34 (0.84)</td>
<td style="text-align: right;">0.021</td>
<td style="text-align: right;">0.000</td>
<td style="text-align: right;">0.928</td>
</tr>
<tr>
<td>R-fimbria</td>
<td>0.03 (0.96)</td>
<td>0.26 (0.82)</td>
<td style="text-align: right;">0.914</td>
<td style="text-align: right;">0.018</td>
<td style="text-align: right;">0.487</td>
</tr>
<tr>
<td>R-Hippocampal_tail</td>
<td>0.15 (0.94)</td>
<td>0.38 (0.67)</td>
<td style="text-align: right;">2.080</td>
<td style="text-align: right;">0.039</td>
<td style="text-align: right;">0.311</td>
</tr>
<tr>
<td colspan="6"><strong>Regional</strong> (Hippocampal subregions based on the long-axis organization)</td>
</tr>
<tr>
<td>L-head</td>
<td>-0.24 (1.14)</td>
<td>0.19 (0.97)</td>
<td style="text-align: right;">3.987</td>
<td style="text-align: right;">0.073</td>
<td style="text-align: right;">0.102</td>
</tr>
<tr>
<td>L-body</td>
<td>-0.32 (1.13)</td>
<td>0.39 (0.93)</td>
<td style="text-align: right;">9.33</td>
<td style="text-align: right;">0.155</td>
<td style="text-align: right;">0.014*</td>
</tr>
<tr>
<td>L-Hippocampal_tail</td>
<td>-0.37 (0.96)</td>
<td>0.27 (0.83)</td>
<td style="text-align: right;">8.796</td>
<td style="text-align: right;">0.147</td>
<td style="text-align: right;">0.014*</td>
</tr>
<tr>
<td>R-head</td>
<td>-0.01 (0.97)</td>
<td>0.15 (0.91)</td>
<td style="text-align: right;">1.994</td>
<td style="text-align: right;">0.038</td>
<td style="text-align: right;">0.164</td>
</tr>
<tr>
<td>R-body</td>
<td>-0.08 (1.02)</td>
<td>0.12 (0.79)</td>
<td style="text-align: right;">2.019</td>
<td style="text-align: right;">0.038</td>
<td style="text-align: right;">0.164</td>
</tr>
<tr>
<td>R-Hippocampal_tail</td>
<td>0.15 (0.94)</td>
<td>0.38 (0.67)</td>
<td style="text-align: right;">2.08</td>
<td style="text-align: right;">0.039</td>
<td style="text-align: right;">0.164</td>
</tr>
</tbody>
</table>

Note: RES=Responders, NRES=Non-responders. Age, Sex and ICV were adjusted.

Data presented as Mean Z-score (Standard Deviation), calculated based on age- and sex-matched Healthy Controls. Negative and positive values indicate smaller and larger volume, respectively.

\* indicates P \< 0.05 after Benjamini-Hochberg FDR correction. Comb.= Combined

Table 3. Group comparison of Hippocampal Asymmetry Indexes (AI).

<table style="width:100%;">
<colgroup>
<col style="width: 29%" />
<col style="width: 20%" />
<col style="width: 18%" />
<col style="width: 8%" />
<col style="width: 11%" />
<col style="width: 10%" />
</colgroup>
<thead>
<tr>
<th>Asymmetry Index (AI)</th>
<th>RES (N=38) mean (S.D.)</th>
<th><p>NRES (N=18)</p>
<p>mean (S.D.)</p></th>
<th>F</th>
<th>Effect Size</th>
<th>P</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="6"><strong>"Whole" Level (Composite Strategies)</strong></td>
</tr>
<tr>
<td>AI-HE</td>
<td>-2.50 (1.85)</td>
<td>-0.81 (1.84)</td>
<td style="text-align: right;">8.324</td>
<td style="text-align: right;">0.14</td>
<td>0.020*</td>
</tr>
<tr>
<td>AI-HF</td>
<td>-3.12 (2.25)</td>
<td>-1.20 (1.85)</td>
<td style="text-align: right;">8.313</td>
<td style="text-align: right;">0.14</td>
<td>0.020*</td>
</tr>
<tr>
<td>AI-HP</td>
<td>-4.26 (3.59)</td>
<td>-2.04 (2.81)</td>
<td style="text-align: right;">4.424</td>
<td style="text-align: right;">0.08</td>
<td style="text-align: right;">0.057</td>
</tr>
<tr>
<td>AI-Comb.Dentate</td>
<td>-2.60 (3.54)</td>
<td>-0.47 (3.27)</td>
<td style="text-align: right;">3.749</td>
<td style="text-align: right;">0.068</td>
<td style="text-align: right;">0.058</td>
</tr>
<tr>
<td>AI-CA.Only</td>
<td>-4.76 (3.88)</td>
<td>-2.52 (2.81)</td>
<td style="text-align: right;">4</td>
<td style="text-align: right;">0.073</td>
<td style="text-align: right;">0.058</td>
</tr>
<tr>
<td>AI-Comb.Dentate.CA</td>
<td>-3.93 (3.44)</td>
<td>-1.74 (2.81)</td>
<td style="text-align: right;">4.564</td>
<td style="text-align: right;">0.082</td>
<td style="text-align: right;">0.057</td>
</tr>
<tr>
<td>AI-CA2.4</td>
<td>-3.92 (4.53)</td>
<td>-0.78 (3.82)</td>
<td style="text-align: right;">5.375</td>
<td style="text-align: right;">0.095</td>
<td style="text-align: right;">0.057</td>
</tr>
<tr>
<td colspan="6" style="text-align: left;"><strong>Regional</strong> (Hippocampal substructures based on the long-axis organization)</td>
</tr>
<tr>
<td>AI-head</td>
<td>-3.04 (2.83)</td>
<td>-1.72 (2.80)</td>
<td style="text-align: right;">1.972</td>
<td style="text-align: right;">0.037</td>
<td style="text-align: right;">0.166</td>
</tr>
<tr>
<td>AI-body</td>
<td>-1.47 (2.61)</td>
<td>0.44 (2.40)</td>
<td style="text-align: right;">5.84</td>
<td style="text-align: right;">0.103</td>
<td style="text-align: right;">0.042*</td>
</tr>
<tr>
<td>AI-tail</td>
<td>-3.10 (4.02)</td>
<td>-0.69 (2.49)</td>
<td style="text-align: right;">5.096</td>
<td style="text-align: right;">0.091</td>
<td style="text-align: right;">0.042*</td>
</tr>
<tr>
<td colspan="6" style="text-align: left;"><strong>Local</strong> (Hippocampal substructures based on the transverse-axis organization)</td>
</tr>
<tr>
<td>AI-parasubiculum</td>
<td>1.64 (6.98)</td>
<td>3.59 (6.82)</td>
<td style="text-align: right;">0.526</td>
<td style="text-align: right;">0.01</td>
<td style="text-align: right;">0.673</td>
</tr>
<tr>
<td>AI-presubiculum</td>
<td>1.76 (4.95)</td>
<td>2.16 (3.49)</td>
<td style="text-align: right;">0.075</td>
<td style="text-align: right;">0.001</td>
<td style="text-align: right;">0.785</td>
</tr>
<tr>
<td>AI-subiculum</td>
<td>-0.69 (3.58)</td>
<td>-0.26 (3.88)</td>
<td style="text-align: right;">0.098</td>
<td style="text-align: right;">0.002</td>
<td style="text-align: right;">0.785</td>
</tr>
<tr>
<td>AI-CA1</td>
<td>-4.51 (3.89)</td>
<td>-2.87 (2.65)</td>
<td style="text-align: right;">2.104</td>
<td style="text-align: right;">0.04</td>
<td style="text-align: right;">0.255</td>
</tr>
<tr>
<td>AI-CA3</td>
<td>-5.59 (5.95)</td>
<td>-1.29 (4.62)</td>
<td style="text-align: right;">6.271</td>
<td style="text-align: right;">0.109</td>
<td style="text-align: right;">0.078</td>
</tr>
<tr>
<td>AI-CA4</td>
<td>-2.56 (3.66)</td>
<td>-0.37 (3.46)</td>
<td style="text-align: right;">3.677</td>
<td style="text-align: right;">0.067</td>
<td style="text-align: right;">0.152</td>
</tr>
<tr>
<td>AI- GC.ML.DG</td>
<td>-2.64 (3.49)</td>
<td>-0.56 (3.13)</td>
<td style="text-align: right;">3.74</td>
<td style="text-align: right;">0.134</td>
<td style="text-align: right;">0.068</td>
</tr>
<tr>
<td>AI-molecular.layer</td>
<td>-3.17 (2.31)</td>
<td>-1.42 (2.05)</td>
<td style="text-align: right;">6.305</td>
<td style="text-align: right;">0.11</td>
<td style="text-align: right;">0.078</td>
</tr>
<tr>
<td>AI-HATA</td>
<td>-3.77 (6.56)</td>
<td>-0.72 (5.59)</td>
<td style="text-align: right;">2.287</td>
<td style="text-align: right;">0.043</td>
<td style="text-align: right;">0.255</td>
</tr>
<tr>
<td>AI-fimbria</td>
<td>1.13 (9.32)</td>
<td>0.33 (7.09)</td>
<td style="text-align: right;">0.25</td>
<td style="text-align: right;">0.005</td>
<td style="text-align: right;">0.774</td>
</tr>
<tr>
<td>AI-tail</td>
<td>-3.10 (4.02)</td>
<td>-0.69 (2.49)</td>
<td style="text-align: right;">5.096</td>
<td style="text-align: right;">0.091</td>
<td style="text-align: right;">0.094</td>
</tr>
</tbody>
</table>

Note: RES=Responders, NRES=Non-responders.

AI calculated as (Left-Right)/(Left+Right)\*100.

\* indicates P \< 0.05 after Benjamini-Hochberg FDR correction (performed within each protocol category). Comb. = Combined

Table 4 Predictive Performance of Top-5 Models Within Each Segmentation Protocol Using TabPFN Classifier

<table>
<colgroup>
<col style="width: 32%" />
<col style="width: 25%" />
<col style="width: 11%" />
<col style="width: 8%" />
<col style="width: 10%" />
<col style="width: 10%" />
</colgroup>
<thead>
<tr>
<th>Feature Set</th>
<th>AUC (95% CI)</th>
<th>P</th>
<th>Sen.</th>
<th>Spe.</th>
<th>Acc.</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="6"><strong>"Whole" Level (Composite Strategies)</strong></td>
</tr>
<tr>
<td>L-HF</td>
<td>0.718 (0.578-0.864)</td>
<td>0.005*</td>
<td style="text-align: right;">0.55</td>
<td style="text-align: right;">0.94</td>
<td style="text-align: right;">0.68</td>
</tr>
<tr>
<td>AI-HF</td>
<td>0.675 (0.515-0.813)</td>
<td>0.017*</td>
<td style="text-align: right;">0.50</td>
<td style="text-align: right;">0.94</td>
<td style="text-align: right;">0.64</td>
</tr>
<tr>
<td>AI-HE</td>
<td>0.651 (0.486-0.792)</td>
<td>0.038*</td>
<td style="text-align: right;">0.66</td>
<td style="text-align: right;">0.72</td>
<td style="text-align: right;">0.68</td>
</tr>
<tr>
<td>L-Comb. Dentate/CA</td>
<td>0.645 (0.496-0.789)</td>
<td>0.046*</td>
<td style="text-align: right;">0.58</td>
<td style="text-align: right;">0.72</td>
<td style="text-align: right;">0.62</td>
</tr>
<tr>
<td>L- HP</td>
<td>0.637 (0.488-0.782)</td>
<td style="text-align: right;">0.054</td>
<td style="text-align: right;">0.61</td>
<td style="text-align: right;">0.67</td>
<td style="text-align: right;">0.62</td>
</tr>
<tr>
<td colspan="6"><strong>Regional (Hippocampal subfields based on the long-axis organization)</strong></td>
</tr>
<tr>
<td>Bilateral-Body</td>
<td>0.703 (0.558-0.842)</td>
<td>0.008*</td>
<td style="text-align: right;">0.66</td>
<td style="text-align: right;">0.78</td>
<td style="text-align: right;">0.70</td>
</tr>
<tr>
<td>AI- Body+AI-Tail</td>
<td>0.702 (0.549-0.843)</td>
<td>0.004*</td>
<td style="text-align: right;">0.79</td>
<td style="text-align: right;">0.67</td>
<td style="text-align: right;">0.75</td>
</tr>
<tr>
<td>L-Tail</td>
<td>0.683 (0.525-0.826)</td>
<td>0.010*</td>
<td style="text-align: right;">0.58</td>
<td style="text-align: right;">0.83</td>
<td style="text-align: right;">0.66</td>
</tr>
<tr>
<td>L-Body</td>
<td>0.677 (0.529-0.823)</td>
<td>0.026*</td>
<td style="text-align: right;">0.66</td>
<td style="text-align: right;">0.83</td>
<td style="text-align: right;">0.71</td>
</tr>
<tr>
<td>Bilateral- tail</td>
<td>0.665 (0.511-0.808)</td>
<td>0.021*</td>
<td style="text-align: right;">0.63</td>
<td style="text-align: right;">0.83</td>
<td style="text-align: right;">0.70</td>
</tr>
<tr>
<td colspan="6"><strong>Local (Hippocampal subregions based on the transverse-axis organization)</strong></td>
</tr>
<tr>
<td>L- tail</td>
<td>0.683 (0.525-0.826)</td>
<td>0.010*</td>
<td style="text-align: right;">0.58</td>
<td style="text-align: right;">0.83</td>
<td style="text-align: right;">0.66</td>
</tr>
<tr>
<td>Top-3 Left Subfields</td>
<td>0.677 (0.526-0.824)</td>
<td>0.017*</td>
<td style="text-align: right;">0.55</td>
<td style="text-align: right;">0.94</td>
<td style="text-align: right;">0.68</td>
</tr>
<tr>
<td>Top-5 Left Subfields</td>
<td>0.649 (0.498-0.794)</td>
<td>0.042*</td>
<td style="text-align: right;">0.55</td>
<td style="text-align: right;">0.94</td>
<td style="text-align: right;">0.68</td>
</tr>
<tr>
<td>Latent-PC1-2 (Left)</td>
<td>0.648 (0.501-0.797)</td>
<td>0.043*</td>
<td style="text-align: right;">0.55</td>
<td style="text-align: right;">0.83</td>
<td style="text-align: right;">0.64</td>
</tr>
<tr>
<td>L-subiculum</td>
<td>0.646 (0.486-0.804)</td>
<td style="text-align: right;">0.051</td>
<td style="text-align: right;">0.61</td>
<td style="text-align: right;">0.83</td>
<td style="text-align: right;">0.68</td>
</tr>
</tbody>
</table>

**Note:**\
Data were analyzed using the TabPFN classifier with a Leave-One-Out Cross-Validation (LOOCV) scheme. AUC (95% CI): Area Under the Receiver Operating Characteristic Curve. 95% Confidence Intervals were estimated via 1,000 bootstrap iterations. P: Empirical P-value derived from 1,000 permutation tests (shuffling group labels); \* indicates statistical significance (P\<0.05)

Sen./Spe./Acc.: Sensitivity, Specificity, and Accuracy calculated at the optimal decision threshold determined by Youden’s Index.

Top-3 Left Subfields: An aggregated feature set comprising the three local subfields with the largest effect sizes in group comparisons: Hippocampal Tail, Molecular Layer, and Subiculum.

Top-5 Left Subfields: Comprises the Top-3 subfields plus CA4 and CA1.

Abbreviations: AI, Asymmetry Index; CA, Cornu Ammonis; HE, Hippocampal Extended; HF, Hippocampal Formation; HP, Hippocampal Proper; L, Left; PC, Principal Component; R, Right.

**\**

**Figure Legends:**

**Figure 1.** Image processing pipeline and hierarchical hippocampal segmentation strategies. Whole-brain T1-weighted images were processed using the FreeSurfer (v7.1.1) recon-all pipeline and the hippocampus were further segmented into subfields. Final metrics used for later analyses followed three protocol: (1) The Composite Protocol ("Global" Level, bottom right): various existing “global hippocampus” definitions that includes different set of subfields; at the “parts” level, (2) The regional protocol (left bottom), macro-scale segmentation along the longitudinal axis into head, body, and tail; (3) the local protocol (left top),micro-scale segmentation along the transverse axis into discrete histological subfields. Abbreviations: CA, Cornu Ammonis; DG, Dentate Gyrus; Sub, Subiculum; PreSub, Presubiculum; ParaSub, Parasubiculum; HATA, Hippocampal-Amygdaloid Transition Area; Mol. Layer, Molecular Layer; HE, Hippocampal Extended; HF, Hippocampal Formation; HP, Hippocampal Proper; Comb.DG, Combined Dentate.

**Figure 2.** Volumetric profiles and effect sizes distinguishing Responders from Non-responders across segmentation protocols. (a, b) Z-score standardized volumes relative to the healthy control baseline for the left (a) and right (b) hemispheres. Blue bars represent responders; red bars represent non-responders. Error bars indicate 95% confidence intervals. Effect sizes (partial eta squared) for group differences in volumes (c) and asymmetry Index (d). Vertical dotted lines represent thresholds for small (0.01), medium (0.06), and large (0.14) effect sizes. Asterisks denote FDR level significance within protocols.

**Figure 3.** Data-driven identification of a latent "core hippocampal factor" in the local protocol, left hemisphere. (A) Heatmap displaying the contribution of each local subfield to the two extracted principal components (PC1 and PC2). PC1 is heavily loaded by the core subfields (CA1-4, Mol. Layer, DG), representing a shared anatomical variance. This PC1 score showed significant difference between responders and non-responders (B), and significant correlation with HAMD reduction rate (C). Effect size comparison showed the effect size (partial eta squared) of the latent PC1 factor surpasses all single subfields(D). Dotted line indicates Large Effect Size threshold (0.14).

**Figure 4.** Circular heatmap showing the association between hippocampal metrics and antidepressant response. The heatmap displays partial correlation coefficients ($`pr`$) between the HAMD reduction rate and hippocampal metrics, adjusted for age, sex, and ICV. The plot is organized into concentric rings representing the left hemisphere (outer), right hemisphere (middle), and asymmetry index (inner). Segments are grouped by segmentation protocol: composite (orange labels), regional (purple labels), and local (gray labels). Asterisks (\*) denote nominal statistical significance (P\<0.05, uncorrected).

**Figure 5.** Predictive performance of top models across segmentation protocols.\
(a) ROC curves for the best-performing feature set within each protocol.\
(b) AUC values for the top 5 models in composite (orange background), regional (purple), and local (green) protocols. Error bars represent 95% confidence intervals derived from bootstrapping. Asterisks indicate statistical significance based on permutation testing (\* p \< 0.05, \*\* p \< 0.01). Vertical dotted line represents random chance (AUC = 0.50).

**Supplementary Fig 1**. Principle Component Analysis (PCA) of the local protocol on the right hemisphere. Two principal components (PC1 and PC2) were extracted. PC1 is heavily loaded by the core hippocampal subfields (CA, DG, Mol. Layer, HATA and Tail), while PC2 is loaded by the subiculum complex and fimbria(A). However, neither of these principal components differ between responders or non-responders (B), or show correlations with reduction rates of HAMD score (C). The effect size of PC1 and PC2 didn’t surpass any of the subfield volume z-scores (D).

**Supplementary Figure 2.** ROC curves for individual hippocampal metrics in distinguishing treatment responders. Receiver Operating Characteristic (ROC) curves illustrate the diagnostic performance of the top-performing univariate predictors identified in the regional (L-body, L-tail) and composite (L-HE, L-HF) protocols. All four metrics demonstrated significant discriminative power with Areas Under the Curve (AUC) \> 0.70 (P\<0.05), consistent with the multivariate TabPFN results. L-body and L-HF exhibited the highest sensitivity at low false positive rates. L, Left; HE, Hippocampal Extended; HF, Hippocampal Formation.
