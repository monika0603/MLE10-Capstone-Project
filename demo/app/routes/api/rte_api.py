from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

#from fastapi.templating import Jinja2Templates
from pathlib import Path

import lib.claims as libClaims

import pandas as pd

kstrPath_api = Path(__file__).resolve().parent
kstrPath_appRoot = kstrPath_api.parent.parent
#templRef = Jinja2Templates(directory=str(kstrPath_appRoot / "templ"))

rteApi = APIRouter()