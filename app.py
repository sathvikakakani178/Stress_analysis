import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# Load the trained model
model = joblib.load("stress_model.pkl")

# Set up the Streamlit app
def main():
    st.set_page_config(page_title="Stress Level Detection", layout="centered")
    st.title("🧠 Stress Level Detection App")
    st.markdown("This app predicts your stress level based on physiological and emotional parameters.")

    st.sidebar.header("Input Features")
    snoring_rate = st.sidebar.slider("Snoring Rate", 0.0, 100.0, 20.0)
    respiration_rate = st.sidebar.slider("Respiration Rate", 0.0, 40.0, 20.0)
    body_temperature = st.sidebar.slider("Body Temperature (°C)", 30.0, 45.0, 36.5)
    limb_movement = st.sidebar.slider("Limb Movement", 0.0, 100.0, 10.0)
    blood_oxygen = st.sidebar.slider("Blood Oxygen Level", 50.0, 100.0, 95.0)
    eye_movement = st.sidebar.slider("Rapid Eye Movement", 0.0, 100.0, 50.0)
    sleeping_hours = st.sidebar.slider("Sleeping Hours", 0.0, 12.0, 7.0)
    heart_rate = st.sidebar.slider("Heart Rate", 40.0, 180.0, 72.0)

    input_data = np.array([[snoring_rate, respiration_rate, body_temperature,
                            limb_movement, blood_oxygen, eye_movement,
                            sleeping_hours, heart_rate]])

    if st.button("Predict Stress Level"):
        try:
            # Optionally scale data if needed (you can remove if already scaled in training)
            scaler = StandardScaler()
            input_scaled = scaler.fit_transform(input_data)

            prediction = model.predict(input_scaled)
            stress_level = {
                0: "Low Stress 😌",
                1: "Medium Stress 😐",
                2: "High Stress 😣"
            }.get(prediction[0], "Unknown")

            st.success(f"Predicted Stress Level: **{stress_level}**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

if __name__ == "__main__":
    main()
