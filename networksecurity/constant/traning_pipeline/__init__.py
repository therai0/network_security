import numpy as np
import os 
"""

defining common constant variable for traning pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "phisingData.csv" #data file name
TRAIN_FILE_NAME ="train.csv"
TEST_FILE_NAME = "test.csv"

SAVED_MODEL_DIR = os.path.join("saved_models")


"""
Data ingestion related constant start with DATA_INGESTION VAR NAME 
"""
DATA_INGESTION_COLLECTION_NAME:str = "Networkdata"
DATA_INGESTION_DATABASE_NAME:str = "bhaskar"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2


"""
Schema file path 
"""
SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")


"""
Data validation related constant start with DATA_VALIDATION  VAR NAME 
"""
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str  = "validated"
DATA_VALIDATION_INVALID_DIR:str  = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str  = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str  = "report.yaml"


"""
Data Transformation related constant file start with DATA_TRANSFORMATION
"""
DATA_TRANSFORMATION_DIR_NAME = "data_transformation" 
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRAINSFORMATION_TRANSFORMED_OBJECT_DIR_ = "transformed_object"


# KNN imputer to replace nan value 
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"

}

"""
Preprocessor file name
"""
PREPROCESSOR_OBJECT_FILE_NAME = "preprocessor.pkl"



"""
Model trainer related constant start with MODEL_TRAINER VAR NAME 
"""

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_DIR_NAME:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:str = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05 