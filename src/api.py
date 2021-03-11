import pandas as pd
import io
from process_data import process_training_data
from flask import request
from flask_login import login_required,current_user
import flask_login
import uuid

from models import User
from app import db

from app import app

# Load the model from config file
RF = app.config['RF']


@app.route('/api/ping')
@login_required
# Test API
def ping():
    return "Pong"

# Create the Model Predict Endpoint
# Use a command like
# curl --data-binary "@test.csv" --request POST http://localhost:5000/api/predict?api_key=api_key
@app.route('/api/predict', methods=['GET', 'POST'])
@login_required
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
        # model_results = app.config['Model'].predict(df_data_final.drop(['PassengerId'], axis=1))

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
