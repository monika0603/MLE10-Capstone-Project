from fastapi import APIRouter


m_kstrFile = __file__
m_blnTraceOn = True


rteQa = APIRouter()


@rteQa.get('/')
@rteQa.get('/verif')
@rteQa.get('/valid')
def qa_entry():
    return {
        "message": "qa routing - For verification, validation"
    }
