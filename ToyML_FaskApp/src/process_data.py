def process_training_data(data, data_set):
    # Lets do some feature engineering
    # Does name contain MR
    data['Name Contains MR'] = data['Name'].apply(lambda x: 'MR' in x.upper())
    # Is there a valid ticket number
    data['Valid Cabin'] = ~data['Cabin'].isna()

    # Drop rows with missing values, we have different row for train and test
    if data_set == 'Train':
        df_data_final = data[['PassengerId', 'Survived', 'Pclass', 'Sex', 'Age', 'SibSp',
                              'Parch', 'Fare', 'Embarked', 'Name Contains MR',
                              'Valid Cabin']].dropna()
    else:
        df_data_final = data[['PassengerId', 'Pclass', 'Sex', 'Age', 'SibSp',
                              'Parch', 'Fare', 'Embarked', 'Name Contains MR',
                              'Valid Cabin']].dropna()

    # Data_encodings
    # Could have used sklearn.preprocessing.LabelEncoder() but we want to reuse these
    data_dict = {'Sex': {'male': 0, 'female': 1},
                 'Embarked': {'S': 0, 'C': 1, 'Q': 2}}

    # Apply Data Encodings
    df_data_final['Sex'] = df_data_final['Sex'].apply(lambda x: data_dict['Sex'][x])
    df_data_final['Embarked'] = df_data_final['Embarked'].apply(lambda x: data_dict['Embarked'][x])

    return df_data_final
