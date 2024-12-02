import sys
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.exception.exception import NetworkSecurityException 
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig , DataValidationConfig 
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifacts
from NetworkSecurity.components.data_validation import DataValidation 


if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()

        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiated data Ingestion")
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")
        print(data_ingestion_artifacts)

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifacts=data_ingestion_artifacts,
                       data_validation_config=data_validation_config)
        logging.info("Initiating data validation")
        data_validation_artifacts = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifacts)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

