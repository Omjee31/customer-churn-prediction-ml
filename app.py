import streamlit as st
import pickle
import numpy as np

# =========================
# Load files
# =========================
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.set_page_config(page_title="Churn Predictor", layout="centered")

st.title("📊 Customer Churn Prediction")
st.write("Fill only important details 👇")

# =========================
# INPUT SECTIONS
# =========================

st.subheader("👤 Customer Info")
gender = st.selectbox("Gender", ["Male", "Female"])
SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])

st.subheader("📡 Services")
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

st.subheader("💳 Billing Info")
tenure = st.slider("Tenure (months)", 0, 72, 12)
MonthlyCharges = st.slider("Monthly Charges", 0, 200, 70)
TotalCharges = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)

payment = st.selectbox("Payment Method", [
    "Bank transfer (automatic)",
    "Credit card (automatic)",
    "Electronic check",
    "Mailed check"
])

# =========================
# DEFAULT VALUES (Hidden)
# =========================
input_dict = {col: 0 for col in columns}

input_dict["gender"] = 1 if gender == "Male" else 0
input_dict["SeniorCitizen"] = SeniorCitizen

# default values (hidden)
input_dict["Partner"] = 1
input_dict["Dependents"] = 0
input_dict["PhoneService"] = 1
input_dict["MultipleLines"] = 0
input_dict["OnlineSecurity"] = 0
input_dict["OnlineBackup"] = 0
input_dict["DeviceProtection"] = 0
input_dict["TechSupport"] = 0
input_dict["StreamingTV"] = 0
input_dict["StreamingMovies"] = 0
input_dict["PaperlessBilling"] = 1

# user inputs
input_dict["tenure"] = tenure
input_dict["MonthlyCharges"] = MonthlyCharges
input_dict["TotalCharges"] = TotalCharges

# one-hot encoding
input_dict[f"InternetService_{internet}"] = 1
input_dict[f"Contract_{contract}"] = 1
input_dict[f"PaymentMethod_{payment}"] = 1

# =========================
# Convert to array
# =========================
input_data = np.array([list(input_dict.values())])

# scale
cols_to_scale = ['tenure', 'MonthlyCharges', 'TotalCharges']
indices = [columns.index(col) for col in cols_to_scale]

input_data[:, indices] = scaler.transform(input_data[:, indices])

# =========================
# Prediction
# =========================
if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    st.subheader("📈 Result")

    if prediction == 1:
        st.error(f"⚠️ High Risk of Churn ({prob:.2f})")
        st.write("💡 Customer may leave due to high charges or weak contract.")
    else:
        st.success(f"✅ Low Risk of Churn ({prob:.2f})")
        st.write("💡 Customer likely to stay with current plan.")