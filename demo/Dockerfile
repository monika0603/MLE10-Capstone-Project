#FROM python:3.9-slim
FROM python:3.10.9-slim-bullseye

#RUN apt update && apt upgrade -y
#RUN pip3 install -U pip setuptools wheel
#RUN pip3 install gunicorn uvloop httptools

COPY ./app /app
COPY ./prod_capstone_py3.10.8.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r ./requirements.txt

EXPOSE 48300
#EXPOSE 48400

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
#CMD ["streamlit", "run", "lit_index.py", "--server.port=48400"]

#--- use gunicorn to control uvicorn launch?

#--- docker build -t img_apiclaimanoms:0.1 .
#--- docker run -p 48300:8000 --name ctr_apiClaimAnoms img_apiclaimanoms:0.1
#--- docker run -P --name ctr_apiClaimAnoms img_apiclaimanoms:0.1                   #--- open all ports defined by Docker EXPOSE

#--- ISSUE:  uvicorn bug does not allow ctl-C break of fastapi through terminal
#--- WORKAROUND:  you have to run a docker or docker compose kill cmd;  eg docker kill <ctr_name>



#---    Docker build log
#       from python:3.9-slim; with prod_reqs.txt            size:  3.54gb       time:  >700s
#       from python:3.10.9-slim-bullseye                    size:  3.53gb       time:  >1300s
#       from python:3.10.9-slim-buster                      size:  