import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging

TRAIN_PATH = os.path.join('artifacts', 'train.csv')
TEST_PATH = os.path.join('artifacts', 'test.csv')
RAW_PATH = os.path.join('artifacts', 'data.csv')


def initiate_data_ingestion():
    logging.info("Data Ingestion started")
    try:
        df = pd.read_csv('Notebook/Data/stud.csv')
        logging.info("Dataset read as dataframe")

        os.makedirs(os.path.dirname(TRAIN_PATH), exist_ok=True)

        df.to_csv(RAW_PATH, index=False)

        train_set, test_set = train_test_split(
            df, test_size=0.2, random_state=76
        )

        train_set.to_csv(TRAIN_PATH, index=False)
        test_set.to_csv(TEST_PATH, index=False)

        logging.info("Data ingestion completed")

        return TRAIN_PATH, TEST_PATH

    except Exception as e:
        logging.error("Error occurred during data ingestion")
        raise CustomException(e, sys)


if __name__ == "__main__":
    initiate_data_ingestion()
