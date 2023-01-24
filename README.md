# MLE10-Capstone-Project

## Health Care Anomaly Detection

**Business Objective**

Rampant fraud in US healthcare system results in increased premiums for many vulnerable citizens who cannot afford to pay hefty price for a fundamental right such as healthcare. The aim is to find patterns of fraud committed by providers and train ML models to detect similar patterns in the future. 
Abuse in healthcare system can take many forms such as:
    - Billing for services that were not rendered.
    - Duplicate submission of a claim for the same service.
    - Charging for a more complex or expensive than was actually provided.

In addition, there can be unintentional mistakes that result in erroneous charges.

**Data**
The dataset for the capstone project was obtained from Kaggle.
The Kaggle data is divided into four sections:
- Provider: labeled as fraud or not
- Beneficiary information
- In-patient information
- Out-patient information

The provider names are anonymized.   Beneficiary name, state, insurance provider name are masked. 
The beneficiary, in-patient, and out-patient data were merged together and features were derived at the provider level.

**Modeling**
Three supervised model were built to predict potential fraud at the provider level.  There can be multiple doctors and claims for each provider.  Because the Kaggle dataset contained fraud labels at the provider level only, individual claims cannot be flagged as anomalies or suspected fraud. 

Models fit to the training data included:
- Logistic Regression
- Support Vector Machine
- TPOT Auto-ML which selected an XGBoostClassifier

**Future Planned Modeling**
After reviewing the initial results of the supervised models, a decision was made to change direction and focus on detecting anomalies whether the anomalies be fraud or simply human error such as typos.  Unsupervised learning using auto-encoders will be used to detect anomalies at the claim level. 


**Model Implementation for Demo**
The XGBoost Classifier model was saved by using pickle - Python’s built-in persistence model.  To serve the model a fastapi implementation will be used.

