from flask import Flask, request, render_template
from joblib import load
from config import Config
import pandas as pd
import io
import sys
import argparse
from process_data import process_training_data
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Define the app as a flask app
app = Flask(__name__)
# Import the config settings
app.config.from_object(Config)
# Set Debug as True to enable quick dev
app.config['DEBUG'] = True
# Add the DB to Flask App
db = SQLAlchemy(app)
# Link the App and DB for migrations
migrate = Migrate(app, db)

login = LoginManager(app)

import models

# Define an API end point
# This is a test to show the page is working
@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return render_template('index.html')


# Create the Model Predict Endpoint
# Use a command like
# curl --data-binary "@test.csv" --request POST http://localhost:5001/predict
@app.route('/predict', methods=['GET', 'POST'])
def prediction():
    # Define different end point for different request types
    # GET - A web page style request
    if request.method == 'GET':
        return "End point for generating predictions"

    # POST - An upload style request
    if request.method == 'POST':
        # Turn the post request into a DataFrame
        df_data_raw = pd.read_csv(io.BytesIO(request.get_data()), encoding="latin1")

        # We need to format this DataFrame like our training set
        df_data_final = process_training_data(df_data_raw, 'Test')

        # Use our model to predict new results
        model_results = RF.predict(df_data_final.drop(['PassengerId'], axis=1))

        # Add the model results to our data frame
        df_data_final['Survived'] = model_results

        # The current DataFrame is the transformed one,
        # we want results on the original

        # Take the IDs and results
        df_outcomes = df_data_final[['PassengerId', 'Survived']]

        # Merge results onto original DataFrame and drop created features
        df_final = df_data_raw.merge(df_outcomes, left_on=['PassengerId'],
                                     right_on=['PassengerId'], how='inner'). \
            drop(['Name Contains MR', 'Valid Cabin'], axis=1)

        # Transpose and return the DataFrame
        return df_final.to_csv(index=False)


# Python MAIN function, need to run the app in stand alone
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help='Port Number for Web Server')
    parser.add_argument('-m', help='Model to load, should be .joblib')
    args = parser.parse_args()

    # Check the loaded model has the correct format
    if args.m.split('.')[-1] != 'joblib':
        print('The model should be a joblib file')
        sys.exit()

    # Load are model
    RF = load('../models/' + args.m)

    # Run the Web App on http://localhost:port
    app.run(host='0.0.0.0', port=args.p)
