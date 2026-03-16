import os
import sys
import mlflow
import mlflow.sklearn

from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.comfig_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel # it combine the preprocessor and trained model in one place to do prediction easily with new data
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, 
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkException(e, sys) from e 
    
    def track_mlflow(self, best_model, classification_metric):
        mlflow.set_tracking_uri("http://127.0.0.1:5000")
        mlflow.set_experiment("NetworkSecurity")
        with mlflow.start_run():
            f1_score = classification_metric.f1_score 
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score
            
            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(best_model, name = "model")
             
        

    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }

            params = {

                "Decision Tree": {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                },

                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },

                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },

                "AdaBoost": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            # Evaluate all models
            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params
            )

            # Find best model
            best_model_score = max(model_report.values())

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            logging.info(f"Best Model Found: {best_model_name}")

            # Train predictions
            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_score(
                y_true=y_train,
                y_pred=y_train_pred
            )
            
            ## track the MLFLOW  -> MLflow is a tool that helps track, manage, and deploy machine learning models during the ML lifecycle
            self.track_mlflow(best_model, classification_train_metric)

            # Test predictions
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(
                y_true=y_test,
                y_pred=y_test_pred
            )
            self.track_mlflow(best_model, classification_test_metric)

            
            print("Preprocessor path:", self.data_transformation_artifact.transformed_object_file_path)

            # Load preprocessor
            preprocessor = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )

            # Create model directory
            model_dir_path = os.path.dirname(self.model_trainer_config.train_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            # Combine preprocessor + model
            network_model = NetworkModel(
                preprocessor=preprocessor,
                model=best_model
            )

            # Save model
            save_object(
                file_path=self.model_trainer_config.train_model_file_path,
                obj=network_model
            )

            # Create artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.train_model_file_path,
                train_matric_artifact=classification_train_metric,
                test_matric_artifact=classification_test_metric
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")

            return model_trainer_artifact
        except Exception as e:
            raise NetworkException(e, sys) from e
        
    def initiated_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            # load train and test file
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            X_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]

            X_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]
            
            model = self.train_model(X_train, y_train, X_test, y_test)
            
            return model   
        except Exception as e:
            raise NetworkException(e, sys) from e