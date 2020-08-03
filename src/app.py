from flask import Flask, request, render_template
from joblib import load
import pandas as pd
import io
import sys
import argparse

# Define the app as a flask app
app = Flask(__name__)
# Set Debug as True to enable quick dev
app.config['DEBUG'] = True

# Data_encodings
# The same one we use for training
Data_dict = {'Sex': {'male': 0, 'female': 1},
             'Embarked': {'S': 0, 'C': 1, 'Q': 2}}


# Define an API end point
# This is a test to show the page is working
@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return render_template('index.html')


# Create the Model Predict Endpoint
# Use a command like
# curl --data-binary "@test.csv" --request POST http://localhost:8001/predict
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

        # Does name contain MR
        df_data_raw['Name Contains MR'] = df_data_raw['Name'].apply(lambda x: 'MR' in x.upper())
        # Is there a valid ticket number
        df_data_raw['Valid Cabin'] = ~df_data_raw['Cabin'].isna()

        # Drop rows with missing values, reset index to enable rejoining
        df_data_final = df_data_raw[['PassengerId', 'Pclass', 'Sex', 'Age', 'SibSp',
                                     'Parch', 'Fare', 'Embarked', 'Name Contains MR',
                                     'Valid Cabin']].dropna().reset_index(drop=True)

        # Apply Data Encodings
        df_data_final['Sex'] = df_data_final['Sex'] \
            .apply(lambda x: Data_dict['Sex'][x])
        df_data_final['Embarked'] = df_data_final['Embarked'] \
            .apply(lambda x: Data_dict['Embarked'][x])

        # Use our model to predict new results
        model_results = RF.predict(df_data_final.drop(['PassengerId'], axis=1))

        # Add the model results to our data frame
        df_data_final['Survived'] = model_results

        # The current DataFrame is the transformed one,
        # we want results on the original

        # Take the IDs and results
        df_outcomes = df_data_final[['PassengerId', 'Survived']]

        # Merge results onto original DataFrame and drop created features
        df_final = df_data_raw.merge(df_outcomes, left_on=['PassengerId']
                                     , right_on=['PassengerId'], how='inner'). \
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
    RF = load('../models/'+args.m)

    # Run the Web App on http://localhost:port
    app.run(host='0.0.0.0', port=args.p)
