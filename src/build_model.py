import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from joblib import dump
import argparse
import sys
from process_data import process_training_data


# The main function for building our model

def build_model(data, model_name):
    # Lets do some feature engineering
    # As this is common to train and test we define it a separate file and import it
    df_data_final = process_training_data(data, 'Train')

    # Define a train and test set ids
    df_train_ids = df_data_final['PassengerId'].sample(frac=0.8, random_state=0)
    df_test_ids = df_data_final[~df_data_final['PassengerId'].isin(df_train_ids)]['PassengerId']

    # Define train and test set
    df_train = df_data_final[df_data_final['PassengerId'].isin(df_train_ids)].drop(['PassengerId'], axis=1)
    df_test = df_data_final[df_data_final['PassengerId'].isin(df_test_ids)].drop(['PassengerId'], axis=1)

    # Define target variable in train and test set
    train_x, train_y = df_train.drop(['Survived'], axis=1), df_train['Survived']
    test_x, test_y = df_test.drop(['Survived'], axis=1), df_test['Survived']

    # Define a Random Forest Model
    rf = RandomForestClassifier(random_state=0)

    # Fit Random Forest
    rf.fit(train_x, train_y)

    # Fit on Test Set
    pred_y = rf.predict(test_x)

    # Print Model AUC Score
    print(roc_auc_score(test_y, pred_y))

    # Save Model
    dump(rf, '../models/' + model_name)


if __name__ == "__main__":
    #   Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', help='Saved model name, should be .joblib')
    parser.add_argument('-t', help='Training data csv file')
    args = parser.parse_args()

    # Check the saved model has the correct format
    if args.m.split('.')[-1] != 'joblib':
        print('The model should be a joblib file')
        sys.exit()

    # Check the training data is a csv
    if args.t.split('.')[-1] != 'csv':
        print('The training file should be a csv')
        sys.exit()

    # Load the data
    df_data_raw = pd.read_csv('../data/' + args.t)

    # Check the training file has the correct column names
    if set(df_data_raw.columns) != {'PassengerId', 'Survived', 'Pclass',
                                    'Name', 'Sex', 'Age', 'SibSp', 'Parch',
                                    'Ticket', 'Fare', 'Cabin', 'Embarked'}:
        print("Training data doesn't have the correct format")
        sys.exit()

    # Run the model build function
    build_model(df_data_raw, args.m)
