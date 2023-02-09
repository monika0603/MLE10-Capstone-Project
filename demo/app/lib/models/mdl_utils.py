import pandas as pd
import pickle
import lib.utils as libPaths


#--- load, merge data from file
m_kstrDataPath = libPaths.pth_data
m_kstrModelPath = libPaths.pth_model
m_kstrBinModelPath = libPaths.pth_binModels

#m_kstrScalerPath_claims = m_kstrBinModelPath + 'stdClaims_scaler_colab.pkl'         #--- does not work for scaling claims data;  from v1.0.2; using 1.1.1
#m_kstrScalerPath_claims2 = m_kstrBinModelPath + 'std_scaler_unsuperv_colab.pkl'     #--- does not work; expects 32 features 
m_kstrScalerPath_claims = m_kstrBinModelPath + 'stdClaims_scaler_colab_v1.2.1.pkl'   
m_kstrScalerPath_providers = m_kstrBinModelPath + 'stdProvider_scaler_colab.pkl'
m_kstrScalerPath_providers_superv = m_kstrBinModelPath + 'gbc_scaler.pkl'
m_kstrScalerPath_providers_train = m_kstrBinModelPath + "stdProvider_scaler.pkl" 
   


def doProviders_stdScaler(pdfFeatEng, blnIsTrain=False, hasGroupByProviderCols=True):
    print("INFO (claims.do_stdScaler):  blnIsTrain, ", blnIsTrain)

    #--- Note:  prediction runs on X_val
    '''
    #--- WARN:  The default value of numeric_only in DataFrameGroupBy.sum is deprecated. 
    #           In a future version, numeric_only will default to False. Either specify 
    #           numeric_only or select only columns which should be valid for the function.
    '''

    #--- WARN:  this code groups all data by provider;  any predictions will also be by provider
    pdfGroupBy = pdfFeatEng
    if (hasGroupByProviderCols):
        pdfGroupBy = pdfFeatEng.groupby(['Provider'], as_index=False).agg('sum')
    
    X = pdfGroupBy

    try:
        X = X.drop(columns=['Provider'], axis=1)        #--- cannot scale;  text
    except KeyError:
        #--- likely column not found; invalid fxn call
        print("ERROR (mdlUtils.doProviders_stdScaler):  Provider col not found")

    try:
        X = X.drop(columns=['PotentialFraud'], axis=1)  
    except KeyError:
        #--- likely column not found; invalid fxn call
        print("ERROR (mdlUtils.doProviders_stdScaler):  Potential Fraud col not found")


    #--- apply std scaler
    #--- WARN:  scaling is also grouped by provider
    print("INFO (mdlUtils.doProviders_stdScaler)  cols: ", X.columns)
    X_std = fitProviders_txfStdScaler(X, blnIsTrain)
    return X_std



def doClaims_stdScaler(pdfFeatEng, blnIsTrain=False):
    print("INFO (mdlUtils.doClaims_stdScaler):  blnIsTrain, ", blnIsTrain)

    #--- Note:  prediction runs on X_val
    '''
    #--- WARN:  The default value of numeric_only in DataFrameGroupBy.sum is deprecated. 
    #           In a future version, numeric_only will default to False. Either specify 
    #           numeric_only or select only columns which should be valid for the function.
    '''

    #--- WARN:  this code groups all data by provider;  any predictions will also be by provider
    X = pdfFeatEng

    try:
        X = X.drop(columns=['Provider'], axis=1)        #--- cannot scale;  text
    except KeyError:
        #--- likely column not found; invalid fxn call
        print("ERROR (mdlUtils.do_stdScaler):  Provider col not found")

    try:
        X = X.drop(columns=['PotentialFraud'], axis=1)  
    except KeyError:
        #--- likely column not found; invalid fxn call
        print("ERROR (mdlUtils.do_stdScaler):  Potential Fraud col not found")


    #--- apply std scaler
    #--- WARN:  scaling is also grouped by provider
    #print("INFO (mdlUtils.doClaims_stdScaler)  cols: ", X.columns)
    X_std = fitClaims_txfStdScaler(X, blnIsTrain)
    return X_std



def doProviders_stdScaler_toPdf(npaScaled):
    #--- NOTE:  the list of cols came from doProvider_stdScaler; print(X.columns)
    aryCols = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'AdmittedDays',
       'NoOfMonths_PartACov', 'NoOfMonths_PartBCov', 'ChronicCond_Alzheimer',
       'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
       'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary',
       'ChronicCond_Depression', 'ChronicCond_Diabetes',
       'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis',
       'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke',
       'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
       'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Age', 'DeadOrNot',
       'Gender_2', 'Race_2', 'Race_3', 'Race_5',
       'ClaimReimbursement_ProviderAvg',
       'ClaimReimbursement_AttendingPhysician',
       'ClaimReimbursement_OperatingPhysician',
       'DeductibleAmtPaid_ProviderAvg', 'DeductibleAmtPaid_AttendingPhysician',
       'DeductibleAmtPaid_OperatingPhysician']

    #npaScaled = do_stdScaler(pdfFeatEng)
    pdfScaled = pd.DataFrame(npaScaled, columns=aryCols)
    return pdfScaled



def doClaims_stdScaler_toPdf(npaScaled):
    #--- NOTE:  the list of cols came from doClaims_stdScaler; print(X.columns)
    aryCols = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'AdmittedDays',
       'RenalDiseaseIndicator', 'NoOfMonths_PartACov', 'NoOfMonths_PartBCov', 'ChronicCond_Alzheimer',
       'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
       'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary',
       'ChronicCond_Depression', 'ChronicCond_Diabetes',
       'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis',
       'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke',
       'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
       'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Age', 'DeadOrNot',
       'Gender_2', 'Race_2', 'Race_3', 'Race_5']

    #npaScaled = do_stdScaler(pdfFeatEng)
    pdfScaled = pd.DataFrame(npaScaled, columns=aryCols)
    return pdfScaled




