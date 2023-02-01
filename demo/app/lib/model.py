import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import lib.utils as libPaths
#from pickle import load, dump
from pathlib import Path
import pickle


kstrBasePath = Path(__file__).resolve().parent.parent
kstrMdlPath = str(kstrBasePath / "model/")

m_kstrDataPath = libPaths.pth_data
m_kstrModelPath = libPaths.pth_model

#m_kstrMdlPath_gbc = kstrMdlPath + '/gbc_model.pkl'
m_kstrMdlPath_gbc = kstrMdlPath + '/gbc_model_colab.pkl'
m_kstrMdlPath_lgr = kstrMdlPath + '/lgr_model_colab.pkl'
m_kstrMdlPath_svm = kstrMdlPath + '/svm_model_colab.pkl'

#--- default methods
def load():
    return loadGBC_fromPkl()

def train(pdfData):
    return trainGBC(pdfData)

def predict(npaData):
    return predictGBC(npaData)


#--- Unsupervised:  autoencoder
m_kstrMdlPath_enc = kstrMdlPath + '/autoencoder_model.pkl'
def loadEnc_fromPkl():
    with open(m_kstrMdlPath_enc, 'rb') as filPkl:
        # load using pickle de-serializer
        mdlAnoms = pickle.load(filPkl)
    return mdlAnoms


def predictEnc(npaData):
    #--- input:  numpy.ndarray of feature eng, and scaled data 
    mdlAnoms = loadEnc_fromPkl()
    npaPredict = mdlAnoms.predict(npaData)

    #--- AttributeError: 'GradientBoostingClassifier' object has no attribute '_loss'
    print("INFO (npaPredict.shape):  ", npaPredict.shape)
    return npaPredict



def fit_stdScaler(pdfData, blnIsTrain=False):
    #--- apply scaler
    #--- WARN:  scaling is also grouped by provider
    from sklearn.preprocessing import StandardScaler

    #--- note:  this is a numpy.ndarray
    #--- we need to fit the scaler, and then save as a pkl file
    strScalerPath = m_kstrModelPath + "std_scaler_colab.pkl"
    print("INFO (lib.model.fit_stdScalar):  ", strScalerPath)
    if (blnIsTrain):
        scaler = StandardScaler()
        sclFit = scaler.fit(pdfData)
        #--- if we train locally;  write out to gbc_scalar.pkl
        #--- we do not want to overwrite the colab version used for test
        strScalerPath = m_kstrModelPath + "gbc_scaler.pkl"
        print("WARN (lib.model.fit_stdScalar)  Using local pkl for Train: ", strScalerPath)
        with open(strScalerPath, 'wb') as filPkl:
            pickle.dump(sclFit, filPkl)
    else:
        #--- we need to load the pkl file
        strScalerPath = m_kstrModelPath + "std_scaler_colab.pkl"
        print("WARN (lib.model.fit_stdScalar)  Using colab pkl for Test: ", strScalerPath)
        with open(strScalerPath, 'rb') as filPkl:
            sclFit = pickle.load(filPkl)
    return sclFit



def fit_txfStdScaler(pdfData, blnIsTrain=False):
    from sklearn.preprocessing import StandardScaler
    sclFit = fit_stdScaler(pdfData, blnIsTrain)
    X_std = sclFit.transform(pdfData)
    return X_std


#--- Supervised:  Gradient Boost Classifier
def trainGBC(pdfData):
    mdlAnoms = GradientBoostingClassifier()
    mdlAnoms.fit(pdfData.values)
    saveGBC_toPkl(mdlAnoms)
    return mdlAnoms


def loadGBC_fromPkl():
    with open(m_kstrMdlPath_gbc, 'rb') as filPkl:
        # load using pickle de-serializer
        mdlAnoms = pickle.load(filPkl)
        #mdlAnoms = joblib.load(filPkl)

    #mdlAnoms = load(m_kstrMdlPath_gbt, 'rb')
    return mdlAnoms



def saveGBC_toPkl(mdlAnoms):
    with open(m_kstrMdlPath_gbc, 'wb') as filPkl:
        pickle.dump(mdlAnoms, filPkl)
    #dump(mdlAnoms, open(m_kstrMdlPath_gbt, 'wb'))
    return mdlAnoms



def predictGBC(npaData):
    #--- input:  numpy.ndarray of feature eng, and scaled data 
    mdlAnoms = loadGBC_fromPkl()
    npaPredict = mdlAnoms.predict(npaData)

    #--- AttributeError: 'GradientBoostingClassifier' object has no attribute '_loss'
    #--- version of scikit-learn?  Monika: ?.?.? ; Iain: 1.2.0

    #print("INFO (type.npaPredict):  ", type(npaPredict))
    print("INFO (npaPredict.shape):  ", npaPredict.shape)
    return npaPredict



#--- Supervised:  Logistic Regession
def loadLogR_fromPkl():
    with open(m_kstrMdlPath_lgr, 'rb') as filPkl:
        mdlAnoms = pickle.load(filPkl)
    return mdlAnoms


def predictLogR(npaData):
    #--- input:  numpy.ndarray of feature eng, and scaled data 
    mdlAnoms = loadLogR_fromPkl()
    npaPredict = mdlAnoms.predict(npaData)

    print("INFO (npaPredict.shape):  ", npaPredict.shape)
    return npaPredict



#--- Supervised:  Support Vector Machines
def loadSVM_fromPkl():
    with open(m_kstrMdlPath_svm, 'rb') as filPkl:
        mdlAnoms = pickle.load(filPkl)
    return mdlAnoms


def predictSVM(npaData):
    #--- input:  numpy.ndarray of feature eng, and scaled data 
    mdlAnoms = loadSVM_fromPkl()
    npaPredict = mdlAnoms.predict(npaData)

    print("INFO (npaPredict.shape):  ", npaPredict.shape)
    return npaPredict