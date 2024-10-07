import streamlit as st
import requests

st.title("🏦 Bank Customer Churn Prediction")

# Sidebar for additional navigation or information
st.sidebar.header("About")
st.sidebar.info(
    "This application predicts whether a bank customer is likely to churn based on their profile. "
    "Please fill in the details below to make a prediction."
)

# Input fields for customer data
st.header("📊 Enter Customer Details")

with st.form(key='customer_form'):
    col1, col2 = st.columns(2)  

    with col1:
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=600, help="A higher score indicates better creditworthiness.")
        age = st.number_input("Age", min_value=18, max_value=100, value=30, help="Age of the customer.")
        tenure = st.number_input("Tenure (Years)", min_value=0, max_value=10, value=1, help="Number of years the customer has been with the bank.")
        balance = st.number_input("Account Balance", min_value=0, value=5000, help="Current balance in the customer's account.")
        has_cr_card = st.selectbox("Has Credit Card", ["Yes", "No"], help="Does the customer have a credit card?")
        
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"], help="Select the gender of the customer.")
        geography = st.selectbox("Geography", ["France", "Spain", "Germany"], help="Select the customer's country.")
        num_of_products = st.number_input("Number of Products", min_value=1, max_value=4, value=1, help="Number of products the customer has with the bank.")
        is_active_member = st.selectbox("Is Active Member", ["Yes", "No"], help="Is the customer an active member of the bank?")
        estimated_salary = st.number_input("Estimated Salary", min_value=0, value=50000, help="The estimated salary of the customer.")

    # Submit button
    submit_button = st.form_submit_button("Predict Churn")

# Handling prediction
if submit_button:
    # Convert inputs to the expected format
    gender_encoded = 1 if gender == "Male" else 0
    geography_encoded = 0 if geography == "France" else (1 if geography == "Spain" else 2)
    has_cr_card_encoded = 1 if has_cr_card == "Yes" else 0
    is_active_member_encoded = 1 if is_active_member == "Yes" else 0

    input_data = {
        'creditScore': credit_score,
        'age': age,
        'gender': gender,
        'geography': geography,
        'tenure': tenure,
        'balance': balance,
        'numOfProducts': num_of_products,
        'hasCrCard': has_cr_card_encoded,
        'isActiveMember': is_active_member_encoded,
        'estimatedSalary': estimated_salary
    }

    # Call the Flask API
    response = requests.post("http://localhost:5000/predict", data=input_data)
    prediction = response.json()

    # Display the prediction result
    st.subheader("Prediction Result")
    if prediction['churn'] == 1:
        st.error("🚨 This customer is likely to churn.")
    else:
        st.success("✅ This customer is likely to stay loyal.")
