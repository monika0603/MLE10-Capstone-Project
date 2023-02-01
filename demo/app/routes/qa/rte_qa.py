from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from pathlib import Path

import lib.model as mdlClaims
import lib.claims as libClaims
import lib.utils as libPaths

import pandas as pd

m_kstrPath_templ = libPaths.pth_templ
m_templRef = Jinja2Templates(directory=str(m_kstrPath_templ))
m_klngMaxRecords = 100
m_klngSampleSize = 25

rteQa = APIRouter()

def get_jinja2Templ(request: Request, pdfResults, strParamTitle, lngNumRecords, blnIsTrain=False, blnIsSample=False):
    lngNumRecords = min(lngNumRecords, m_klngMaxRecords)
    if (blnIsTrain):  strParamTitle = strParamTitle + " - Training Data"
    if (not blnIsTrain):  strParamTitle = strParamTitle + " - Test Data"
    if (blnIsSample):  lngNumRecords = m_klngSampleSize
    if (blnIsSample):  strParamTitle = strParamTitle + " - max " + str(lngNumRecords) + " sample rows)"

    pdfClaims = pdfResults.head(lngNumRecords)
    htmlClaims = pdfClaims.to_html(classes='table table-striped')
    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': strParamTitle,
                'paramDataframe': htmlClaims
            }
    result = m_templRef.TemplateResponse(kstrTempl, jsonContext)
    return result

@rteQa.get('/')
@rteQa.get('/verif')
@rteQa.get('/valid')
def qa_entry():
    return {
        "message": "qa routing - For verification, validation"
    }



#--- get claims data
def claims_loadData(request: Request, response: Response, blnIsTrain=False, blnIsSample=False, blnForceCsv=False):
 
    pdfClaims = libClaims.load_claims(blnIsTrain)
    lngNumRecords = m_klngMaxRecords
    strParamTitle = "Claims"

    return get_jinja2Templ(request, pdfClaims, strParamTitle, lngNumRecords, blnIsTrain, blnIsSample)



@rteQa.get('/claims/data/loadCsv/', response_class = HTMLResponse)
def claims_loadCsv(request: Request, response: Response):
    #--- forces a reload of csv's in case a refresh is required
    pdfClaims = libClaims.load_claims(False, True)
    pdfClaims = libClaims.load_claims(True, True)
    return claims_loadData(request, response, True,False)



@rteQa.get('/claims/data/train/', response_class = HTMLResponse)
def claims_loadTrainData(request: Request, response: Response, blnIsSample=False):
    return claims_loadData(request, response, True, blnIsSample)



@rteQa.get('/claims/data/train/sample', response_class = HTMLResponse)
def claims_loadTrainSample(request: Request, response: Response):
    return claims_loadTrainData(request, response, True)



@rteQa.get('/claims/data/test/', response_class = HTMLResponse)
def claims_loadTestData(request: Request, response: Response, blnIsSample=False):
    return claims_loadData(request, response, False, blnIsSample)



@rteQa.get('/claims/data/test/sample', response_class = HTMLResponse)
def claims_loadTestSample(request: Request, response: Response):
    return claims_loadTestData(request, response, True)



@rteQa.get('/claims/doFeatEng/', response_class = HTMLResponse)
def claims_featEng(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng = libClaims.do_featEng(pdfClaims, blnIsTrain)

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Feature Engineered Claims"

    return get_jinja2Templ(request, pdfFeatEng, strParamTitle, lngNumRecords, blnIsTrain, True)



@rteQa.get('/claims/doFeatEng/train', response_class = HTMLResponse)
def claims_featEngTrain(request: Request, response: Response):
    return claims_featEng(request, response, True)



@rteQa.get('/claims/doFeatEng/test', response_class = HTMLResponse)
def claims_featEngTest(request: Request, response: Response):
    return claims_featEng(request, response, False)



@rteQa.get('/claims/doStdScaling/', response_class = HTMLResponse)
def claims_stdScaling(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng = libClaims.do_featEng(pdfClaims, blnIsTrain)
    npaScaled = libClaims.do_stdScaler(pdfFeatEng, blnIsTrain)
    pdfScaled = libClaims.do_stdScaler_toPdf(npaScaled)

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Std Scaled Claims"
    return get_jinja2Templ(request, pdfScaled, strParamTitle, lngNumRecords, blnIsTrain, blnIsSample)



@rteQa.get('/claims/doStdScaling/train', response_class = HTMLResponse)
def claims_stdScalingTrain(request: Request, response: Response):
    return claims_stdScaling(request, response, True)



@rteQa.get('/claims/doStdScaling/test', response_class = HTMLResponse)
def claims_stdScalingTest(request: Request, response: Response):
    return claims_stdScaling(request, response, False)



@rteQa.get('/claims/predict/superv', response_class = HTMLResponse)
@rteQa.get('/claims/predict/gbc', response_class = HTMLResponse)
def predict_supervised_gbc(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfResults = libClaims.get_gbcPredict(pdfClaims)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Loaded Claims Predictions (Gradient Boosting Classifier)"

    return get_jinja2Templ(request, pdfResults, strParamTitle, lngNumRecords, False, True)



@rteQa.get('/claims/predict/lgr', response_class = HTMLResponse)
def predict_supervised_lgr(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfResults = libClaims.get_logrPredict(pdfClaims)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Loaded Claims Predictions (Logistic Regression)"

    return get_jinja2Templ(request, pdfResults, strParamTitle, lngNumRecords, False, True)



@rteQa.get('/claims/predict/svm', response_class = HTMLResponse)
def predict_supervised_svm(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfResults = libClaims.get_logrPredict(pdfClaims)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Loaded Claims Predictions (Support Vector Machines)"

    return get_jinja2Templ(request, pdfResults, strParamTitle, lngNumRecords, False, True)