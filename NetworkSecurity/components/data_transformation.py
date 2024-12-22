import sys 
import os 
import numpy as np
import pandas as pd 
from sklearn.impute import KNNImputer 
from sklearn.pipeline import Pipeline

from NetworkSecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from NetworkSecurity.entity.artifact_entity import DataTransformationArtifacts, DataValidationArtifacts
from NetworkSecurity.entity.config_entity import DataTransformationConfig 
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.utils.common.functions import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifacts: DataValidationArtifacts,
                    data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config 
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNN imputer object with parameter specified in training pipeline.py file
        and retune the pipeline object with tha KNNImputer object as the first step.
        Args:
            cls: DataTransformation
        Returns:
            A pipeline object 
        """
        logging.info("entered get_data_transormer_object method of transformation class")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initilizing KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_transformation(self)-> DataTransformationArtifacts:
        logging.info("Entered initiate_data_transformation method of Data Transformation class")
        try:
            logging.info("Initiating Data Transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)

            # Training data frame
            X_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            y_train_df = train_df[TARGET_COLUMN]
            # Replacing the feature values with 0 and 1. (replacing -1 to 0)
            X_train_df = X_train_df.replace(-1, 0)

            # Testing data frame
            X_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            y_test_df = test_df[TARGET_COLUMN]
            # Replacing the feature values with 0 and 1. (replacing -1 to 0)
            X_test_df = X_test_df.replace(-1, 0)

            # Transforming the data
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(X_test_df)
            X_train_transformed_df = preprocessor_object.transform(X_train_df)
            X_test_transformed_df = preprocessor_object.transform(X_test_df)
            train_arr = np.c_[X_train_transformed_df, np.array(y_train_df)]
            test_arr = np.c_[X_test_transformed_df, np.array(y_test_df)]

            # Save array data   
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            # Preparing artifacts
            data_transformation_artifacts = DataTransformationArtifacts(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
                )
            return data_transformation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)

