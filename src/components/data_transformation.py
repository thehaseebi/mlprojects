import sys
import os
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object

PREPROCESSOR_PATH = os.path.join("artifacts", "preprocessor.pkl")
TARGET_COL = "math_score"

NUM_COLS = ["writing_score", "reading_score"]
CAT_COLS = [
    "gender",
    "race_ethnicity",
    "parental_level_of_education",
    "lunch",
    "test_preparation_course",
]


def get_preprocessor():
    try:
        num_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        cat_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder", OneHotEncoder()),
                ("scaler", StandardScaler(with_mean=False)),
            ]
        )

        logging.info("Numerical columns standard scaling completed")
        logging.info("Categorical columns encoding completed")

        preprocessor = ColumnTransformer(
            transformers=[
                ("num_pipeline", num_pipeline, NUM_COLS),
                ("cat_pipeline", cat_pipeline, CAT_COLS),
            ]
        )

        return preprocessor

    except Exception as e:
        raise CustomException(e, sys)


def initiate_data_transformation(train_path, test_path, preprocessor_path=PREPROCESSOR_PATH):
    try:
        logging.info("Reading training and testing data")
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)

        logging.info("Obtaining preprocessing object")
        preprocessor = get_preprocessor()

        X_train = train_df.drop(columns=[TARGET_COL], axis=1)
        y_train = train_df[TARGET_COL]

        X_test = test_df.drop(columns=[TARGET_COL], axis=1)
        y_test = test_df[TARGET_COL]

        logging.info("Applying preprocessing object on training and testing data")
        X_train_arr = preprocessor.fit_transform(X_train)
        X_test_arr = preprocessor.transform(X_test)

        train_arr = np.c_[X_train_arr, np.array(y_train)]
        test_arr = np.c_[X_test_arr, np.array(y_test)]

        logging.info("Data transformation completed")

        save_object(file_path=preprocessor_path, obj=preprocessor)

        return train_arr, test_arr, preprocessor_path

    except Exception as e:
        raise CustomException(e, sys)
