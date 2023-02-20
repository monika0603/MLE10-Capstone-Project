'''
    purpose:      
'''

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
import uvicorn


from lib import claims as libClaims, providers as libProviders
import lib.utils as libUtils
from lib.models import mdl_utils as libMdlUtils


#--- imported route handlers
from routes.api.rte_api import rteApi
from routes.qa.rte_qa import rteQa
from routes.qa.rte_claims import rteClaims
from routes.qa.rte_providers import rteProv


#--- fastAPI self doc descriptors
description = """
    Fourthbrain Capstone:  MLE10 Cohort
    
    The Healthcare Claims Anomaly API is provided to assist with

    ## Claims Analysis
    ## Supervised Provider Predictions - Anomaly Detection (XGBoost)
    ## Unsupervised Claim Predictions - Anomaly Detection (KMeans Cluster)

    You will be able to:
    * Analyze Claims data
    * Identify potential Provider Anomalies
    * Idenitfy potential Claim Anomalies
"""

app = FastAPI(
    title="App:  Healthcare Claims - Anomaly Detection",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Iain McKone",
        "email": "iain.mckone@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


#--- configure route handlers
app.include_router(rteApi, prefix="/api")
app.include_router(rteQa, prefix="/qa")
app.include_router(rteClaims, prefix="/claims")
app.include_router(rteProv, prefix="/providers")



m_kstrPath_templ = libUtils.pth_templ
m_templRef = Jinja2Templates(directory=str(m_kstrPath_templ))


def get_jinja2Templ(request: Request, pdfResults, strParamTitle, lngNumRecords, blnIsTrain=False, blnIsSample=False):
    lngNumRecords = min(lngNumRecords, libUtils.m_klngMaxRecords)
    if (blnIsTrain):  strParamTitle = strParamTitle + " - Training Data"
    if (not blnIsTrain):  strParamTitle = strParamTitle + " - Test Data"
    if (blnIsSample):  lngNumRecords = libUtils.m_klngSampleSize
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


#--- get main ui/ux entry point
@app.get('/')
def index():
    return {
        "message": "Landing page:  Capstone Healthcare Anomaly Detection"
    }



if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=48300, reload=True)
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
