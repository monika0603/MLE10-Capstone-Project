# MLE10-Capstone-Project:  Demo App

    #--- Table of Contents
    1.  Overview
    2.  Background
    3.  How to run the demo
    4.  How to deploy
    5.  How to build
    6.  How to dev, update
    7.  Prereqs, dependencies



    Section 1:  Overview



    Section 2:  Background



    Section 3:  How to run the demo
        3.1     AWS EC2:        
                - Streamlit:    http://ec2-44-201-155-7.compute-1.amazonaws.com:58080
                - FastAPI:      http://ec2-44-201-155-7.compute-1.amazonaws.com:58081/docs

        3.2     Local env:      
              - Streamlit:      http://localhost:48400
                - FastAPI:      http://localhost:48300/docs



    Section 4:  How to deploy
        4.1     EC2:  Manual Method
                - ssh:          ssh -i "capstone-mle10-imckone.pem" ec2-user@ec2-44-201-155-7.compute-1.amazonaws.com
                - conda:        conda activate env_capstone
                - git:          cd mle10*/demo/app
                                git pull capstone ftr_demo
                - tmux:         tmux a -t demo_streamlit
                                tmux a -t demo_fastapi
                - streamlit:    streamlit run lit_index.py --server.port 58080
                - fastapi:      uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 58081

        4.2     Local env:      (from dev/app)
                - streamlit:      streamlit run lit_index.py --server.port 48400
                - fastAPI:        uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 48300



    Section 5:  How to build
        5.1     EC2 Environ:
                - conda:        conda create --name env_capstone python=3.8.16
                                conda activate env_capstone
                - pip:          pip install -r requirements.txt
                - git:          mkdir mle10-capstone
                                cd mle10*
                                git init
                                git config core.sparsecheckout true
                                echo demo/ >> .git/info/sparse-checkout
                                git remote add -f capstone https://github.com/monika0603/MLE10-Capstone-Project.git
                                git pull capstone ftr_demo
                - tmux:         tmux new -s demo_streamlit
                                tmux new -s demo_fastapi

        5.2     Local Dev Environment
        5.3     Docker Image


    Section 6:  How to dev, update

    
    Section 7:  Prereqs, dependencies


#--- prereqs:  local development
- install miniconda
    - conda install pandas matplotlib ipykernel 
    - pip install sklearn scikit-learn fastapi uvicorn
- pip list --format=freeze > env_capstone_py3.10.8.txt

- how to run fast api:
    - demo/app/uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 48300

- how to run streamlit:
    - demo/app/streamlit run lit_index.py --server.port 48400

#--- AWS prereqs
- ssh into AWS ec2
- install miniconda
    - wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
    - bash ~/miniconda.sh -b -p ~/miniconda
    - echo "PATH=$PATH:$HOME/miniconda/bin" >> ~/.bashrc
    - source ~/.bashrc
    - restart shell
    - conda update conda
    - rm miniconda.sh
    - conda install wget
- create conda env
    - conda create --name prod_capstone python=3.10.8
    - conda activate prod_capstone
- setup env
    - sudo yum update -y
    - sudo yum install git -y    
    - sudo yum install tmux
- clone repo
    - git clone https://github.com/monika0603/MLE10-Capstone-Project.git
    - git checkout ftr_demo
- set up prereqs
    - pip install -U pip
    - pip install -r prod_capstone_py3.10.8.txt
- run tmux  
    - tmux new -s demo_streamlit
    - tmux new -s demo_fastapi
    - tmux a -t <session>              #--- to attach to an existing session



#--- AWS Instance
name:   capstone-mle10-healthcare-claim-anomalies
ssh:    port 58022
https:  port 58443
http:   port 58080 streamlit
http:   port 58081 fastapi
ssh -i "capstone-mle10-imckone.pem" ec2-user@ec2-44-201-155-7.compute-1.amazonaws.com

    runtime ERRORS:
        - streamlit websocket timeout, firewall block?
            - attempt#1 (did not work):  sed -i -e 's/,1e3/,1e4/g' -e 's/,500/,10000/g' ~/miniconda3/envs/prod_capstone/lib/python3.10/site-packages/streamlit/static/static/js/main.3c7e5310.chunk.js
            - attempt#2:  modify MESSAGE_SIZE_LIMIT var in server_utils.py (here: .\venv\Lib\site-packages\streamlit\server\server_util.py). By default this is 50MB; to 500MB
            - attempt#3:  increase "websocket_ping_timeout": 30, in the TORNADO_SETTINGS dictionary located in lib\site-packages\streamlit\server\server.py; from 30 seconds to 200s


#--- docker commands (local)
docker build -t img_apiclaimanoms:dev .
docker run -p 48300:8000 --name ctr_apiClaimAnoms img_apiclaimanoms:dev


#--- docker commands (publish)
docker save <image:tag> > my_image.tar
docker load my_image.tar