# ToyMl model and Simple Flask App

Python code that creates a simple titanic model and deploys this in a Flask app

This Flask app uses almost exclusively server side rendering and as 
such all the functionality is editable from the Python code

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

* Set the app as the ```FLASK_APP``` environment variable 
```bash
export FLASK_APP=app.py
```
* Init the Database 
```bash
Flask db init
```
* Read ```models.py``` for Database tables and create the migration scripts 
```bash
Flask db migrate
```
* Update the Database from the migrations scripts 
```bash
Flask db upgrade
```
* Run the Flask app 
```bash
Flask run
```

## Using the App

Either go to localhost:5000 and submit data or use the following from the command line

```bash
curl --data-binary "@test.csv" --request POST http://localhost:5000/api/predict?api_key=api_key
```

## Building a Docker Container
From the project dir run:
```bash
docker build -t toyml:leastest . && docker run -p 5000:5000 --name ToyML toyml:leastest
```
to build and run the newly built container

## Possible Improvements

* Unit tests
* Flask Blueprints for Auth and Logging
* YAML Config Files
* Client Side Functionality (deliberately left out at the moment)


