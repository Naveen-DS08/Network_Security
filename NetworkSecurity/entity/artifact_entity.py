from dataclasses import dataclass 
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    trained_file_path: Path 
    test_file_path: Path

@dataclass 
class DataValidationArtifacts:
    validation_status: bool 
    valid_train_file_path : Path 
    valid_test_file_path : Path 
    invalid_train_file_path: Path 
    invalid_test_file_path: Path
    drift_report_file_path: Path 

@dataclass 
class DataTransformationArtifacts:
    transformed_object_file_path: Path 
    transformed_train_file_path: Path 
    transformed_test_file_path: Path 

@dataclass
class ClassificationMetricArtifact:
    f1_score :float 
    precision_score: float 
    recall_score: float 

@dataclass 
class ModelTrainerArtifacts:
    trained_model_file_path: Path 
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
