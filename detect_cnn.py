import json
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
import matplotlib.pyplot as plt
from process import *
import shutil
import glob
import os

DATASET_PATH="./test"
IP_DATA_PATH="top.json"

def load_data(data_path):
    """Loads training dataset from json file.
        :param data_path (str): Path to json file containing data
        :return X (ndarray): Inputs
        :return y (ndarray): Targets
    """

    with open(data_path, "r") as fp:
        data = json.load(fp)

    X = np.array(data["mfcc"])
    y = np.array(data["labels"])
    return X, y

def prepare_datasets(test_size, validation_size,data_path):
    """Loads data and splits it into train, validation and test sets.
    :param test_size (float): Value in [0, 1] indicating percentage of data set to allocate to test split
    :param validation_size (float): Value in [0, 1] indicating percentage of train set to allocate to validation split
    :return X_train (ndarray): Input training set
    :return X_validation (ndarray): Input validation set
    :return X_test (ndarray): Input test set
    :return y_train (ndarray): Target training set
    :return y_validation (ndarray): Target validation set
    :return y_test (ndarray): Target test set
    """

    # load data
    X, y = load_data(data_path)

    # create train, validation and test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=validation_size)

    # add an axis to input sets
    X_train = X_train[..., np.newaxis]
    X_validation = X_validation[..., np.newaxis]
    X_test = X_test[..., np.newaxis]

    return X_train, X_validation, X_test, y_train, y_validation, y_test

def predict(model, X, y):
    """Predict a single sample using the trained model
    :param model: Trained classifier
    :param X: Input data
    :param y (int): Target
    """

    # add a dimension to input data for sample - model.predict() expects a 4d array in this case
    X = X[np.newaxis, ...] # array shape (1, 130, 13, 1)

    # perform prediction
    prediction = model.predict(X)

    # get index with max value
    predicted_index = np.argmax(prediction, axis=1)

    print("Target: {}, Predicted label: {}".format(y, predicted_index))
    return (y,predicted_index)

def detect_genre_cnn():
    cnn_model = keras.models.load_model('saved_model/my_CNN_model')    
    
    save_mfcc(DATASET_PATH, JSON_PATH, num_segments=10)
    # pick a sample to predict from the test set
    tX_train, tX_validation, tX_test, ty_train, ty_validation, ty_test = prepare_datasets(0.25, 0.2, IP_DATA_PATH)
    X_to_predict = tX_test[0]
    y_to_predict = ty_test[0]
    
     # predict sample with CNN model
    a, b = predict(cnn_model, X_to_predict, y_to_predict)
    print("CNN:- \na=", a, "\nb=", b)
    
    f = open('top.json', 'r+')
    f.truncate(0)
    f.close()
    os.chdir("./test/input/")
    for file in glob.glob("*.au"):
        os.remove(file)
    os.chdir("../../")
    
    if b==1:
        return "Blues"
    elif b==2:
        return "Classical"
    elif b==3:
        return "Country"
    elif b==4:
        return "Disco"
    elif b==5:
        return "HipHop"
    elif b==6:
        return "Jazz"
    elif b==7:
        return "Metal"
    elif b==8:
        return "Pop"
    elif b==9:
        return "Reggae"
    elif b==10:
        return "Rock"