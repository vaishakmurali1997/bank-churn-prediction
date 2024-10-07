from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline


application = Flask(__name__)
app = application

@app.route('/')
def index():
    return 'Connected to application'

@app.route('/predict', methods=['POST'])
def prediction():
    data=CustomData(
        creditScore = request.form.get('creditScore'),
        age = request.form.get('age'),
        gender = request.form.get('gender'),
        geography = request.form.get('geography'),
        tenure = request.form.get('tenure'),
        balance = request.form.get('balance'),
        numOfProducts = request.form.get('numOfProducts'),
        hasCrCard = request.form.get('hasCrCard'),
        isActiveMember = request.form.get('isActiveMember'),
        estimatedSalary = request.form.get('estimatedSalary')
    )

    prediction_data = data.get_data_frame()
    print(prediction_data)
    
    predict_pipeline = PredictPipeline()
    result = predict_pipeline.predict(prediction_data)
    return jsonify({'churn': int(result[0])})

if __name__ == "__main__" :
    app.run(host="0.0.0.0", debug=True)
