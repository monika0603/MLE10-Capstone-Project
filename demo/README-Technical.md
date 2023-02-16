# MLE10-Capstone-Project:  Demo App


## Table of Contents
1.  Background
2.  Overview
3.  How to run the demo
4.  How to deploy
5.  How to build
6.  Roadmap




## Section 1:  Background
Healthcare fraud is an expensive white-collar crime in the US and leads to an 
increase in healthcare premiums, and a reduction in quality and access to care.  
The National Health Care Anti-Fraud Association1 conservatively estimates that 
about 3 percent of US healthcare spending is lost to fraud per year ($300 
billion approximately). 



## Section 2:  Overview
To illustrate the capabilities of Machine Learning to identify claims anomalies, 
this capstone project team has developed two demonstrable solutions:   
- a supervised XGradient Boost Model to identify potential anomalies at the 
  provider level 
- an unsupervised KMeans Clustering Model to identify potential anomalies at 
  the claim level 

These solutions are hosted on Amazon EC2 utilizing a Streamlit front end for 
illustration.  Fast API endpoints are in final development to expose the model 
for on-demand supervised and unsupervised predictions.



## Section 3:  How to run the demo
### 3.1     AWS EC2:        ec2-18-205-247-232.compute-1.amazonaws.com
- Streamlit:    http://ec2-52-87-139-44.compute-1.amazonaws.com:58080
- FastAPI:      http://ec2-52-87-139-44.compute-1.amazonaws.com:58081/docs


### 3.2     Local env:      
- Streamlit:    http://localhost:48400
- FastAPI:      http://localhost:48300/docs



## Section 4:  How to deploy
### 4.1     EC2:  Manual Method
- ssh:          ssh -i "capstone-mle10-imckone.pem" ec2-user@ec2-52-87-139-44.compute-1.amazonaws.com
- conda:        conda activate env_capstone
- git:          cd mle10*/demo/app
                git pull capstone ftr_demo
- tmux:         tmux a -t demo_streamlit
                tmux a -t demo_fastapi
- streamlit:    streamlit run lit_index.py --server.port 58080
- fastapi:      uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 58081


### 4.2     Local env:      (from demo/app)
- streamlit:    streamlit run lit_index.py --server.port 48400
- fastAPI:      uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 48300



## Section 5:  How to build
### 5.1     EC2 Environ:
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

### 5.2     Local Dev Environment
- conda:        -- same as EC2 --
- pip:          -- same as EC2 --
- git:          -- same as EC2 --


### 5.3     Docker Image
- build:        docker build -t img_apiclaimanoms:demo .
- run:          docker run -p 48300:8000 --name ctr_apiClaimAnoms img_apiclaimanoms:demo



## Section 6:  Roadmap
- model:        finalize variational auto-encoder
- streamlit:    provide more visuals outlining the supervised and unsupervised features of interest
- fastapi:      expose the models to request/response model
                expose a claims data file check routine
                host fastapi on a seperate EC2 instance
- model serve:  consider model serving options and implement