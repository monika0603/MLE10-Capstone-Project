import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from pickle import load, dump

#--- default methods
def load():
    return loadXGB()

def train(pdfData):
    return trainXGB(pdfData)

def predict(pdfData):
    return predictXGB(pdfData)


#--- XGBoost
m_kstrMdlPath_gbt = '../model/gbt_model.pkl'
def trainXGB(pdfData):
    mdlAnoms = XGBoost()
    mdlAnoms.fit(pdfData.values)
    saveXGB(mdlAnoms)
    return mdlAnoms

def loadXGB():
    mdlAnoms = load(m_kstrMdlPath_gbt, 'rb')
    return mdlAnoms

def saveXGB(mdlAnoms):
    dump(mdlAnoms, open(m_kstrMdlPath_gbt, 'wb'))
    return mdlAnoms

def predictXGB(pdfData):
    mdlAnoms = loadXGB()
    serPredict = mdlAnoms.predict(pdfData.values)  #--- Q:  is this a data series?
    return serPredict
