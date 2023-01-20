import pandas as pd
#import os


m_kstrDataPath = "./app/data/"
#print("INFO:  ", os.getcwd())


#--- load, merge data from file
#def loadCsv_trainData():

def loadCsv_testData():
    #--- TODO:  make optional arg test or train data

    #--- load all csv test data
    #--- ouput:  pandas data frame
    pdfTest_provider = pd.read_csv(m_kstrDataPath + 'Test-1542969243754.csv') 
    pdfTest_benef = pd.read_csv(m_kstrDataPath + 'Test_Beneficiarydata-1542969243754.csv')
    pdfTest_inpat = pd.read_csv(m_kstrDataPath + 'Test_Inpatientdata-1542969243754.csv')
    pdfTest_outpat = pd.read_csv(m_kstrDataPath + 'Test_Outpatientdata-1542969243754.csv') 

    #--- data engineering 
    pdfTest_benef = prep_benefData(pdfTest_benef)
    pdfTest_inpat = prep_inpatData(pdfTest_inpat)

    #--- merge inpatient and outpatient data (assert: 31 cols)
    aryMergeCols = list(pdfTest_outpat.columns)
    pdfTest_allpat = pdfTest_inpat.merge(pdfTest_outpat, on=aryMergeCols, how='outer')

    #--- +merge beneficiary data
    pdfTest_allPatBenef = pdfTest_allpat.merge(pdfTest_benef, on='BeneID', how='inner')

    #--- +merge provider data
    pdfTest_allPatBenefProv = pdfTest_allPatBenef.merge(pdfTest_provider, on='Provider', how='inner')
    
    pdfTest_allPatBenefProv.to_pickle(m_kstrDataPath + 'deng_testPatBenefProv.pkl')
    return pdfTest_allPatBenefProv


def do_featEng(pdfLoaded):
    #--- remove cols
    #--- note:  remove the Potential Fraud column if it exists
    aryColsToDrop = ['BeneID', 'ClaimID', 'ClaimStartDt','ClaimEndDt','AttendingPhysician',
                     'OperatingPhysician', 'OtherPhysician', 'ClmDiagnosisCode_1',
                     'ClmDiagnosisCode_2', 'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4',
                     'ClmDiagnosisCode_5', 'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7',
                     'ClmDiagnosisCode_8', 'ClmDiagnosisCode_9', 'ClmDiagnosisCode_10',
                     'ClmProcedureCode_1', 'ClmProcedureCode_2', 'ClmProcedureCode_3',
                     'ClmProcedureCode_4', 'ClmProcedureCode_5', 'ClmProcedureCode_6',
                     'ClmAdmitDiagnosisCode', 'AdmissionDt',
                     'DischargeDt', 'DiagnosisGroupCode','DOB', 'DOD',
                     'State', 'County']
    pdfFeatEng = pdfLoaded.drop(columns=aryColsToDrop, axis=1)

    #--- flag categorical cols
    pdfFeatEng.Gender = pdfFeatEng.Gender.astype('category')
    pdfFeatEng.Race = pdfFeatEng.Race.astype('category')

    #--- one-hot-encoding
    pdfFeatEng = pd.get_dummies(pdfFeatEng, columns=['Gender', 'Race'], drop_first=True)
    pdfFeatEng.loc[pdfFeatEng['RenalDiseaseIndicator'] == 'Y', 'RenalDiseaseIndicator'] = 1 
    pdfFeatEng['DeductibleAmtPaid'].fillna(0, inplace=True)
    pdfFeatEng['AdmittedDays'].fillna(0, inplace=True)

    #--- correlated cols

    #--- add new features to assist with predictions
    pdfFeatEng['ClaimReimbursement_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['InscClaimAmtReimbursed'].transform('mean') 
    pdfFeatEng['ClaimReimbursement_AttendingPhysician'] = pdfFeatEng.groupby(['Provider'])['InscClaimAmtReimbursed'].transform('mean')
    pdfFeatEng['ClaimReimbursement_OperatingPhysician'] = pdfFeatEng.groupby(['Provider'])['InscClaimAmtReimbursed'].transform('mean')

    pdfFeatEng['DeductibleAmtPaid_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['DeductibleAmtPaid'].transform('mean')
    pdfFeatEng['DeductibleAmtPaid_AttendingPhysician'] = pdfFeatEng.groupby(['Provider'])['DeductibleAmtPaid'].transform('mean')
    pdfFeatEng['DeductibleAmtPaid_OperatingPhysician'] = pdfFeatEng.groupby(['Provider'])['DeductibleAmtPaid'].transform('mean')
    return pdfFeatEng


def do_stdScaler(pdfFeatEng):
    #--- Note:  prediction runs on X_val
    pdfGroupBy = pdfFeatEng.groupby(['Provider'], as_index=False).agg('sum')
    X = pdfGroupBy.drop(columns=['Provider', 'PotentialFraud'], axis=1)

    #--- apply scaler
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

    X_minmax = scaler.fit_transform(X)                          # BUG? not sure about a refit/transform that may not match the model
    #X_test = scaler.transform(test_final_groupby.iloc[:, 1:])  # BUG? still has provider, pot_fraud cols
    return X_minmax


#--- data eng on inpatient data
def prep_inpatData(pdfInpat):
    #--- calc admitted days
    pdfInpat['AdmissionDt'] = pd.to_datetime(pdfInpat['AdmissionDt'], format='%Y-%m-%d')
    pdfInpat['DischargeDt'] = pd.to_datetime(pdfInpat['DischargeDt'], format='%Y-%m-%d')
    pdfInpat['AdmittedDays'] = round((pdfInpat['DischargeDt'] - pdfInpat['AdmissionDt']).dt.days + 1)
    return pdfInpat


#--- data eng on beneficiary data
def prep_benefData(pdfBenef):
    #--- chronic condition cols;  change any vals of 2 to 0 
    aryCols = ['ChronicCond_Alzheimer', 'ChronicCond_Heartfailure', 
                'ChronicCond_KidneyDisease', 'ChronicCond_Cancer',
                'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression',
                'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart',
                'ChronicCond_Osteoporasis', 'ChronicCond_rheumatoidarthritis',
                'ChronicCond_stroke'] 

    for strVal in aryCols:
        pdfBenef.replace({strVal: 2}, 0, inplace=True)

    #--- fill missing data:  persons age
    kstrDatetime = '2019-12-01'                            #--- the est datetime for the dataset
    pdfBenef['DOB'] = pd.to_datetime(pdfBenef['DOB'], format = '%Y-%m-%d')
    pdfBenef['DOD'] = pd.to_datetime(pdfBenef['DOD'], format = '%Y-%m-%d') 
    pdfBenef['Age'] = round((pdfBenef['DOD'] - pdfBenef['DOB']).dt.days/365)
    pdfBenef['Age'].fillna(round(((pd.to_datetime(kstrDatetime, format='%Y-%m-%d') - pdfBenef['DOB']).dt.days)/365), inplace=True)

    #--- add an isDead flag column
    pdfBenef.loc[pdfBenef['DOD'].isna(), 'DeadOrNot'] = 0 
    pdfBenef.loc[pdfBenef['DOD'].notna(), 'DeadOrNot'] = 1 

    return pdfBenef