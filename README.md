# Insight Data Science Project

## 1. [Insight into the Medical Records](https://github.com/lanttern/Insight/blob/master/MedicalRecordsAnalysis.ipynb)
The global health care systems are rapidly adopting Electronic Health Records (EHR), which result in dramatically increase of the quantity of medical data that are available for analysis. Along with development of technologies such as machine learning and big data techniques, the data driven healthcare that using big medical data to provide the best, most personalized care and decrease costs of healthcare, is becoming the major trends in the revolution of healthcare industry. This analysis aims to use natural language processing technique to analyze the medical records and give an insight into the medical records that are relevant to stroke. To do that, the MIMIC-III (Medical Information Mart for Intensive Care), a large, single-center database comprising information relating to patients admitted to critical care units at a large tertiary care hospital, is used (1). The whole MIMIC-III database includes 26 tables (1). Here, the analysis focused on 3 tables - the NOTEEVENTS (including nursing and physician notes, ECG reports, radiology reports, and discharge summaries), DIAGNOSES_ICD (Hospital assigned diagnoses, coded using the International Statistical Classification of Diseases and Related Health Problems (ICD) system) and D_DIAGNOSES_ICD (Dictionary of International Statistical Classification of Diseases and Related Health Problems (ICD-9) codes relating to diagnoses) tables. The charge summaries of the NOTEEVENTS data are randomly sampling out for this analysis. Prior to analysis and exploration, the data are cleaned including removing null values, removing incorrect reports and clean non-characteristic letters and replacing medical abbreviations. Then, the medical records in NOTEEVENTS table are associated with the ICD9 codes in DIAGNOSIS_ICD table and with the diagnosis name in D_DIAGNOSIS_ICD table. Next, the records are labeled as stroke and non-stroke based on the ICD9 code and the patients' past medical, social and history information are retrieved. The top 10 diagnoses in the whole dataset are plotted and shown. The 1904 records for stroke patients and 2000 randomly sampled records for non-stroke patients are combined for cosine similarity and component analysis. The similarity of medical information for stroke and non-stroke patients are compared based on the word occurance or weighted word occurance (tfidf). Finally, the principle component analysis is applied to visulize the how stroke and non-stroke samples are separated.

## 2. [Predict risk of stroke](https://github.com/lanttern/Insight/blob/master/MedicalRecordsStrokePrediction.ipynb)
In this section, prediction models including LogisticRegression and Support Vector Machine classifier are implemented to predict the diagnosis and the parameters for each model are optimized in order to obtain the good prediction performance. Specifically, the following steps are followed: 1) split the data into train data (for model selection) and test data (for model validation), 2) use natural language processing (apply stemming to text, compute occurance of words or term frequency–inverse document frequency to transform text notes, 3) perform lasso feature selection using linear support vector classifier, 4) implement and optimize two popular text classifier: the LogisticRegression and Support Vector Machine classifiers, 5) compare the performance of the optimized classifiers that are trained with occurance of words or term frequency–inverse document frequency.

## 3. [Build a stroke warning system](https://github.com/lanttern/Insight/tree/master/sws)
#### Stroke Factors
795,000 people in the US have a stroke every year (Leading cause of disabilities)

134,000 deaths each year (No. 5 cause of death in the US)

Projections show that by 2030, stroke prevalence will increase by more than 20% over 2012

Total direct medical stroke-related costs are projected to triple by 2030, from $71.6 billion in 2012 to $184.1 billion

80% of strokes can be prevented

58% of Americans don’t know if they are at risk for stroke

#### [Stroke Warning System](http://www.sws-anti-stroke.org)
Stroke Warning System (http://www.sws-anti-stroke.org) is an accessible tool to predict risk of stroke. Health insurance company may use this tool to perform prescreen, save lives and decreased costs.

#### Limitations
The model used for Stroke Warning System is trained based on patients' past medical, social and family history information from intensive care unit. Therefore, the model is targeted to process the medical terms and medical languages written in English. The plain words may not yield a good prediction performance. The prediction is NOT a diagnosis, please always check with your doctor if you feel you may be at risk!
