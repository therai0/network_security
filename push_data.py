import os
import sys 
import json
import certifi
import pandas as pd 
import numpy as np
import pymongo
from dotenv import load_dotenv
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")

# certificated authority
ca = certifi.where()


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    # function to read the csv file and convert into csv file
    def csv_to_json_convertor(self,file_path):
        try:
            dataset = pd.read_csv(file_path)
            dataset.reset_index(drop=True,inplace=True)
            records = list(json.loads(dataset.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(mongo_db_url)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    FILE_PATH = "Network_data/phisingData.csv"
    DATABASE = "bhaskar"
    print(type(DATABASE))
    collecation = "Networkdata"
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_convertor(FILE_PATH)
    lenght = network_obj.insert_data_to_mongodb(records=records,database=DATABASE,collection=collecation)
    print(lenght)

