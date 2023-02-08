from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

import main as libMain
from lib import utils as libUtils, claims as libClaims, providers as libProviders
from lib.models import mdl_utils as libMdlUtils



m_kstrFile = __file__
m_blnTraceOn = True

m_kstrPath_templ = libUtils.pth_templ
m_templRef = Jinja2Templates(directory=str(m_kstrPath_templ))


rteProv = APIRouter()



#--- get claims data
def providers_loadData(request: Request, response: Response, blnIsTrain=False, blnIsSample=False):
 
    pdfProviders = libProviders.load_providers(blnIsTrain)

    lngNumRecords = libUtils.m_klngMaxRecords
    strParamTitle = "Providers"

    return libMain.get_jinja2Templ(request, pdfProviders, strParamTitle, lngNumRecords, blnIsTrain, blnIsSample)



@rteProv.get('/data/train/', response_class = HTMLResponse)
def providers_loadTrainData(request: Request, response: Response, blnIsSample=False):
    return providers_loadData(request, response, True, blnIsSample)



@rteProv.get('/data/train/sample', response_class = HTMLResponse)
def providers_loadTrainSample(request: Request, response: Response):
    return providers_loadTrainData(request, response, True)



@rteProv.get('/data/test/', response_class = HTMLResponse)
def providers_loadTestData(request: Request, response: Response, blnIsSample=False):
    return providers_loadData(request, response, False, blnIsSample)



@rteProv.get('/data/test/sample', response_class = HTMLResponse)
def providers_loadTestSample(request: Request, response: Response):
    return providers_loadTestData(request, response, True)



@rteProv.get('/doFeatEng/', response_class = HTMLResponse)
def providers_featEng(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng_claims = libClaims.do_featEng(pdfClaims, blnIsTrain)
    pdfFeatEng_providers = libProviders.do_featEng(pdfFeatEng_claims)

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Feature Engineered Claims Grouped by Provider"

    return libMain.get_jinja2Templ(request, pdfFeatEng_providers, strParamTitle, 
                                    lngNumRecords, blnIsTrain, True)



@rteProv.get('/doFeatEng/train', response_class = HTMLResponse)
def providers_featEngTrain(request: Request, response: Response):
    return providers_featEng(request, response, True)



@rteProv.get('/doFeatEng/test', response_class = HTMLResponse)
def providers_featEngTest(request: Request, response: Response):
    return providers_featEng(request, response, False)



@rteProv.get('/doStdScaling/', response_class = HTMLResponse)
def providers_stdScaling(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng = libClaims.do_featEng(pdfClaims, blnIsTrain)
    npaScaled = libMdlUtils.doProviders_stdScaler(pdfFeatEng, blnIsTrain)
    pdfScaled = libMdlUtils.doProviders_stdScaler_toPdf(npaScaled)

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Std Scaled Claims Grouped by Provider"
    return libMain.get_jinja2Templ(request, pdfScaled, strParamTitle, 
                                lngNumRecords, blnIsTrain, blnIsSample)



@rteProv.get('/doStdScaling/train', response_class = HTMLResponse)
def providers_stdScalingTrain(request: Request, response: Response):
    return providers_stdScaling(request, response, True)



@rteProv.get('/doStdScaling/test', response_class = HTMLResponse)
def providers_stdScalingTest(request: Request, response: Response):
    return providers_stdScaling(request, response, False)



@rteProv.get('/predict/superv', response_class = HTMLResponse)
@rteProv.get('/predict/xgb', response_class = HTMLResponse)
def predict_supervised_xgb(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfResults = libProviders.get_xgbPredict(pdfFeatEng)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Provider Predictions (Gradient Boosting Classifier)"

    return libMain.get_jinja2Templ(request, pdfResults, strParamTitle, 
                                lngNumRecords, False, blnIsSample)



@rteProv.get('/predict/logr', response_class = HTMLResponse)
def predict_supervised_logr(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfResults = libProviders.get_logrPredict(pdfFeatEng)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Provider Predictions (Logistic Regression)"

    return libMain.get_jinja2Templ(request, pdfResults, strParamTitle, 
                            lngNumRecords, False, blnIsSample)



@rteProv.get('/predict/svm', response_class = HTMLResponse)
def predict_supervised_svm(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfResults = libProviders.get_svmPredict(pdfFeatEng)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Provider Predictions (Support Vector Machines)"

    return libMain.get_jinja2Templ(request, pdfResults, strParamTitle, 
                            lngNumRecords, False, blnIsSample)



@rteProv.get('/predict/enc', response_class = HTMLResponse)
def predict_kerasSeq(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfResults = libProviders.get_encPredict(pdfFeatEng)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Claims Predictions (Transformer/Encoder - Keras Sequential)"

    return libMain.get_jinja2Templ(request, pdfResults, strParamTitle, 
                                lngNumRecords, False, blnIsSample)
