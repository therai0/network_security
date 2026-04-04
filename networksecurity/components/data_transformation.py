import sys, os
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.traning_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
)
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifacts,
    DataValidationArtifacts,
)
from networksecurity.utils.main_utils.utils import save_numpy_array_data
from networksecurity.entity.config_entity import DataTransformationConfig


class DataTransformation:
    def __init__(
        self,
        data_validation_artifacts: DataValidationArtifacts,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(cls) -> Pipeline:
        """
        Initilize the KNN imputer object with parameter which is define in training_pipeline.py file

        arg:
            cls: DataTransformer
        Return:
             pipeline object
        """
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initlization of KNNImputer with params {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )

            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Read the data from the particular path
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        try:
            logging.info("Data transformation initation")
            train_df = DataTransformation.read_data(
                self.data_validation_artifacts.valid_train_file_path
            )
            test_df = DataTransformation.read_data(
                self.data_validation_artifacts.invalid_test_file_path
            )

            # Dropping the target colums
            input_features_train_df = train_df.drop([TARGET_COLUMN], axis=1)
            train_target_features = train_df[TARGET_COLUMN]
            train_target_features = train_target_features.replace(-1, 0)

            input_features_test_df = test_df.drop([TARGET_COLUMN], axis=1)
            test_target_features = test_df[TARGET_COLUMN]
            test_target_features = test_target_features.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            transformed_input_train_features = preprocessor.fit_transform(input_features_train_df)
            transformed_input_test_features = preprocessor.transform(input_features_test_df)
            



        except Exception as e:
            raise NetworkSecurityException(e, sys)
