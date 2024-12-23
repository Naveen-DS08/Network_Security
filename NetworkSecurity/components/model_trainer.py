import os 
import sys 

from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException 

from NetworkSecurity.entity.artifact_entity import DataTransformationArtifacts, ModelTrainerArtifacts
from NetworkSecurity.entity.config_entity import ModelTrainerConfig 

from NetworkSecurity.utils.common.functions import (save_object, load_object, 
                                                    load_numpy_array_data)
from NetworkSecurity.utils.ml_utils.model.evaluate import evaluate_models
from NetworkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import ( RandomForestClassifier, 
                            AdaBoostClassifier, GradientBoostingClassifier)

import mlflow

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifacts: DataTransformationArtifacts):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifacts = data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self, best_model , classification_metric ):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("Precision", precision_score)
            mlflow.log_metric("Recall", recall_score)

            mlflow.sklearn.log_model(best_model, "model")


        
    def train_model(self,X_train, y_train, X_test, y_test):
        try:
            
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "Logistic Regression": LogisticRegression(verbose=1),
                "Ada Boost": AdaBoostClassifier()
            }
        
            params = {
                "Decision Tree":{
                    "criterion": ["gini", "entropy", "log_loss"],
                    "splitter": ["best", "random"],
                    "max_features": ["sqrt", "log2"]
                },
                "Random Forest":{
                    "criterion": ["gini", "entropy", "log_loss"],
                    "max_features": ["sqrt", "log2", None],
                    "n_estimators": [8,16,32,64,128,246]
                },
                "Gradient Boosting":{
                    "loss": ["log_loss", "exponential"],
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    "criterion": ["squared_error", "friedman_mse"],
                    "max_features": ["auto", "sqrt", "log2"],
                    "n_estimators": [88,16,32,64,128,256]
                },
                "Ada Boost":{
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "n_estimators": [88,16,32,64,128,256]
                },
                "Logistic Regression":{}
            }
            model_report: dict = evaluate_models(X_train=X_train, y_train= y_train,
                                                 X_test = X_test, y_test=y_test, 
                                                 params = params, models= models) 
            
            # Get best model score and model
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            # Predict 
            y_train_pred = best_model.predict(X_train)
            classification_train_report = get_classification_score(y_true=y_train, y_pred= y_train_pred )

            # Track experiments with MLflow
            self.track_mlflow(best_model, classification_train_report)

            y_test_pred = best_model.predict(X_test)
            classification_test_report = get_classification_score(y_true=y_test, y_pred= y_test_pred )

            # Track experiments with MLflow
            self.track_mlflow(best_model, classification_test_report)

            preprocessor = load_object(file_path=self.data_transformation_artifacts.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trainer_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(self.model_trainer_config.trainer_model_file_path, obj=Network_Model)

            # Model Trainer Artifacts 
            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_file_path=self.model_trainer_config.trainer_model_file_path,
                train_metric_artifact= classification_train_report,
                test_metric_artifact= classification_test_report
                                  )
            logging.info(f"Model Trainer Artifacts: {model_trainer_artifacts}")
            return model_trainer_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)
           
        
    def initiate_model_trainer(self)->ModelTrainerArtifacts:
        try:

            train_file_path = self.data_transformation_artifacts.transformed_train_file_path
            test_file_path = self.data_transformation_artifacts.transformed_test_file_path

            # loading training array and testing array 
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            # splitting dependent and independent features 
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
                )
            
            model_trainer_artifacts = self.train_model(X_train, y_train, X_test, y_test)
            return model_trainer_artifacts


        except Exception as e:
            raise NetworkSecurityException(e, sys)
 