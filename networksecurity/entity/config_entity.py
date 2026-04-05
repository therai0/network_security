import os 
import sys 
from datetime import datetime

# importing the constent 
from networksecurity.constant import traning_pipeline
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException



class TraningPipelineConfig:

    def __init__(self,timestamp=datetime.now()):
        try:
            timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
            self.pipeline_name = traning_pipeline.PIPELINE_NAME
            self.artifact_dir = os.path.join(traning_pipeline.ARTIFACT_DIR,timestamp)
            self.timestamp:str = timestamp
        except Exception as e:
            raise NetworkSecurityException(e,sys)

class DataIngestionConfig:
    """
    In this class we define the configuration for Data ingestion 
    --> Ingestion dir(base dir for raw,train and test file)
    --> Train file path(Where should we need to store the train file)
    --> Test file path(Where should we need to store the test file)
    --> Collection name(Name of collection which is needed for reading the data from database)
    --> DataBase Name 
    --> Split ratio(Ratio for spliting the train and test data)
    """

    def __init__(self,traning_pipeline_config:TraningPipelineConfig):
        try:
            # artificats/2_2026/data_ingestion
            self.data_ingestion_dir:str = os.path.join(
                traning_pipeline_config.artifact_dir,traning_pipeline.DATA_INGESTION_DIR_NAME
            )
            # artificats/2_2026/data_ingestion/feature_store/phisingData.csv
            """
            Features store file (raw data)
            """
            self.features_store_file_path:str = os.path.join(
                self.data_ingestion_dir,traning_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,traning_pipeline.FILE_NAME
            )

            # artificats/2_2026/data_ingestion/train.csv
            self.train_file_path:str = os.path.join(
                self.data_ingestion_dir,traning_pipeline.DATA_INGESTION_DIR_NAME,traning_pipeline.TRAIN_FILE_NAME
            )

             # artificats/2_2026/data_ingestion/test.csv
            self.test_file_path:str = os.path.join(
                self.data_ingestion_dir,traning_pipeline.DATA_INGESTION_DIR_NAME,traning_pipeline.TEST_FILE_NAME
            )
            # split ratio of train and test
            self.train_test_split_ratio:float = traning_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            
            self.collection_name:str = traning_pipeline.DATA_INGESTION_COLLECTION_NAME
            self.database_name:str = traning_pipeline.DATA_INGESTION_DATABASE_NAME
            logging.info("Data ingestion config")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

class DataValidationConfig:
    """
    Here we define the all the configuration for the Data validation
    --> Data validation dir
    --> Valid Data dir
    --> Invalid data dir
    --> Valid data train file path
    --> Valid data test file path
    --> Invalid train file path
    --> Invalid test file path
    --> Drift report file path
    """
    def __init__(self,training_pipeline_config:TraningPipelineConfig):

        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,traning_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir = os.path.join(self.data_validation_dir,traning_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir = os.path.join(self.data_validation_dir,traning_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_data_train_path = os.path.join(self.valid_data_dir,traning_pipeline.TRAIN_FILE_NAME)
        self.valid_data_test_path = os.path.join(self.valid_data_dir,traning_pipeline.TEST_FILE_NAME)
        self.invalid_data_train_path = os.path.join(self.invalid_data_dir,traning_pipeline.TRAIN_FILE_NAME)
        self.invalid_data_test_path = os.path.join(self.invalid_data_dir,traning_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path = os.path.join(self.data_validation_dir,traning_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,traning_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)


class DataTransformationConfig:
    """
    In this class here we define the different information 
    --> Data transformation dir 
    --> transformed train file path
    --> preprocessor file path (transform preprocessor)
    """
    def __init__(self,training_pipeline_config:TraningPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,traning_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.data_transformed_train_file_path = os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        traning_pipeline.TRAIN_FILE_NAME.replace("csv","npy")
        )
        self.data_transformed_test_file_path = os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        traning_pipeline.TEST_FILE_NAME.replace("csv","npy")
        )
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir,traning_pipeline.DATA_TRAINSFORMATION_TRANSFORMED_OBJECT_DIR_,
        traning_pipeline.PREPROCESSOR_OBJECT_FILE_NAME
        )
