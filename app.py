import streamlit as st
import pickle
import requests
import os

# Download the model file from Google Drive
@st.cache_resource
def load_model():
    file_id = "1hEO4k_AxfRdnpJf2iOJFK8mAzBUwOSen"  # Replace with your actual Google Drive file ID
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url, stream=True)
    with open("newton_model.pkl", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    # Load the model
    with open("newton_model.pkl", "rb") as f:
        return pickle.load(f)

# Load the model
try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

# Streamlit app
st.title("Newton's Second Law Calculator 🌟")
st.write("**Calculate Force, Mass, or Acceleration using Newton's Second Law (F = ma)**")

# Select the unknown variable
unknown = st.selectbox("Select the variable to calculate:", ["Force (F)", "Mass (m)", "Acceleration (a)"])

# Input fields for known variables
if unknown == "Force (F)":
    st.subheader("Calculate Force (F)")
    mass = st.number_input("Enter Mass (m) in kg:", min_value=0.01, value=10.0, step=0.01)
    acceleration = st.number_input("Enter Acceleration (a) in m/s²:", min_value=0.01, value=5.0, step=0.01)
    if st.button("Calculate Force (F)"):
        force = model.predict([[mass, acceleration]])[0]
        st.success(f"Calculated Force: {force:.2f} N")
elif unknown == "Mass (m)":
    st.subheader("Calculate Mass (m)")
    force = st.number_input("Enter Force (F) in N:", min_value=0.01, value=50.0, step=0.01)
    acceleration = st.number_input("Enter Acceleration (a) in m/s²:", min_value=0.01, value=5.0, step=0.01)
    if st.button("Calculate Mass (m)"):
        mass = force / acceleration
        st.success(f"Calculated Mass: {mass:.2f} kg")
else:  # Acceleration (a)
    st.subheader("Calculate Acceleration (a)")
    force = st.number_input("Enter Force (F) in N:", min_value=0.01, value=50.0, step=0.01)
    mass = st.number_input("Enter Mass (m) in kg:", min_value=0.01, value=10.0, step=0.01)
    if st.button("Calculate Acceleration (a)"):
        acceleration = force / mass
        st.success(f"Calculated Acceleration: {acceleration:.2f} m/s²")

# Add some aesthetic elements
st.write("---")
st.write("**About**")
st.write("This app uses a Random Forest model to calculate Force based on Newton's Second Law.")
st.write("🌟 Built with ❤️ by [Dr. Fakhre Alam Khan]!")
