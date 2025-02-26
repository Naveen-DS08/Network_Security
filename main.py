import sys
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.exception.exception import NetworkSecurityException 
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import (DataIngestionConfig, TrainingPipelineConfig , 
                                                  DataValidationConfig, DataTransformationConfig,
                                                   ModelTrainerConfig )
from NetworkSecurity.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifacts,
                                                    DataTransformationArtifacts, ModelTrainerArtifacts)
from NetworkSecurity.components.data_validation import DataValidation 
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.model_trainer import ModelTrainer
from NetworkSecurity.pipeline.training_pipeline import TrainingPipeline


if __name__=="__main__":
    try:
        # training_pipeline_config = TrainingPipelineConfig()

        # data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        # data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        # logging.info("Initiated data Ingestion")
        # data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        # logging.info("Data Ingestion completed")
        # print(data_ingestion_artifacts)

        # data_validation_config = DataValidationConfig(training_pipeline_config)
        # data_validation = DataValidation(data_ingestion_artifacts=data_ingestion_artifacts,
        #                data_validation_config=data_validation_config)
        # logging.info("Initiating data validation")
        # data_validation_artifacts = data_validation.initiate_data_validation()
        # logging.info("Data validation completed")
        # print(data_validation_artifacts)

        # data_transformation_config = DataTransformationConfig(training_pipeline_config)
        # data_transformation = DataTransformation(data_validation_artifacts= data_validation_config, 
        #                                          data_transformation_config=data_transformation_config)
        # logging.info("Initiated Data Transformation")
        # data_transformation_artifacts = data_transformation.initiate_data_transformation()
        # logging.info("Data Transformation Completed")
        # print(data_transformation_artifacts)

        # logging.info("Initiating Model Trainer")
        # model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        # model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, 
        #                              data_transformation_artifacts=data_transformation_artifacts)
        # model_trainer_artifacts = model_trainer.initiate_model_trainer()
        # logging.info("Model Trainer Artifacts Created")
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()



    except Exception as e:
        raise NetworkSecurityException(e, sys)

