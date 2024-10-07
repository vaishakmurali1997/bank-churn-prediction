import os
import sys
import numpy as np
import pandas as pd
import dill
from src.exceptions import CustomException

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, r2_score

def save_object (file_path, object): 
    try: 
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_object:
            dill.dump(object, file_object)
    except Exception as e: 
        raise CustomException(e, sys)

def evaluate_model (X_train, y_train, X_test, y_test, models):
    report = {}
    
    for model in range(len(list(models))):
        clf = list(models.values())[model]
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        score_report = accuracy_score(y_test, y_pred)
        report[list(models.keys())[model]] = score_report
    
    return report
