from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import os 
import sys 
import pymongo 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 

# Config file for data ingestion 
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion():
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_df(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"], axis=1)
            df.replace({"na":np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_data_into_featurestore(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # creating folder 
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_into_train_test(self, dataframe: pd.DataFrame):
        try:
            train, test = train_test_split(dataframe,
                                           test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on dataframe")
            train_dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(train_dir_path, exist_ok=True)
            test_dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(test_dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path")
            train.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test.to_csv(self.data_ingestion_config.testing_file_path, index = False, header=True)
            logging.info(f"Exported train and test path")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_df()
            dataframe = self.export_data_into_featurestore(dataframe)
            self.split_data_into_train_test(dataframe)
            dataingestion_artifacts = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path, 
                test_file_path = self.data_ingestion_config.testing_file_path
            )
            return dataingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)