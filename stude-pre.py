import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Connection
uri = "mongodb+srv://mdmoazzamali984:amug786@cluster0.jzrdt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['student']
collection = db["student_pred"]

# Load Model
@st.cache_resource
def load_model():
    with open("student_lr_final_model.pkl", 'rb') as file:
        model, scaler, le = pickle.load(file)
    return model, scaler, le

# Preprocessing Function
def preprocessing_input_data(data, scaler, le):
    data['Extracurricular Activities'] = le.transform([data['Extracurricular Activities']])
    df = pd.DataFrame([data])
    df_transformed = scaler.transform(df)
    return df_transformed

# Prediction Function
def predict_data(data):
    model, scaler, le = load_model()
    processed_data = preprocessing_input_data(data, scaler, le)
    prediction = model.predict(processed_data)
    return prediction

# Function to Retrieve Stored Data from MongoDB
def fetch_stored_predictions():
    records = collection.find({}, {"_id": 0})  # Exclude MongoDB's default `_id` field
    return list(records)

# Main Streamlit App
def main():
    st.title("Student Performance Prediction")
    st.write("Enter your data to predict your performance")

    # Input Fields
    hours_studied = st.number_input("Hours Studied", min_value=1, max_value=10, value=5)
    previous_score = st.number_input("Previous Scores", min_value=40, max_value=100, value=70)
    Extra = st.selectbox("Extracurricular Activities", ['Yes', 'No'])
    sleeping_hours = st.number_input("Sleep Hours", min_value=4, max_value=10, value=7)
    sample_solved = st.number_input("Sample Question Papers Practiced", min_value=0, max_value=10, value=5)

    # Predict Button
    if st.button("Predict Score"):
        user_data = {
            "Hours Studied": hours_studied,
            "Previous Scores": previous_score,
            "Extracurricular Activities": Extra,
            "Sleep Hours": sleeping_hours,
            "Sample Question Papers Practiced": sample_solved
        }

        prediction = predict_data(user_data)
        st.success(f"Your prediction result is: {prediction[0]}")

        # Convert numpy data for MongoDB storage
        user_data["Prediction"] = prediction[0]
        for key, value in user_data.items():
            if isinstance(value, np.ndarray):
                user_data[key] = value.tolist()

        # Store in MongoDB
        collection.insert_one(user_data)
        st.write("Prediction stored in database!")

if __name__ == "__main__":
    main()
