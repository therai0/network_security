from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig())
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_frame = data_ingestion.export_collection_as_dataframe()
    file_path = data_ingestion.init_data_ingestion()
    print(file_path.test_file_path)
    print(file_path.train_file_path)

