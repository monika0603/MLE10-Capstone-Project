from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse


from lib import utils as libUtils, claims as libClaims
from lib.models import mdl_utils as libMdlUtils
import main as libMain

m_kstrFile = __file__
m_blnTraceOn = True

m_kstrPath_templ = libUtils.pth_templ


rteClaims = APIRouter()



#--- get claims data
def claims_loadData(request: Request, response: Response, blnIsTrain=False, blnIsSample=False, blnForceCsv=False):
 
    pdfClaims = libClaims.load_claims(blnIsTrain)
    lngNumRecords = libUtils.m_klngMaxRecords
    strParamTitle = "Claims"

    return libMain.get_jinja2Templ(request, pdfClaims, strParamTitle, lngNumRecords, blnIsTrain, blnIsSample)



@rteClaims.get('/data/loadCsv/', response_class = HTMLResponse)
def claims_loadCsv(request: Request, response: Response):
    #--- forces a reload of csv's in case a refresh is required
    pdfClaims = libClaims.load_claims(False, True)
    pdfClaims = libClaims.load_claims(True, True)
    return claims_loadData(request, response, True,False)



@rteClaims.get('/data/train/', response_class = HTMLResponse)
def claims_loadTrainData(request: Request, response: Response, blnIsSample=False):
    return claims_loadData(request, response, True, blnIsSample)



@rteClaims.get('/data/train/sample', response_class = HTMLResponse)
def claims_loadTrainSample(request: Request, response: Response):
    return claims_loadTrainData(request, response, True)



@rteClaims.get('/data/test/', response_class = HTMLResponse)
def claims_loadTestData(request: Request, response: Response, blnIsSample=False):
    return claims_loadData(request, response, False, blnIsSample)



@rteClaims.get('/data/test/sample', response_class = HTMLResponse)
def claims_loadTestSample(request: Request, response: Response):
    return claims_loadTestData(request, response, True)



@rteClaims.get('/doStdScaling/', response_class = HTMLResponse)
def claims_stdScaling(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng = libClaims.do_featEng(pdfClaims, blnIsTrain, False)
    npaScaled = libMdlUtils.doClaims_stdScaler(pdfFeatEng, blnIsTrain)
    pdfScaled = libMdlUtils.doClaims_stdScaler_toPdf(npaScaled)

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Std Scaled Claims"
    return libUtils.get_jinja2Templ(request, pdfScaled, strParamTitle, lngNumRecords, blnIsTrain, blnIsSample)



@rteClaims.get('/doStdScaling/train', response_class = HTMLResponse)
def claims_stdScalingTrain(request: Request, response: Response):
    return claims_stdScaling(request, response, True)



@rteClaims.get('/doStdScaling/test', response_class = HTMLResponse)
def claims_stdScalingTest(request: Request, response: Response):
    return claims_stdScaling(request, response, False)



@rteClaims.get('/doFeatEng/', response_class = HTMLResponse)
def claims_doFeatEng(request: Request, response: Response, blnIsTrain=False):
    pdfClaims = libClaims.load_claims(blnIsTrain)
    pdfFeatEng_claims = libClaims.do_featEng(pdfClaims, blnIsTrain)

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = True

    strParamTitle = "Feature Engineered Claims"

    return libUtils.get_jinja2Templ(request, pdfFeatEng_claims, strParamTitle, 
                                    lngNumRecords, blnIsTrain, True)



@rteClaims.get('/predict/kmeans', response_class = HTMLResponse)
def predict_kmeans(request: Request, response: Response):
    
    #--- load test data, perform featEng, stdScaling, and fit to Kmeans args
    pdfClaims = libClaims.load_claims(False)
    print("TRACE: claims.predict.kmeans getting prediction ...")
    pdfResults = libClaims.get_kmeansPredict(pdfClaims)
    print("TRACE: claims.predict.kmeans prepping response ...")

    lngNumRecords = libUtils.m_klngMaxRecords
    blnIsSample = False
    strParamTitle = "Predictions (KMeans Clusters)"

    return libUtils.get_jinja2Templ(request, pdfResults, strParamTitle, 
                                    lngNumRecords, False, blnIsSample)



@rteClaims.get('/fit/kmeans', response_class = HTMLResponse)
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