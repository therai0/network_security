from datetime import datetime
import os 
from networksecurity.constant import training_pipeline



class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifacts_name = training_pipeline.ARTIFACTS_DIR
        self.artifacts_dir = os.path.join(self.artifacts_name,timestamp)
        self.timestamp:str = timestamp


""" 
Configuring the Data ingestion class 
This class provide the file path for train,test and raw(feature store file)
also provide the collection name, database name and ingestion dir

"""
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        # data ingestion dir
        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifacts_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        # feature store file path
        self.feature_store_file_path:str = os.path.join(training_pipeline_config.artifacts_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
        # test data file path
        self.test_data_file_path:str = os.path.join(training_pipeline_config.artifacts_dir,
        training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME)
        # train data file path
        self.train_data_file_path:str = os.path.join(training_pipeline_config.artifacts_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME)
        # train and test split ratio
        self.train_test_split_ratio:float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        # collection name 
        self.collection_name:str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        # database name 
        self.database_name:str = training_pipeline.DATA_INGESTION_DATABASE_NAME
