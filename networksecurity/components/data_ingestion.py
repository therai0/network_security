""" 
1. Initiate data ingestion
2. Store the raw file(create feature store file)
3. Split the data into train and test 
4. Save train and test file
"""
import  numpy as np
import os
from dataclasses import dataclass
import pandas as pd 
import sys
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL =  os.getenv("MONGO_DB_URL")

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

# configuration of data ingestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifacts

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
             self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    # fetch the data form the database and return as a dataframe
    def export_collection_as_dataframe(self):
        try:
            logging.info("initation data fetching from database")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[database_name]
            self.collection = self.database[collection_name]
            data_frame = pd.DataFrame(list(self.collection.find()))
            logging.info("Fetching data from database has been completed")
            # removingthe _id columns
            if "_id" in data_frame.columns.to_list():
               data_frame.drop(['_id'],axis=1,inplace=True)
        
            data_frame.replace({"na":np.nan},inplace=True)
            logging.info("Returnig dataframe")
            return data_frame
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    # this function will return the train and test file path 
    def init_data_ingestion(self):
        try:
            data_frame = self.export_collection_as_dataframe()
            # save this data_frame as a feature_store file 
            self.export_data_to_feature_store(data_frame=data_frame)
            self.split_data_into_train_and_test(data_frame=data_frame)
            data_ingestion_artifacts = DataIngestionArtifacts(
                train_file_path=self.data_ingestion_config.train_data_file_path,
                test_file_path=self.data_ingestion_config.test_data_file_path)
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    # function to store the data as a feature_store file
    def export_data_to_feature_store(self,data_frame:pd.DataFrame):
        try:
            logging.info("Exporting data frame as feature_store file")
            dir_path = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            data_frame.to_csv(self.data_ingestion_config.feature_store_file_path,index=False,header=True)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    # function to split the data into train and test
    def split_data_into_train_and_test(self,data_frame:pd.DataFrame):
        try:
            logging.info("Initating test and train data")
            train_data,test_data = train_test_split(data_frame,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            train_dir_path = os.path.dirname(self.data_ingestion_config.train_data_file_path)
            os.makedirs(train_dir_path,exist_ok=True)
            train_data.to_csv(self.data_ingestion_config.train_data_file_path)
            # export train data frame as csv file 
            logging.info("export train data frame as csv file ")
            test_data.to_csv(self.data_ingestion_config.test_data_file_path)
            logging.info("export test data frame as csv file ")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