def fitClaims_stdScaler(pdfData, blnIsTrain=False):
    #--- apply scaler
    #--- WARN:  scaling is not grouped by provider
    from sklearn.preprocessing import StandardScaler

    #--- note:  this is a numpy.ndarray
    #--- we need to fit the scaler, and then save as a pkl file
    #strScalerPath = m_kstrScalerPath_claims
    strScalerPath = m_kstrScalerPath_claims
#    strScalerPath = m_kstrBinModelPath + "stdClaims_scaler_colab.pkl"
    print("INFO (lib.model.fitClaims_stdScalar):  ", strScalerPath)
    if (blnIsTrain):
        scaler = StandardScaler()
        sclFit = scaler.fit(pdfData)
        #--- if we train locally;  write out to gbc_scalar.pkl
        #--- we do not want to overwrite the colab version used for test
        strScalerPath = m_kstrBinModelPath + "stdClaims_scaler.pkl"
        print("WARN (lib.model.fit_stdScalar)  Using local pkl for Train: ", strScalerPath)
        with open(strScalerPath, 'wb') as filPkl:
            pickle.dump(sclFit, filPkl)
    else:
        #--- we need to load the pkl file
        print("WARN (lib.model.fit_stdScalar)  Using colab pkl for Test: ", strScalerPath)
        with open(strScalerPath, 'rb') as filPkl:
            sclFit = pickle.load(filPkl)
        print("WARN (libModel.fitClaims_stdScalar)  sclFit.type: ", type(sclFit))
        print("INFO (libModel.fitClaims_stdScalar)  sclFit.version: " , sclFit.__getstate__()['_sklearn_version'])

        #--- testing
        scaler = StandardScaler()
        print("INFO (libModel.fitClaims_stdScalar)  StdScaler.version: ", scaler.__getstate__()['_sklearn_version'])
    return sclFit



def fitProviders_stdScaler(pdfData, blnIsTrain=False):
    #--- apply scaler
    #--- WARN:  scaling is also grouped by provider
    from sklearn.preprocessing import StandardScaler

    #--- note:  this is a numpy.ndarray
    #--- we need to fit the scaler, and then save as a pkl file
    #strScalerPath = m_kstrScalerPath_providers
    #strScalerPath = m_kstrScalerPath_providers_train            
    strScalerPath = m_kstrScalerPath_providers_superv          #--- works for provider test
    print("INFO (libModel.fitProviders_stdScalar):  ", strScalerPath)
    if (blnIsTrain):
        scaler = StandardScaler()
        sclFit = scaler.fit(pdfData)
        #--- if we train locally;  write out to gbc_scalar.pkl
        #--- we do not want to overwrite the colab version used for test
        strScalerPath = m_kstrScalerPath_providers_train       #--- works for provider training
        print("WARN (libModel.fitProviders_stdScalar)  Using local pkl for Train: ", strScalerPath)
        with open(strScalerPath, 'wb') as filPkl:
            pickle.dump(sclFit, filPkl)
    else:
        #--- we need to load the pkl file
        print("WARN (libModel.fitProviders_stdScalar)  Using colab pkl for Test: ", strScalerPath)
        with open(strScalerPath, 'rb') as filPkl:
            sclFit = pickle.load(filPkl)
        print("WARN (libModel.fitProviders_stdScalar)  sclFit.type: ", type(sclFit))
    return sclFit



def fitProviders_stdScalerSuperv(pdfData, blnIsTrain=False):
    #--- apply scaler
    #--- WARN:  scaling is also grouped by provider
    from sklearn.preprocessing import StandardScaler

    #--- note:  this is a numpy.ndarray
    #--- we need to fit the scaler, and then save as a pkl file
    strScalerPath = m_kstrScalerPath_providers
    print("INFO (libModel.fitProviders_stdScalar):  ", strScalerPath)
    if (blnIsTrain):
        scaler = StandardScaler()
        sclFit = scaler.fit(pdfData)
        #--- if we train locally;  write out to gbc_scalar.pkl
        #--- we do not want to overwrite the colab version used for test
        strScalerPath = m_kstrBinModelPath + "stdProvider_scaler.pkl"
        print("WARN (libModel.fitProviders_stdScalar)  Using local pkl for Train: ", strScalerPath)
        with open(strScalerPath, 'wb') as filPkl:
            pickle.dump(sclFit, filPkl)
    else:
        #--- we need to load the pkl file
        print("WARN (libModel.fitProviders_stdScalar)  Using colab pkl for Test: ", strScalerPath)
        with open(strScalerPath, 'rb') as filPkl:
            sclFit = pickle.load(filPkl)
        print("WARN (libModel.fitProviders_stdScalar)  sclFit.type: ", type(sclFit))
    return sclFit



def fitProviders_txfStdScaler(pdfData, blnIsTrain=False):
    from sklearn.preprocessing import StandardScaler
    sclFit = fitProviders_stdScaler(pdfData, blnIsTrain)
    X_std = sclFit.transform(pdfData)
    return X_std



def fitClaims_txfStdScaler(pdfData, blnIsTrain=False):
    from sklearn.preprocessing import StandardScaler
    sclFit = fitClaims_stdScaler(pdfData, blnIsTrain)


    X_std = sclFit.transform(pdfData)
    return X_std