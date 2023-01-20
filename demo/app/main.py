from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

#from IPython.display import HTML
import uvicorn
import lib.model as mdlClaims
import lib.claims as libClaims
#import pandas as pd
#import json
#import os

from pathlib import Path

api = FastAPI()
kstrBasePath = Path(__file__).resolve().parent
templRef = Jinja2Templates(directory=str(kstrBasePath / "templ"))

#print("INFO (basePath):  ", kstrBasePath)

#--- get main ui/ux entry point
@api.get('/')
def index():
    return {
        "message": "Hello World2"
    }

#--- get claims data; test; train; predict
@api.get('/claims/train/')
def get_claims_train():
    #--- load raw csv(s)
    #--- return json
    #--- save as pandas data frame?
    return {
        "message": "get claims train data"
    }

@api.get('/claims/test/')
@api.get('/claims/test/loadData/', response_class = HTMLResponse)
def get_claims_test(request: Request, response: Response):
    pdfClaims = libClaims.loadCsv_testData()
    pdfSample = pdfClaims.sample(10)
    htmlSample = pdfSample.to_html()

    context = {'request': request, 'dataframe': pdfSample.to_html(classes='table table-stripped')}
    result = templRef.TemplateResponse(
        'templ_showDataframe.html', context)

    return result

@api.get('/api/claims/predict/xgb')
def model_predict():
    #--- input:  json claims data
    return {
        "message": "Model prediction"
    }
    #mdlClaims.predict(pdfData)


@api.get('/test/')
def tst_harness():
    return {
        "message": "For verification, validation"
    }

if __name__ == '__main__':
    uvicorn.run("main:api", host="0.0.0.0", port=48300, reload=True)
#CMD ["uvicorn", "main:api", "--host=0.0.0.0", "--reload"]
