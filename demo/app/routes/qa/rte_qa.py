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


@rteQa.get('/')
@rteQa.get('/verif')
@rteQa.get('/valid')
def qa_entry():
    return {
        "message": "qa routing - For verification, validation"
    }


@rteQa.get('/claims/predict/superv', response_class = HTMLResponse)
@rteQa.get('/claims/predict/gbc', response_class = HTMLResponse)
def predict_supervised_gbc(request: Request, response: Response):
    #--- load test data
    pdfClaims = libClaims.loadPkl_testClaims()
    print("INFO (predict.pklClaims.shape):  ", pdfClaims.shape)

    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    print("INFO (predict.pdfFeatEng.shape):  ", pdfFeatEng.shape)

    npaScaled = libClaims.do_stdScaler(pdfFeatEng)
    pdfScaled = libClaims.do_stdScaler_toPdf(npaScaled)
    print("INFO (predict.npaScaled.shape):  ", npaScaled.shape)

    ndaPredict = mdlClaims.predict(npaScaled)
    print("INFO (predict.npaPredict.shape):  ", ndaPredict.shape)

    pdfPredict = pd.DataFrame(ndaPredict)
    print("INFO (predict.pdfPredict.shape):  ", pdfPredict.shape)

    #--- stitch the grouped data with the labels
    pdfResults = pdfScaled.copy()
    pdfResults.insert(0, "hasAnom?", pdfPredict[0])

    #--- filter to only those rows that are flagged with an anomaly
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    #htmlSample = pdfPredict.head(50).to_html(classes='table table-striped')
    htmlSample = pdfResults.head(50).to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Loaded Claims Predictions (Gradient Boosting Classifier)",
                'paramDataframe': htmlSample}

    result = m_templRef.TemplateResponse(kstrTempl, jsonContext)
    return result



#--- get claims data and/or samples
def claims_loadData(request: Request, response: Response, blnIsTrain=False, blnIsSample=False, blnForceCsv=False):
 
    pdfClaims = libClaims.load_claims(blnIsTrain)
    lngNumRecords = m_klngMaxRecords

    strParamTitle = "Claims - Test Data"
    if (blnIsTrain):  strParamTitle = "Claims - Training Data"
    if (blnIsSample):  lngNumRecords = m_klngSampleSize
        
    strParamTitle = strParamTitle + " (merged sample - top " + str(lngNumRecords) + " rows)"
    pdfClaims = pdfClaims.head(lngNumRecords)
    htmlClaims = pdfClaims.to_html(classes='table table-striped')
    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': strParamTitle,
                'paramDataframe': htmlClaims
            }
    result = m_templRef.TemplateResponse(kstrTempl, jsonContext)
    return result



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
def tst_claims_featEng(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Feature Engineered Claims - Test Data"
    if (blnIsTrain):  strParamTitle = "Feature Engineered Claims - Training Data"
    if (blnIsSample):  lngNumRecords = m_klngSampleSize
        
    htmlSample = pdfFeatEng.head(lngNumRecords).to_html(classes='table table-striped')
    strParamTitle = strParamTitle + " (sample - top " + str(lngNumRecords) + " rows)"
 
    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': strParamTitle,
                'paramDataframe': htmlSample}

    result = m_templRef.TemplateResponse(kstrTempl, jsonContext)
    return result


@rteQa.get('/claims/doStdScaling/', response_class = HTMLResponse)
def tst_claims_stdScaling(request: Request, response: Response):
    pdfClaims = libClaims.loadPkl_testClaims()
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfScaled = libClaims.do_stdScaler_toPdf(pdfFeatEng)

    htmlSample = pdfScaled.head(50).to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Scaled Claims - Test Data (sample)",
                'paramDataframe': htmlSample}

    result = m_templRef.TemplateResponse(kstrTempl, jsonContext)
    return result