import sys

from networksecurity.entity.artifact_entity import ClasssificationMetricartifact
from networksecurity.exception.excetion import NetworkException
from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(y_true, y_pred)-> ClasssificationMetricartifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        
        classification_metrics = ClasssificationMetricartifact(
            f1_score= model_f1_score,
            precision_score= model_precision_score,
            recall_score= model_recall_score
        )
        return classification_metrics 
    except Exception as e:
        raise NetworkException(e, sys) from e