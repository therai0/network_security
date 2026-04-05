
from networksecurity.constant.traning_pipeline import MODEL_TRAINER_TRAINED_MODEL_NAME,SAVED_MODEL_DIR

import sys 
from networksecurity.exception.exception import NetworkSecurityException


class NetoworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor 
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,X):
        try:
            X_transform = self.preprocessor.transform(X)
            y_predict = self.model.predict(X_transform)
            return y_predict 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
