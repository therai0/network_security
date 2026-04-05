from networksecurity.entity.artifact_entity import ClassificationMetricArtifacts
from sklearn.metrics import f1_score,recall_score,precision_score

from networksecurity.exception.exception import NetworkSecurityException

import sys 

def get_classification_report(y_true,y_pred)->ClassificationMetricArtifacts:
    try:
        score = f1_score(y_true,y_pred)
        recal = recall_score(y_true,y_pred)
        pre_score = precision_score(y_true,y_pred)

        classification_metric_artifacts = ClassificationMetricArtifacts(
            f1_score=score,
            precision_score=pre_score,
            recall_score=recal
        )
        return classification_metric_artifacts
    except Exception as e:
        raise NetworkSecurityException(e,sys)



