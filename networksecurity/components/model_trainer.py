import os, sys
import mlflow
from networksecurity.entity.artifact_entity import (
    ModelTrainerArtifacts,
    ClassificationMetricArtifacts,
    DataTransformationArtifacts,
)
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numy_array_data,
    evaluate_models,
)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.metric.classification_metric import (
    get_classification_report,
)
from networksecurity.utils.ml_utils.model.estimator import NetoworkModel




class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifacts: DataTransformationArtifacts,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifacts = data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def track_mlflow(self, best_model,classification_metric):
        try:
            with mlflow.start_run():
                f1_score = classification_metric.f1_score
                precision_score = classification_metric.precision_score
                recall_score = classification_metric.recall_score
                mlflow.log_metric("f1 Score",f1_score)
                mlflow.log_metric("precision_score",precision_score)
                mlflow.log_metric("recall",recall_score)
                mlflow.sklearn.log_model(best_model,"model")

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Random forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Logistic regression": LogisticRegression(verbose=1),
                "Adaboost": AdaBoostClassifier(),
                "Gradient boosting": GradientBoostingClassifier(verbose=1),
                "KNNeighbour": KNeighborsClassifier(),
            }
            best_model = evaluate_models(X_train, y_train, X_test, y_test, models)
            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_report(
                y_train, y_train_pred
            )
              # tracking the mlflow
            self.track_mlflow(
                best_model=best_model, classification_metric=classification_train_metric
            )
            
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_report(y_test, y_test_pred)
            
            # tracking the mlflow
            self.track_mlflow(
                best_model=best_model, classification_metric=classification_test_metric
            )

            preprocessor = load_object(
                self.data_transformation_artifacts.transformed_obect_file_path
            )
            model_dir_path = os.path.dirname(
                self.model_trainer_config.train_model_file_path
            )
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetoworkModel(preprocessor=preprocessor, model=best_model)
            save_object(
                self.model_trainer_config.train_model_file_path, object=network_model
            )

            # saving the model in final model dir 
            save_object("final_model/model.pkl",best_model)
        

            # model trainer artifacts
            model_trainer_artifacts = ModelTrainerArtifacts(
                train_model_file_path=self.model_trainer_config.train_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric,
            )
            logging.info(f"{model_trainer_artifacts}")
            return model_trainer_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)



    def initiate_model_trianer(self) -> ModelTrainerArtifacts:
        try:
            train_file_path = (
                self.data_transformation_artifacts.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifacts.transformed_test_file_path
            )

            train_arr = load_numy_array_data(file_path=train_file_path)
            test_arr = load_numy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            model_trainer_artifacts = self.train_model(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test
            )
            return model_trainer_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)
