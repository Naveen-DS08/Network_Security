from NetworkSecurity.exception.exception import NetworkSecurityException
import sys

from NetworkSecurity.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score, recall_score, precision_score 

def get_classification_score(y_true, y_pred )->ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        classification_report = ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score= model_recall_score
            )
        return classification_report
    except Exception as e:
        raise NetworkSecurityException(e, sys)
     
