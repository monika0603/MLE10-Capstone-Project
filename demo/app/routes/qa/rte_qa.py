from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from pathlib import Path

import lib.model as mdlClaims
import lib.claims as libClaims

import pandas as pd

kstrPath_qa = Path(__file__).resolve().parent
kstrPath_appRoot = kstrPath_qa.parent.parent
templRef = Jinja2Templates(directory=str(kstrPath_appRoot / "templ"))

rteQa = APIRouter()


@rteQa.get('/')
@rteQa.get('/verif')
def qa_entry():
    return {
        "message": "For verification"
    }


@rteQa.get('/valid')
def qa_entry():
    return {
        "message": "For validation"
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

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result


#--- get claims data; test; train; predict
@rteQa.get('/claims/train/')
def get_claims_train():
    #--- load raw csv(s)
    #--- return json
    #--- save as pandas data frame?
    return {
        "message": "get claims train data"
    }


@rteQa.get('/claims/loadCsv/', response_class = HTMLResponse)
def tst_claims_loadedCsv(request: Request, response: Response):
    pdfClaims = libClaims.loadCsv_testClaims()
    pdfSample = pdfClaims.head(50)
    htmlSample = pdfSample.to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Loaded Claims - Test Data (merged sample csv)",
                'paramDataframe': htmlSample}

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result


@rteQa.get('/claims/loadPkl/', response_class = HTMLResponse)
def tst_claims_loadedPkl(request: Request, response: Response):
    pdfClaims = libClaims.loadPkl_testClaims()
    htmlSample = pdfClaims.head(50).to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Loaded Claims - Test Data (merged sample pkl)",
                'paramDataframe': htmlSample}

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result


@rteQa.get('/claims/doFeatEng/', response_class = HTMLResponse)
def tst_claims_featEng(request: Request, response: Response):
    pdfClaims = libClaims.loadPkl_testClaims()
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    htmlSample = pdfFeatEng.head(50).to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Feature Engineered Claims - Test Data (sample)",
                'paramDataframe': htmlSample}

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
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

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result