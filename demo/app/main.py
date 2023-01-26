'''
    purpose:      
'''

from fastapi import FastAPI
import uvicorn


#--- imported route handlers
from routes.qa.rte_qa import rteQa                  #--- for testing
from routes.api.rte_api import rteApi               #--- for web services
from routes.uix.rte_claims import rteClaims         #--- for streamlit UI


#--- fastAPI self doc descriptors
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

app = FastAPI(
    title="App:  Healthcare Claims Anomaly Detection",
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


app.include_router(rteQa, prefix="/qa")


#print("INFO (basePath):  ", kstrBasePath)

#--- get main ui/ux entry point
@app.get('/')
def index():
    return {
        "message": "Hello World2"
    }



if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=48300, reload=True)
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
