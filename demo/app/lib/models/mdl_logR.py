from sklearn.linear_model import LogisticRegressionCV
import lib.utils as libPaths
import pickle


m_kstrFile = __file__
m_kstrDataPath = libPaths.pth_data
m_kstrBinModelPath = libPaths.pth_binModels
m_kstrModelPath = m_kstrBinModelPath + 'lgr_model_colab.pkl'


#--- Supervised:  Logistic Regession
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

    print("INFO (npaPredict.shape):  ", npaPredict.shape)
    return npaPredict



def train(pdfTrainData):
    mdlAnoms = LogisticRegressionCV()
    mdlAnoms.fit(pdfTrainData.values)
    save_toPkl(mdlAnoms)
    return mdlAnoms