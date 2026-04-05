from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TraningPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys 
if __name__ == "__main__":
    try:
        logging.info("Data ingestion started")
        training_pipeline_config = TraningPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()

        logging.info("Complete of data ingestion")
        logging.info("Data validation started")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
                data_validation_config=data_validation_config,
                data_ingestion_artifacts=data_ingestion_artifacts
        )
        data_validation_artifacts = data_validation.init_data_validation()

        logging.info("End of data validation")
        logging.info("Initation of data transformation")

        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(
            data_validation_artifacts= data_validation_artifacts,
            data_transformation_config=data_transformation_config
        )
        data_transformation_artifacts = data_transformation.initiate_data_transformation()
        print(data_transformation_artifacts)



    except Exception as e:
        raise NetworkSecurityException(e,sys)
