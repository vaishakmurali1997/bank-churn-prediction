import os
import sys
from src.utils import save_object, evaluate_model
from src.logger import logging
from dataclasses import dataclass
from src.exceptions import CustomException

# Import model for classification
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier)
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, r2_score

@dataclass
class ModelTrainerConfig: 
    trained_model_file_path = os.path.join('artifacts', 'trained_model.pkl')

class ModelTrainer: 
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig
    
    def initiate_model_training(self, train_arr, test_arr):
        
        try:
            logging.info("Split train and test input data ... ")
            X_train,  y_train, X_test, y_test = (train_arr[:,:-1],train_arr[:,-1], test_arr[:,:-1], test_arr[:,-1])

            # Models to train
            models = {
                'Logistic Regression': LogisticRegression(),
                'SVC': SVC(),
                'Decision Tree': DecisionTreeClassifier(),
                'Gradient Boosting': GradientBoostingClassifier(),
                'AdaBoost': AdaBoostClassifier(),
                'Random Forest': RandomForestClassifier(),
                'KNN': KNeighborsClassifier(),
                'Naive Bayes': GaussianNB()
            }
            
            model_report: dict = evaluate_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            if best_model_score < 0.8: 
                raise Exception ('Model traininng is weak.')
            
            
            logging.info(f"best_model is {best_model_name} & Accuracy Score {best_model_score}")
            
            save_object(
                file_path = self.model_trainer_config.trained_model_file_path, 
                object = best_model)
            
            logging.info("Model Training Complete... ")

        except Exception as e:
            raise CustomException(e, sys)

