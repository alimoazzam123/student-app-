import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGO_URI = "mongodb+srv://mdmoazzamali984:amug786@cluster0.jzrdt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

@st.cache_resource  # Keeps MongoDB connection alive
def get_mongo_connection():
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    return client

# Get the cached connection
client = get_mongo_connection()
db = client['student']
collection = db["student_pred"]

# Check connection status
try:
    client.admin.command('ping')
    st.success("✅ Successfully connected to MongoDB!")
except Exception as e:
    st.error(f"❌ MongoDB connection failed: {e}")
