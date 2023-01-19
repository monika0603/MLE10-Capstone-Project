FROM python:3.9-slim

RUN apt update && apt upgrade -y
RUN pip3 install -U pip setuptools wheel
#RUN pip3 install gunicorn uvloop httptools

COPY ./app /app
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 48300

CMD ["uvicorn", "main:api", "--host=0.0.0.0", "--reload"]

#--- use gunicorn to control uvicorn launch?

#--- docker build -t img_apiclaimanoms:0.1 .
#--- docker run -p 48300:8000 --name ctr_apiClaimAnoms img_apiclaimanoms:0.1

#--- ISSUE:  uvicorn bug does not allow ctl-C break of fastapi through terminal
#--- WORKAROUND:  you have to run a docker or docker compose kill cmd;  eg docker kill <ctr_name>
