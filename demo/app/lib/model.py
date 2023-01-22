import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib
#from pickle import load, dump
from pathlib import Path
import pickle


kstrBasePath = Path(__file__).resolve().parent.parent
kstrMdlPath = str(kstrBasePath / "model/")


#--- default methods
def load():
    return loadGBC_fromPkl()

def train(pdfData):
    return trainGBC(pdfData)

def predict(npaData):
    return predictGBC(npaData)


#--- Supervised:  Gradient Boost Classifier
m_kstrMdlPath_gbc = kstrMdlPath + '/gbc_model.pkl'
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
