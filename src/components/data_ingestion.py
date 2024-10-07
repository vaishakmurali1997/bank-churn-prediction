import os
import sys 
from dataclasses import dataclass
import pandas as pd
from src.logger import logging
from src.exceptions import CustomException
from sklearn.model_selection import train_test_split

from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')

class DataIngestion: 
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingesstion Method")
        
        try:
            data = pd.read_csv('notebook/data/churn.csv')
            logging.info('Read the dataset')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info('Train and Test initalization')
            train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Data Ingestion Completed')
            
            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)
        except Exception as e: 
            raise CustomException(e, sys)

if __name__ == "__main__":
    object = DataIngestion()
    train_data, test_data = object.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data, test_data)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_training(train_arr=train_arr, test_arr=test_arr))
