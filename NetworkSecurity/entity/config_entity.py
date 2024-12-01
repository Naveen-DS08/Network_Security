from datetime import datetime
import os
from NetworkSecurity.constants import data_ingestion_pipeline

class DataIngestionPipelineConfig():
    def __init__(self, timestamp= datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipelinename = data_ingestion_pipeline.PIPELINE_NAME
        self.artifact_name = data_ingestion_pipeline.ARTIFACT_DIR 
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp: str = timestamp

class DataIngestionConfig():
    def __init__(self, data_ingestion_pipeline_config:DataIngestionPipelineConfig):
        self.data_ingestion_dir : str = os.path.join(
            data_ingestion_pipeline_config.artifact_dir, 
            data_ingestion_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path:str = os.path.join(
            self.data_ingestion_dir, data_ingestion_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            data_ingestion_pipeline.FILE_NAME
        )
        self.training_file_path:str = os.path.join(
            self.data_ingestion_dir, data_ingestion_pipeline.DATA_INGESTION_INGESTED_DIR,
            data_ingestion_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path:str = os.path.join(
            self.data_ingestion_dir, data_ingestion_pipeline.DATA_INGESTION_INGESTED_DIR,
            data_ingestion_pipeline.TEST_FILE_NAME
        )  
        self.train_test_split_ratio: float = data_ingestion_pipeline.DATA_INGESTIONTRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = data_ingestion_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name : str = data_ingestion_pipeline.DATA_INGESTION_DATABASE_NAME