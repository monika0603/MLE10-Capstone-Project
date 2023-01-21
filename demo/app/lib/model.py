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
    return loadXGB_fromPkl()

def train(pdfData):
    return trainXGB(pdfData)

def predict(npaData):
    return predictXGB(npaData)


#--- XGBoost
m_kstrMdlPath_gbt = kstrMdlPath + '/gbt_model.pkl'
def trainXGB(pdfData):
    mdlAnoms = GradientBoostingClassifier()
    mdlAnoms.fit(pdfData.values)
    saveXGB_toPkl(mdlAnoms)
    return mdlAnoms

def loadXGB_fromPkl():
    with open(m_kstrMdlPath_gbt, 'rb') as filPkl:
        # load using pickle de-serializer
        #mdlAnoms = pickle.load(filPkl)
        mdlAnoms = joblib.load(filPkl)

    #mdlAnoms = load(m_kstrMdlPath_gbt, 'rb')
    return mdlAnoms

def saveXGB_toPkl(mdlAnoms):
    with open(m_kstrMdlPath_gbt, 'wb') as filPkl:
        pickle.dump(mdlAnoms, filPkl)
    #dump(mdlAnoms, open(m_kstrMdlPath_gbt, 'wb'))
    return mdlAnoms

def predictXGB(npaData):
    #--- input:  numpy.ndarray of feature eng, and scaled data 
    mdlAnoms = loadXGB_fromPkl()
    npaPredict = mdlAnoms.predict(npaData)

    #--- AttributeError: 'GradientBoostingClassifier' object has no attribute '_loss'
    #--- version of scikit-learn?  Monika: ?.?.? ; Iain: 1.2.0

    print("INFO (type.npaPredict):  ", type(npaPredict))
    return npaPredict
