import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import lib.utils as libPaths
import pickle


m_kstrFile = __file__
m_kstrDataPath = libPaths.pth_data
m_kstrBinModelPath = libPaths.pth_binModels
m_kstrModelPath = m_kstrBinModelPath + 'gbc_model_colab.pkl'


#--- Supervised:  xg boost;  gradient boosting classifier
def load_fromPkl():
    with open(m_kstrModelPath, 'rb') as filPkl:
        mdlAnoms = pickle.load(filPkl)
    return mdlAnoms



def save_toPkl(mdlAnoms):
    with open(m_kstrModelPath, 'wb') as filPkl:
        pickle.dump(mdlAnoms, filPkl)
    return mdlAnoms



def predict(npaData):
    #--- input:  numpy.ndarray of feature eng, and scaled data 
    mdlAnoms = load_fromPkl()
    npaPredict = mdlAnoms.predict(npaData)

    #--- AttributeError: 'GradientBoostingClassifier' object has no attribute '_loss'
    #--- version of scikit-learn?  Monika: ?.?.? ; Iain: 1.2.0

    #print("INFO (type.npaPredict):  ", type(npaPredict))
    print("INFO (npaPredict.shape):  ", npaPredict.shape)
    return npaPredict


def train(pdfTrainData):
    mdlAnoms = GradientBoostingClassifier()
    mdlAnoms.fit(pdfTrainData.values)
    save_toPkl(mdlAnoms)
    return mdlAnoms
