from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import lib.claims as libClaims
import lib.providers as libProviders
import lib.utils as libPaths
from lib.models import mdl_utils as libMdlUtils

import pandas as pd

m_kstrFile = __file__
m_blnTraceOn = True

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
    strParamTitle = strParamTitle + " - max " + str(lngNumRecords) + " rows"

    pdfClaims = pdfResults.sample(lngNumRecords)
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



@rteQa.get('/providers/doFeatEng/', response_class = HTMLResponse)
def providers_featEng(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng_claims = libClaims.do_featEng(pdfClaims, blnIsTrain)
    pdfFeatEng_providers = libProviders.do_featEng(pdfFeatEng_claims)

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Feature Engineered Claims Grouped by Provider"

    return get_jinja2Templ(request, pdfFeatEng_providers, strParamTitle, lngNumRecords, blnIsTrain, True)



@rteQa.get('/providers/doFeatEng/train', response_class = HTMLResponse)
def providers_featEngTrain(request: Request, response: Response):
    return providers_featEng(request, response, True)



@rteQa.get('/providers/doFeatEng/test', response_class = HTMLResponse)
def providers_featEngTest(request: Request, response: Response):
    return providers_featEng(request, response, False)



@rteQa.get('/providers/doStdScaling/', response_class = HTMLResponse)
def providers_stdScaling(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng = libClaims.do_featEng(pdfClaims, blnIsTrain)
    npaScaled = libMdlUtils.doProviders_stdScaler(pdfFeatEng, blnIsTrain)
    pdfScaled = libMdlUtils.doProviders_stdScaler_toPdf(npaScaled)

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Std Scaled Claims Grouped by Provider"
    return get_jinja2Templ(request, pdfScaled, strParamTitle, lngNumRecords, blnIsTrain, blnIsSample)



@rteQa.get('/providers/doStdScaling/train', response_class = HTMLResponse)
def providers_stdScalingTrain(request: Request, response: Response):
    return providers_stdScaling(request, response, True)



@rteQa.get('/providers/doStdScaling/test', response_class = HTMLResponse)
def providers_stdScalingTest(request: Request, response: Response):
    return providers_stdScaling(request, response, False)



@rteQa.get('/claims/doStdScaling/', response_class = HTMLResponse)
def claims_stdScaling(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng = libClaims.do_featEng(pdfClaims, blnIsTrain, False)
    npaScaled = libMdlUtils.doClaims_stdScaler(pdfFeatEng, blnIsTrain)
    pdfScaled = libMdlUtils.doClaims_stdScaler_toPdf(npaScaled)

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



@rteQa.get('/claims/doFeatEng/', response_class = HTMLResponse)
def claims_doFeatEng(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng_claims = libClaims.do_featEng(pdfClaims, blnIsTrain)

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Feature Engineered Claims"

    return get_jinja2Templ(request, pdfFeatEng_claims, strParamTitle, lngNumRecords, blnIsTrain, True)



@rteQa.get('/providers/predict/superv', response_class = HTMLResponse)
@rteQa.get('/providers/predict/xgb', response_class = HTMLResponse)
def predict_supervised_xgb(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfResults = libProviders.get_xgbPredict(pdfFeatEng)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Provider Predictions (Gradient Boosting Classifier)"

    return get_jinja2Templ(request, pdfResults, strParamTitle, lngNumRecords, False, blnIsSample)



@rteQa.get('/providers/predict/logr', response_class = HTMLResponse)
def predict_supervised_logr(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfResults = libProviders.get_logrPredict(pdfFeatEng)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Provider Predictions (Logistic Regression)"

    return get_jinja2Templ(request, pdfResults, strParamTitle, lngNumRecords, False, blnIsSample)



@rteQa.get('/providers/predict/svm', response_class = HTMLResponse)
def predict_supervised_svm(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfResults = libProviders.get_svmPredict(pdfFeatEng)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Provider Predictions (Support Vector Machines)"

    return get_jinja2Templ(request, pdfResults, strParamTitle, lngNumRecords, False, blnIsSample)



@rteQa.get('/providers/predict/enc', response_class = HTMLResponse)
def predict_kerasSeq(request: Request, response: Response):
    
    #--- load test data
    #--- filter to only those rows that are flagged with an anomaly
    pdfClaims = libClaims.load_claims(False)
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfResults = libProviders.get_encPredict(pdfFeatEng)
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    lngNumRecords = m_klngMaxRecords
    blnIsSample = True
    strParamTitle = "Claims Predictions (Transformer/Encoder - Keras Sequential)"

    return get_jinja2Templ(request, pdfResults, strParamTitle, lngNumRecords, False, blnIsSample)


@rteQa.get('/claims/predict/kmeans', response_class = HTMLResponse)
def predict_kmeans(request: Request, response: Response):
    
    #--- load test data, perform featEng, stdScaling, and fit to Kmeans args
    pdfClaims = libClaims.load_claims(False)
    print("TRACE: claims.predict.kmeans getting prediction ...")
    pdfResults = libClaims.get_kmeansPredict(pdfClaims)
    print("TRACE: claims.predict.kmeans prepping response ...")

    lngNumRecords = m_klngMaxRecords
    blnIsSample = False
    strParamTitle = "Predictions (KMeans Clusters)"

    return get_jinja2Templ(request, pdfResults, strParamTitle, lngNumRecords, False, blnIsSample)



@rteQa.get('/claims/fit/kmeans', response_class = HTMLResponse)
def fit_kmeans(request: Request, response: Response):
    
    #--- load test data, perform featEng, stdScaling, and fit to Kmeans args
    pdfClaims = libClaims.load_claims(False)
    mdlKMeans = libClaims.get_kmeansFit(pdfClaims)

    #--- inspect KMeans data;  clusters, centers, sizes
    #lstCenters = mdlKMeans.cluster_centers_
    lstIdx = range(len(mdlKMeans.cluster_centers_))
    if (m_blnTraceOn): print("TRACE (" + m_kstrFile + ".fit_kmeans)  lstIdx: ", lstIdx)

    lstSize = [sum(mdlKMeans.labels_ == idx) for idx,_ in enumerate(lstIdx)]
    if (m_blnTraceOn): print("TRACE (" + m_kstrFile + ".fit_kmeans)  lstSize: ", lstSize)

    return