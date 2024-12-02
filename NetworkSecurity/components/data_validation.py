import os
import sys
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifacts
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
from NetworkSecurity.utils.common.functions import *

class DataValidation:
    def __init__(self, 
                 data_ingestion_artifacts: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_df(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validate_no_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            default_col_len = len(self.schema_config["columns"])
            logging.info(f"Required no of columns: {default_col_len}")
            df_col_len = len(dataframe.columns) 
            logging.info(f"Data frame has the column length of {df_col_len}")
            if df_col_len == default_col_len:
                return True 
            return False 
        except Exception as e:
            raise NetworkSecurityException(e, sys)  

    def validate_numerical_columns(self, dataframe: pd.DataFrame) ->bool:
        try:
            default_num_columns = self.schema_config["numerical_columns"]
            df_num_cols = list((dataframe.select_dtypes("int64")).columns)
            if default_num_columns not in df_num_cols:
                return False 
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_data_drift(self, default_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) ->bool:
        try:
            status = False 
            report={}
            for column in default_df.columns:
                d1 = default_df[column]
                d2 = current_df[column]
                sample_dist = ks_2samp(d1,d2)
                if sample_dist.pvalue >= threshold:
                    is_found = False 
                else:
                    is_found = True  
                    status = True 
                report.update(
                    {column:{"p_value": float(sample_dist.pvalue),
                             "drift_status": is_found}}
                )
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Create directory 
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
       

    def initiate_data_validation(self)-> DataValidationArtifacts:
        try:
            train_file_path = self.data_ingestion_artifacts.trained_file_path 
            test_file_path = self.data_ingestion_artifacts.test_file_path

            # Read the data from train and test path 
            train_df = DataValidation.read_df(train_file_path)
            test_df = DataValidation.read_df(test_file_path)

            # Validate number of columns 
            status = self.validate_no_of_columns(dataframe=train_df)
            if not status:
                error_message = "Train dataframe does not contain all columns"
            status = self.validate_no_of_columns(dataframe=test_df)
            if not status:
                error_message = "Test dataframe does not cointain all columns"
            
            # Validate numerical columns exists
            status = self.validate_numerical_columns(dataframe=train_df)
            if not status: 
                error_message = "Train dataframe has missing numerical columns"
            status = self.validate_numerical_columns(dataframe=test_df)
            if not status: 
                error_message = "Test dataframe has missing numerical columns"

            # Check data drift
            status = self.detect_data_drift(default_df=train_df, current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            if not status:
                train_df.to_csv(
                    self.data_validation_config.valid_train_file_path, index = False, header=True 
                    )
                test_df.to_csv(
                    self.data_validation_config.valid_test_file_path, index =False, header=True
                )

            
            data_validation_artifacts = DataValidationArtifacts(
                validation_status= status, 
                valid_train_file_path= self.data_ingestion_artifacts.trained_file_path,
                valid_test_file_path= self.data_ingestion_artifacts.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifacts



        except Exception as e:
            raise NetworkSecurityException(e, sys)