import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import lib.utils as libPaths
import pickle
import sys


m_kstrFile = __file__
m_kstrDataPath = libPaths.pth_data
m_kstrBinModelPath = libPaths.pth_binModels
m_kstrModelPath_gbc = m_kstrBinModelPath + 'gbc_model_colab.pkl'
m_kstrModelPath_prov111 = m_kstrBinModelPath + 'prov_gbc_v1.1.1_32cols.pkl'            #--- ERROR:  __randomstate_ctor() takes from 0 to 1 positional arguments but 2 were given
m_kstrModelPath_prov121 = m_kstrBinModelPath + 'prov_gbc_v1.2.1_32cols.pkl'
m_kstrModelPath_prov_py3816_sk111hp = m_kstrBinModelPath + 'prov_gbc_py3816_sk111hp_32cols.pkl'
m_kstrModelPath = m_kstrModelPath_prov_py3816_sk111hp

m_blnTraceOn = True



#--- Supervised:  xg boost;  gradient boosting classifier
def load_fromPkl():
    try:
        with open(m_kstrModelPath, 'rb') as filPkl:
            mdlAnoms = pickle.load(filPkl)
        return mdlAnoms

    except:
        e = sys.exc_info()
        print("ERROR (mdl_xgb.load_fromPkl_genError):  ", e)    



def save_toPkl(mdlAnoms):
    with open(m_kstrModelPath, 'wb') as filPkl:
        pickle.dump(mdlAnoms, filPkl)
    return mdlAnoms



def predict(npaData):

    try:
        #--- input:  numpy.ndarray of feature eng, and scaled data 
        mdlAnoms = load_fromPkl()
        if (m_blnTraceOn):  print("TRACE (mdl_xgb.predict):  data loaded ... ")
        npaPredict = mdlAnoms.predict(npaData)

    except:
        e = sys.exc_info()
        print("ERROR (mdl_xgb.predict_genError1):  ", e)  


    #--- AttributeError: 'GradientBoostingClassifier' object has no attribute '_loss'
    #--- version of scikit-learn?  Monika: ?.?.? ; Iain: 1.2.0

    #print("INFO (type.npaPredict):  ", type(npaPredict))
    #if (m_blnTraceOn):  print("TRACE (mdl_xgb.predict) npaPredict.shape:  ", npaPredict.shape)
    return npaPredict


def train(pdfTrainData):
    mdlAnoms = GradientBoostingClassifier()
    mdlAnoms.fit(pdfTrainData.values)
    save_toPkl(mdlAnoms)
    return mdlAnoms
