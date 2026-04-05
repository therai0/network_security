
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import r2_score
import os , sys 
import pickle
import yaml 
import numpy as np 


def read_yaml_file(file_path:str)->dict:
    """
    Function to read the yaml file 
    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)



def write_yaml_file(file_path:str,content:object,replace:bool = False)->None:
    """
    Creating the yaml file and saving it
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)



def save_numpy_array_data(file_path:str,array:np.array):
    "Save numpy array to file path"
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file:
            np.save(file,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def load_numy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_object(file_path:str,object)-> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(object,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception("File doesn't exist in this path")
        
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise NetworkSecurityException(e,sys)

def evaluate_models(X_train,y_train,X_test,y_test,models):
    try:
        model_report = {}
        for mod in models.keys():
            model = models[mod]
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            score = r2_score(y_test,y_pred)
            model_report[model] = score 
        
        max_values = max(model_report.values())
        best_model = list(model_report.keys())[list(model_report.values()).index(max_values)]

        return best_model
    except Exception as e:
        raise NetworkSecurityException(e,sys)