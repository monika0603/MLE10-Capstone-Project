from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

#from IPython.display import HTML
import uvicorn
import lib.model as mdlClaims
import lib.claims as libClaims

import pandas as pd
#import json
#import os

from pathlib import Path

kstrBasePath = Path(__file__).resolve().parent
templRef = Jinja2Templates(directory=str(kstrBasePath / "templ"))


description = """
    Fourthbrain Capstone:  MLE10 Cohort
    
    The Healthcare Claims Anomaly API is provided to assist with

    ## Insurance Claims Analysis


    You will be able to:

    * **Create users** (_not implemented_).
    * **Read users** (_not implemented_).
    * Analyze Claims data
    * Identify potential Anomalies
"""

api = FastAPI(
    title="Api:  Healthcare Claims Anomaly Detection",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "AnnC, IainM, MonikaS",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


#print("INFO (basePath):  ", kstrBasePath)

#--- get main ui/ux entry point
@api.get('/')
def index():
    return {
        "message": "Hello World2"
    }


@api.get('/api/claims/predict/superv', response_class = HTMLResponse)
@api.get('/api/claims/predict/xgb', response_class = HTMLResponse)
def predict_supervised_xgb(request: Request, response: Response):
    #--- load test data
    pdfClaims = libClaims.loadPkl_testClaims()
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    npaScaled = libClaims.do_stdScaler(pdfFeatEng)

    ndaPredict = mdlClaims.predict(npaScaled)
    pdfPredict = pd.DataFrame(ndaPredict)

    htmlSample = pdfPredict.sample(10).to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Loaded Claims Predictions (Gradient Boosting Classifier)",
                'paramDataframe': htmlSample}

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result



@api.get('/test/')
def tst_harness():
    return {
        "message": "For verification, validation"
    }


#--- get claims data; test; train; predict
@api.get('/test/claims/train/')
def get_claims_train():
    #--- load raw csv(s)
    #--- return json
    #--- save as pandas data frame?
    return {
        "message": "get claims train data"
    }


@api.get('/test/claims/loadCsv/', response_class = HTMLResponse)
def tst_claims_loadedCsv(request: Request, response: Response):
    pdfClaims = libClaims.loadCsv_testClaims()
    pdfSample = pdfClaims.sample(10)
    htmlSample = pdfSample.to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Loaded Claims - Test Data (merged sample csv)",
                'paramDataframe': htmlSample}

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result


@api.get('/test/claims/loadPkl/', response_class = HTMLResponse)
def tst_claims_loadedPkl(request: Request, response: Response):
    pdfClaims = libClaims.loadPkl_testClaims()
    htmlSample = pdfClaims.sample(10).to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Loaded Claims - Test Data (merged sample pkl)",
                'paramDataframe': htmlSample}

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result


@api.get('/test/claims/doFeatEng/', response_class = HTMLResponse)
def tst_claims_featEng(request: Request, response: Response):
    pdfClaims = libClaims.loadPkl_testClaims()
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    htmlSample = pdfFeatEng.sample(10).to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Feature Engineered Claims - Test Data (sample)",
                'paramDataframe': htmlSample}

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result


@api.get('/test/claims/doStdScaling/', response_class = HTMLResponse)
def tst_claims_stdScaling(request: Request, response: Response):
    pdfClaims = libClaims.loadPkl_testClaims()
    pdfFeatEng = libClaims.do_featEng(pdfClaims)
    pdfScaled = libClaims.do_stdScaler_toPdf(pdfFeatEng)

    htmlSample = pdfScaled.sample(10).to_html(classes='table table-striped')

    kstrTempl = 'templ_showDataframe.html'
    jsonContext = {'request': request, 
                'paramTitle': "Scaled Claims - Test Data (sample)",
                'paramDataframe': htmlSample}

    result = templRef.TemplateResponse(kstrTempl, jsonContext)
    return result


if __name__ == '__main__':
    uvicorn.run("main:api", host="0.0.0.0", port=48300, reload=True)
#CMD ["uvicorn", "main:api", "--host=0.0.0.0", "--reload"]
