import sys
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.exception.exception import NetworkSecurityException 
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig, DataIngestionPipelineConfig

if __name__=="__main__":
    try:
        data_ingestion_pipeline_config = DataIngestionPipelineConfig()
        data_ingestion_config = DataIngestionConfig(data_ingestion_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiated data Ingestion")
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

