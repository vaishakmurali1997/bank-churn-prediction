import sys
from src.logger import logging
from src.exceptions import CustomException
from src.utils import load_object
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features): 
        
        try: 
            model_path = 'artifacts/trained_model.pkl'
            preprossor_path = 'artifacts/preprocessor.pkl'

            model = load_object(file_path=model_path)
            preprossor = load_object(file_path=preprossor_path)

            data_scaled = preprossor.transform(features)
            print(data_scaled)

            prediction = model.predict(data_scaled)

            if prediction[0] == 0.0: 
                return 'Customer is likely to retain'
            elif prediction[0] == 1:
                return 'Customer is likely to churn'
            else:
                return '[fatal: 100] Something is wrong'
            
        
        except Exception as e: 
            raise CustomException(e, sys)


class CustomData:
    def __init__(
        self,
        creditScore : int,
        age: int, 
        gender: str,
        geography: str,
        tenure: int, 
        balance: int, 
        numOfProducts: int,
        hasCrCard: int,
        isActiveMember: int,
        estimatedSalary: int ):
        
        self.creditScore = creditScore
        self.age = age
        self.gender =gender
        self.geography = geography
        self.tenure = tenure
        self.balance = balance
        self.numOfProducts = numOfProducts
        self.hasCrCard = hasCrCard
        self.isActiveMember = isActiveMember
        self.estimatedSalary = estimatedSalary
    
    def get_data_frame(self):
        try:
            custom_data_input = {
                'CreditScore': [self.creditScore], 
                'Age' : [self.age],
                'Gender': [self.gender],
                'Geography': [self.geography],
                'Tenure': [self.tenure],
                'Balance': [self.balance],
                'NumOfProducts': [self.numOfProducts],
                'HasCrCard': [self.hasCrCard],
                'IsActiveMember': [self.isActiveMember],
                'EstimatedSalary': [self.estimatedSalary]
            
            }

            return pd.DataFrame(custom_data_input)
        except:
            pass
    
