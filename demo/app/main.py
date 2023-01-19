import fastapi
import uvicorn
import model as mdlClaims


api = fastapi.FastAPI()

@api.get('/')
def index():
    return {
        "message": "Hello World"
    }

@api.get('/claims/predict/')
def model_predict():
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
    uvicorn.run(api)
