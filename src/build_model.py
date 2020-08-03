import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from joblib import dump
import argparse
import sys


# The main function for building our model
def build_model(Data, Model_Name):
    # Lets do some feature engineering
    # Does name contain MR
    Data['Name Contains MR'] = Data['Name'].apply(lambda x: 'MR' in x.upper())
    # Is there a valid ticket number
    Data['Valid Cabin'] = ~Data['Cabin'].isna()

    # Drop rows with missing values
    df_data_final = Data[['PassengerId', 'Survived', 'Pclass', 'Sex', 'Age', 'SibSp',
                          'Parch', 'Fare', 'Embarked', 'Name Contains MR',
                          'Valid Cabin']].dropna()

    # Data_encodings
    # Could have used sklearn.preprocessing.LabelEncoder() but we want to reuse these
    Data_dict = {'Sex': {'male': 0, 'female': 1},
                 'Embarked': {'S': 0, 'C': 1, 'Q': 2}}

    # Apply Data Encodings
    df_data_final['Sex'] = df_data_final['Sex'].apply(lambda x: Data_dict['Sex'][x])
    df_data_final['Embarked'] = df_data_final['Embarked'].apply(lambda x: Data_dict['Embarked'][x])

    # Define a train and test set ids
    df_train_ids = df_data_final['PassengerId'].sample(frac=0.8, random_state=0)
    df_test_ids = df_data_final[~df_data_final['PassengerId'].isin(df_train_ids)]['PassengerId']

    # Define train and test set
    df_train = df_data_final[df_data_final['PassengerId'].isin(df_train_ids)].drop(['PassengerId'], axis=1)
    df_test = df_data_final[df_data_final['PassengerId'].isin(df_test_ids)].drop(['PassengerId'], axis=1)

    # Define target variable in train and test set
    train_X, train_Y = df_train.drop(['Survived'], axis=1), df_train['Survived']
    test_X, test_Y = df_test.drop(['Survived'], axis=1), df_test['Survived']

    # Define a Random Forest Model
    RF = RandomForestClassifier(random_state=0)

    # Fit Random Forest
    RF.fit(train_X, train_Y)

    # Fit on Test Set
    pred_Y = RF.predict(test_X)

    # Print Model AUC Score
    print(roc_auc_score(test_Y, pred_Y))

    # Save Model
    dump(RF, '../models/'+Model_Name)


if __name__ == "__main__":
    #   Parse command line aruments
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
    df_data_raw = pd.read_csv('../data/'+args.t)

    # Check the training file has the correct column names
    if set(df_data_raw.columns) != {'PassengerId', 'Survived', 'Pclass',
                                    'Name', 'Sex', 'Age', 'SibSp', 'Parch',
                                    'Ticket', 'Fare', 'Cabin', 'Embarked'}:
        print("Training data doesn't have the correct format")
        sys.exit()

    # Run the model build function
    build_model(df_data_raw, args.m)
