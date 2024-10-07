import os
import sys
import pandas as pd
import numpy as np
from src.exceptions import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_object

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

@dataclass
class DataTransformationConfig: 
    preprocessor_object_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation: 
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def initiate_data_transformation(self, train_path, test_path):
        logging.info("Data Transformation Started...")
        
        try:

            logging.info("Preprocessing Started...")
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            preprocessing_object = self.get_data_transformer_object()


            target_column_name = 'Exited'
            columns_to_drop = ['Exited']

            ## Train data
            input_feature_train = train_data.drop(columns=columns_to_drop, axis=1)
            target_feature_train = train_data[target_column_name]

            ## Test data
            input_feature_test = test_data.drop(columns=columns_to_drop, axis=1)
            target_feature_test = test_data[target_column_name]
           
            input_feature_train_arr = preprocessing_object.fit_transform(input_feature_train)
            input_feature_test_arr = preprocessing_object.transform(input_feature_test)

            # Combine these input and target arrays using np.c_ [X_train, y_train || X_test, y_test]
            train_arr = np.c_ [input_feature_train_arr, np.array(target_feature_train)]
            test_arr = np.c_ [input_feature_test_arr, np.array(target_feature_test)]

            logging.info("Preprocessing object saved...")

            save_object(
                file_path = self.data_transformation_config.preprocessor_object_path, 
                object = preprocessing_object)

            return(train_arr, test_arr, self.data_transformation_config.preprocessor_object_path)

        except Exception as e:
            raise CustomException(e, sys)
    
    def get_data_transformer_object(self): 

        try:
            numerical_features = ['CreditScore','Age', 'Tenure', 
                                  'Balance', 'NumOfProducts',
                                  'HasCrCard','IsActiveMember',
                                  'EstimatedSalary'
                                ]
            categorical_features = ['Geography', 'Gender']

            # Create pipline operations for features
            numerical_features_pipeline = Pipeline(
                steps=[
                    ("standardization", StandardScaler(with_mean=False))
            ])

            categorical_features_pipeline = Pipeline(
                steps=[
                    ("OneHotEncoder", OneHotEncoder()),
                    ("standardization", StandardScaler(with_mean=False))
            ])

            preprocessor = ColumnTransformer([
                ("numerical_pipeline", numerical_features_pipeline, numerical_features),
                ("categorical_pipeline", categorical_features_pipeline, categorical_features)
            ])

            return preprocessor

        except Exception as e: 
            raise CustomException(e, sys)
       
    

