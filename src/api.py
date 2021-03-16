import pandas as pd
import io
from process_data import process_training_data
from flask import request
from flask_login import login_required

from app import app
from app import auth

# Load the model from config file
RF = app.config['RF']


# Test API
# curl -H "Authorization: Bearer <ACCESS_TOKEN>" --request POST http://localhost:5000/api/ping
@app.route('/api/ping')
@auth.login_required
def ping():
    return "Pong"


# Create the Model Predict Endpoint
# Use a command like
# curl -H "Authorization: Bearer <ACCESS_TOKEN>" --data-binary "@test.csv" --request POST http://localhost:5000/api/predict
@app.route('/api/predict', methods=['GET', 'POST'])
@auth.login_required
def prediction():
    # Define different end point for different request types
    # POST - An upload style request
    if request.method == 'POST':
        # Parse the incoming request object into a dataframe
        data = pd.read_csv(io.BytesIO(request.data), encoding="latin1")

        # We need to format this DataFrame like our training set
        df_data_final = process_training_data(data, 'Test')
        # Use our model to predict new results
        model_results = RF.predict(df_data_final.drop(['PassengerId'], axis=1))
        # Add the model results to our data frame
        df_data_final['Survived'] = model_results

        # The current DataFrame is the transformed one,
        # we want results on the original
        # Take the IDs and results
        df_outcomes = df_data_final[['PassengerId', 'Survived']]
        # Merge results onto original DataFrame and drop created features
        df_final = data.merge(df_outcomes, left_on=['PassengerId'],
                              right_on=['PassengerId'], how='inner'). \
            drop(['Name Contains MR', 'Valid Cabin'], axis=1)
        # Transpose and return the DataFrame
        return df_final.to_csv(index=False)
    # GET - A web page style request
    if request.method == 'GET':
        return "End point for generating predictions"
