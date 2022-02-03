import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split

def open_csv_file(path):
    return pd.read_csv(path)

def data_prepare():
    np.set_printoptions(precision=3, suppress=True)
    train=open_csv_file('app/keras_titanic/train.csv')
    test =open_csv_file('app/keras_titanic/test.csv')
    # label_column = 'Survived'
    # labels = [0,1]
    print(train.head())
    print(test.head())
    train_test_data = [train,test]
    for dataset in train_test_data :
        dataset["Title"] = dataset['Name'].str.extract('([A-za-z]+)\. ', expand=False)
    title_mapping = {"Mr": 0, "Miss": 1, "Mrs": 2,
                    "Master": 3, "Dr": 3, "Rev": 3, "Col": 3, "Ms": 2, "Mile": 3, "Major": 3, "Lady": 3, "Capt": 3,
                    "Sir": 3, "Don": 3, "Mme": 3, "Jonkheer": 3, "Countess": 3}
    for dataset in train_test_data:
        dataset['Title'] = dataset['Title'].map(title_mapping)

    df1 = train
    df1['Age'].fillna(df1['Age'].median(),inplace=True)

    df2 = test
    df2['Age'].fillna(df2['Age'].median(),inplace=True)

    train["Embarked"] = train["Embarked"].fillna("S")
    train['Embarked'][train["Embarked"]== "S"] = 0
    train['Embarked'][train["Embarked"]== "C"] = 1
    train['Embarked'][train["Embarked"]== "Q"] = 2

    test['Embarked'][train["Embarked"]== "S"] = 0
    test['Embarked'][train["Embarked"]== "C"] = 1
    test['Embarked'][train["Embarked"]== "Q"] = 2

    train["Fare"].fillna(test["Fare"].mean(), inplace=True)
    test["Fare"].fillna(test["Fare"].mean(), inplace=True)

    train = train.drop(['Name'], axis = 1)
    train = train.drop(['PassengerId'], axis = 1)
    train = train.drop(['Cabin'], axis = 1)
    train = train.drop(['Ticket'], axis = 1)
    train = train.drop(['Embarked'], axis = 1)

    test = test.drop(['Name'], axis = 1)
    test = test.drop(['PassengerId'], axis = 1)
    test = test.drop(['Cabin'], axis = 1)
    test = test.drop(['Ticket'], axis = 1)
    test = test.drop(['Embarked'], axis = 1)

    sex_mapping = {"male": 0, "female":1}
    train['Sex'] = train['Sex'].map(sex_mapping)
    test['Sex'] = test['Sex'].map(sex_mapping)

    x_data = train.values[:,[1,2,3,4,5,6]]
    y_data = train.values[:,[0]]


    X_train, X_test, y_train, y_test = train_test_split(x_data, y_data,
                                                        test_size=0.1, random_state=7)

    X_train = np.asarray(X_train).astype('float32')
    y_train = np.asarray(y_train).astype('float32')
    y_test = np.asarray(y_test).astype('float32')
    X_test = np.asarray(X_test).astype('float32')

    return X_train,y_train,y_test,X_test


def titanic_simulator(user_answer):
    X_train, y_train, y_test, X_test = data_prepare()
    model = Sequential()
    model.add(Dense(255, input_shape=(6,), activation='relu'))
    model.add(Dense((1), activation='sigmoid'))
    model.compile(loss='mse', optimizer='Adam', metrics=['accuracy'])
    model.summary()
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50)
    survive = round(model.predict(user_answer)[0][0] * 100)
    return survive




