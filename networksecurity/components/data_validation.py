from networksecurity.entity.artifact_entity import DataValidationArtifacts,DataIngestionArtifacts
from networksecurity.entity.config_entity import DataValidationConfig ,DataIngestionConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd 
from networksecurity.constant.traning_pipeline import SCHEMA_FILE_PATH
import os,sys 


class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifacts:DataIngestionArtifacts):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        "read the file and return as a data frame"
        try:
            return pd.read_csv(file_path)    
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        """
        Validate the number of columns in Datafram
        """
        try:
            number_of_columns = len(self.schema_config["Columns"])
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has :{len(dataframe.columns)}")
            return number_of_columns == len(dataframe.columns)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True 
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False 
                else:
                    is_found = True
                    status = False 
                report.update(
                    {
                        column:{
                            "p_value":float(is_same_dist.pvalue),
                            "drift_status":is_found
                        }
                    }
                )
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def init_data_validation(self)->DataValidationArtifacts:
        try:
            train_file_path= self.data_ingestion_artifacts.train_file_path
            test_file_path = self.data_ingestion_artifacts.test_file_path

            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            status  = self.validate_number_of_columns(train_df)
            if not status:
                train_error_message = f"Train DataFrame doesn't contain all columns"
            status = self.validate_number_of_columns(test_df)
            if not status:
                test_error_message = f"Test DataFrame doesn't contain all columns"
            
            status = self.detect_dataset_drift(base_df=train_df,current_df=test_df)

            dir_path = os.path.dirname(self.data_validation_config.valid_data_train_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_data_train_path,index=False,header=True)
            test_df.to_csv(self.data_validation_config.valid_data_test_path,index=False,header=True)

            data_validation_artifacts = DataValidationArtifacts(
                validation_status=status,
                valid_test_file_path=self.data_validation_config.valid_data_test_path,
                valid_train_file_path=self.data_validation_config.valid_data_train_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)




