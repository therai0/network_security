import os 
import sys 
from datetime import datetime
from networksecurity.constant import traning_pipeline
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException



class TraningPipelineConfig:

    def __init__(self,timestamp=datetime.now()):
        try:
            timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
            self.pipeline_name = traning_pipeline.PIPELINE_NAME
            self.artifacts_name = traning_pipeline.ARTIFACT_DIR
            self.artifact_dir = os.path.join(self.artifact_dir,timestamp)
            self.timestamp:str = timestamp
        except Exception as e:
            raise NetworkSecurityException(e,sys)




class DataIngestionConfig:
    def __init_(self,traning_pipeline_config:TraningPipelineConfig):
        try:
            self.data_ingestion_dir:str = os.path.join(
                traning_pipeline_config.artifact_dir,traning_pipeline.DATA_INGESTION_DIR_NAME
            )
            self.features_store_file_path:str = os.path.join(
                self.data_ingestion_dir,traning_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,traning_pipeline.FILE_NAME
            )
            self.traning_file_path:str = os.path.join(
                self.data_ingestion_dir,traning_pipeline.DATA_INGESTION_DIR_NAME,traning_pipeline.TRAIN_FILE_NAME
            )
            self.test_file_path:str = os.path.join(
                self.data_ingestion_dir,traning_pipeline.DATA_INGESTION_DIR_NAME,traning_pipeline.TEST_FILE_NAME
            )
            self.train_test_split_ratio:float = traning_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name:str = traning_pipeline.DATA_INGESTION_COLLECTION_NAME
            self.database_name:str = traning_pipeline.DATA_INGESTION_DATABASE_NAME
        except Exception as e:
            raise NetworkSecurityException(e,sys)