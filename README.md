# openapi-ui

The purpose of this project is to provide a FastAPI based OpenAPI SDK generator that allows generate SDK code in any language in seconds by providing the openapi specification, at some point the project will also offer a UI but at this point it is only the API that allows you to easily integrate the project in your CI/CD pipeline.

## Building and running the API

 These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Step 1:Clone the repository
     git clone https://github.com/grmono/openapi-ui.git
### step 2:Navigate to the clone 
     cd your_path/openapi-ui
### Step 3: Install python3 and dependencies:
     sudo apt install python3 python3-pip
### Step 4:
    pip3 install -r requirements.txt
### Step 5:
     cd app
### Step 6:
    python3 main.py
### Step 7:
     Visit localhost:8000/docs with your browser

## Docker Integration
Docker integration is already supported and allows you to use the solutions via docker compose
