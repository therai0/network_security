from pyexpat import features

from networksecurity.entity.artifact_entity import DataIngestionArtifacts
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# configuration of the data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig

import os 
import sys 
import pymongo
import pandas as pd 
import numpy as np 
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_connection_as_dataframe(self):
        """
        Read the data from the database(or any source) and return the DataFrame
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            collection = self.mongo_client[database_name][collection_name]

            dataframe = pd.DataFrame(list(collection.find()))
            if "_id" in dataframe.columns.to_list():
                dataframe.drop(["_id"],axis=1,inplace=True)
            dataframe.replace({"na":np.nan},inplace=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_data_into_features_store(self,dataframe:pd.DataFrame):
        """
        extport the data(raw.csv) whole to features store file
        """
        try:
            features_store_file_path = self.data_ingestion_config.features_store_file_path
            dir_path = os.path.dirname(features_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(features_store_file_path,header=True,index=False)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_data,test_data = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Split the data into train and test")

            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_data.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            logging.info("Exporting traning dataset")

            test_data.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("Exporting test dataset")
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_ingestion(self):
        try:
            logging.info("Data Ingestion started")
            dataframe = self.export_connection_as_dataframe()
            dataframe = self.export_data_into_features_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            logging.info("End of Data ingestion")

            return DataIngestionArtifacts(train_file_path=self.data_ingestion_config.train_file_path,
            test_file_path=self.data_ingestion_config.test_file_path)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)