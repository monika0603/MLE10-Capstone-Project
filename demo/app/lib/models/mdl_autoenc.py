import pandas as pd
import numpy as np
from sklearn.decomposition import PCA 
import lib.utils as libPaths
import pickle


m_kstrFile = __file__
m_kstrDataPath = libPaths.pth_data
m_kstrBinModelPath = libPaths.pth_binModels
m_kstrPcaModelPath = m_kstrBinModelPath + 'pca_unsuperv_colab.pkl'
m_kstrEncModelPath = m_kstrBinModelPath + 'enc_keras_seq/'


#--- Supervised:  autoencoder - Principal Component Analysis
def load_encFromKeras():
    from tensorflow import keras
    mdlAnoms = keras.models.load_model(m_kstrEncModelPath)
    return mdlAnoms


def load_pcaFromPkl():
    with open(m_kstrPcaModelPath, 'rb') as filPkl:
        # load using pickle de-serializer
        mdlAnoms = pickle.load(filPkl)
    return mdlAnoms


def save_encToKeras(mdlAnoms):
    mdlAnoms.save(m_kstrEncModelPath)



def predict(pdfScaled):
    
    #--- Pre:  Transforming train and test dataframes based on PCA
    mdlPCA = load_pcaFromPkl()         #--- this is a pre-fit model based on training
    npaPca = mdlPCA.transform(pdfScaled)
    print("INFO (" + m_kstrFile + ".predict)  npaPca.shape:  ", npaPca.shape)


    #--- predict on unseen data
    mdlEnc = load_encFromKeras()
    npaPredict = mdlEnc.predict(npaPca[:,:29])
    print("INFO (" + m_kstrFile + ".predict)  npaPredict.shape:  ", npaPredict.shape)
    #--- expected:  297, 29?
    return npaPredict
    

""" 
def train(pdfTrainData):
    mdlAnoms = PCA()                        #---- TODO:  this is Keras Sequential
    mdlAnoms.fit(pdfTrainData.values)
    save_encToKeras(mdlAnoms)
    return mdlAnoms """