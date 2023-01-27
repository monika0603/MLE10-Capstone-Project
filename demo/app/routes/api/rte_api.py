from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

import pandas as pd
import json

import lib.claims as libClaims
import lib.model as mdlClaims


rteApi = APIRouter()

#--- return json for claims data (merged)
#--- note:  current is kaggle, but future could include from yyyymm filter
@rteApi.get('/claims', response_class = JSONResponse)
def api_getClaims(request: Request, response: Response):
    pdfClaims = libClaims.loadPkl_testClaims()
    jsonSample = pdfClaims.head(50).to_json(orient="records", indent=4)
    result = json.loads(jsonSample)
    return result


#--- return json for featEng
@rteApi.get('/claims/doFeatEng/', response_class = JSONResponse)
def tst_claims_featEng():
    pdfClaims = libClaims.loadPkl_testClaims()
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    jsonSample = pdfClaims.head(50).to_json(orient="records", indent=4)
    result = json.loads(jsonSample)
    return result


@rteApi.get('/claims/doStdScaling/', response_class = JSONResponse)
def tst_claims_stdScaling():
    pdfClaims = libClaims.loadPkl_testClaims()
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfScaled = libClaims.do_stdScaler_toPdf(pdfFeatEng)

    jsonSample = pdfClaims.head(50).to_json(orient="records", indent=4)
    result = json.loads(jsonSample)
    return result


@rteApi.get('/claims/predict/superv', response_class = JSONResponse)
@rteApi.get('/claims/predict/gbc', response_class = JSONResponse)
def predict_supervised_gbc():
    #--- load test data
    pdfClaims = libClaims.loadPkl_testClaims()
    pdfFeatEng = libClaims.do_featEng(pdfClaims)

    npaScaled = libClaims.do_stdScaler(pdfFeatEng)
    pdfScaled = libClaims.do_stdScaler_toPdf(npaScaled)
  
    ndaPredict = mdlClaims.predict(npaScaled)
    pdfPredict = pd.DataFrame(ndaPredict)

    #--- stitch the grouped data with the labels
    pdfResults = pdfScaled.copy()
    pdfResults.insert(0, "hasAnom?", pdfPredict[0])

    #--- filter to only those rows that are flagged with an anomaly
    pdfResults = pdfResults[pdfResults['hasAnom?'] > 0] 

    jsonSample = pdfResults.head(50).to_json(orient="records", indent=4)
    result = json.loads(jsonSample)
    return result
