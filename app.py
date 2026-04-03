from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TraningPipelineConfig,DataIngestionConfig,DataValidationConfig
from networksecurity.components.data_validation import DataValidation

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys 
if __name__ == "__main__":
    try:
        logging.info("Data ingestion started")
        training_pipeline_config = TraningPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion.initiate_data_ingestion()
        logging.info("Complete of data ingestion")
        logging.info("Data validation started")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_config=data_ingestion_config)
        data_valid_info = data_validation.init_data_validation()
        print(data_valid_info)
        logging.info("Data validation end")
    except Exception as e:
        raise NetworkSecurityException(e,sys)