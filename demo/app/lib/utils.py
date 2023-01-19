import pandas as pd
#from sklearn.ensemble import XGBoost
#from pickle import dump, load


#--- load the pandas dataframe from csv
def readData(filePath):
    pdfData = pd.read_csv(filePath, encoding='unicode_escape')

    #--- we can perform any other pre/post processing here
    return pdfData






