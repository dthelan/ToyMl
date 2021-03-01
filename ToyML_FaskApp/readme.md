#ToyMl model and Simple Flask App

Python code that creates a simple titanic model and deploys this in a simple flask app

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to by running
```bash
 pip install -r requirements.txt
```

## Files
Main files:
* ```src/build_model.py``` - Trains the model
* ```src/app.py``` - Flask app 

## Running the Code
To build the model run:
```bash
python build_model.py -m Basic_RF.joblib -t train.csv
```
Here the code is looking in the Data dir

To run the app
```bash
python app.py -m Basic_RF.joblib -p 5001
```

## Using the App

Either go to localhost:5001 and submit data or use the following from the command line

```bash
curl --data-binary "@test.csv" --request POST http://localhost:5001/predict
```

##Building a Docker Container
From the project dir run:
```bash
docker build -t toyml:leastest . && docker run -p 5001:5000 --name ToyML toyml:leastest
```
to build and run the newly built container