#--- purpose:  to train a model

from utils import readData, trainModel, plotLabels

if __name__ == "__main__":
    str_trainDataPath = "./data/train.csv"
    pdf_trainData = readData(str_trainDataPath)
    mdlAnoms = trainModel(pdf_trainData)
    pdf_trainData.loc[:,'labels'] = mdlAnoms.predict(pdf_trainData.values)