import os 
import sys 

from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException

from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation 
from NetworkSecurity.components.data_transformation import DataTransformation 
from NetworkSecurity.components.model_trainer import ModelTrainer 

from NetworkSecurity.entity.config_entity import (TrainingPipelineConfig,
                                                  DataIngestionConfig, DataValidationConfig,
                                                  DataTransformationConfig, ModelTrainerConfig )

from NetworkSecurity.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifacts,
                                                     DataTransformationArtifacts, ModelTrainerArtifacts)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config) 
            logging.info("Initializing Data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Completed...\nData Ingestion Artifacts:\n{data_ingestion_artifacts}")
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_atifacts: DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Initializing Data Validation")
            data_validation = DataValidation(data_ingestion_artifacts=data_ingestion_atifacts,
                                             data_validation_config=self.data_validation_config)
            data_validation_artifacts = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Completed...\nData Validation Artifacts:\n{data_validation_artifacts}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifacts: DataValidationArtifacts):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Initializing Data Transformation")
            data_transformation = DataTransformation(data_validation_artifacts=data_validation_artifacts, 
                                                        data_transformation_config= self.data_transformation_config)
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation Completed...\nData Transformation Artifacts:\n{data_transformation_artifacts}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_training(self, data_transformation_artifacts:DataTransformationArtifacts):
        try: 
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Initationg Model Training")
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config, 
                                        data_transformation_artifacts=data_transformation_artifacts)
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training Completed...\nModel Trainer Artifacts:\n{model_trainer_artifacts}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_atifacts=data_ingestion_artifacts)
            data_transformation_artifacts = self.start_data_transformation(data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifacts = self.start_model_training(data_transformation_artifacts=data_ingestion_artifacts)
            return model_trainer_artifacts
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        

                                                        