import streamlit as st
import pandas as pd
import joblib
import os

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Personalized E-Commerce Fraud Prevention",
    page_icon="🛒",
    layout="wide"
)

# ==========================================
# LOAD MODEL & SCALER
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "best_fraud_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "scaler.pkl")

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    st.error(f"Error Loading Model : {e}")
    st.stop()

# ==========================================
# TITLE
# ==========================================
st.markdown(
    "<h1 style='text-align:center;'>🛒 Personalized E-Commerce Fraud Prevention</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("📌 Project Details")

st.sidebar.success("Personalized E-Commerce Fraud Prevention")

st.sidebar.info("Algorithm : Logistic Regression")

st.sidebar.success("Accuracy : 87.65 %")

st.sidebar.write("Developer : Praveen N")

st.sidebar.write("Department : B.E CSE (Cyber Security)")

# ==========================================
# INPUT FORM
# ==========================================

st.subheader("Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:

    transaction_id = st.number_input("Transaction ID", 1, value=1001)

    customer_id = st.number_input("Customer ID", 1, value=501)

    age = st.number_input("Age", 18, 100, value=25)

    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    gender = 0 if gender == "Female" else 1

    product_category = st.number_input(
        "Product Category",
        min_value=0,
        value=0
    )

    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=1000.0
    )

    payment_method = st.number_input(
        "Payment Method",
        min_value=0,
        value=0
    )

with col2:

    device = st.number_input(
        "Device",
        min_value=0,
        value=0
    )

    browser = st.number_input(
        "Browser",
        min_value=0,
        value=0
    )

    country = st.number_input(
        "Country",
        min_value=0,
        value=0
    )

    ip_address = st.number_input(
        "IP Address",
        min_value=0,
        value=0
    )

    shipping_match = st.selectbox(
        "Shipping Address Match",
        ["No", "Yes"]
    )

    shipping_match = 1 if shipping_match == "Yes" else 0

    transaction_hour = st.slider(
        "Transaction Hour",
        0,
        23,
        12
    )

    transaction_day = st.slider(
        "Transaction Day",
        1,
        31,
        15
    )

    transaction_month = st.slider(
        "Transaction Month",
        1,
        12,
        6
    )

# ==========================================
# PREDICT
# ==========================================

if st.button("🔍 Predict Fraud", use_container_width=True):

    input_df = pd.DataFrame([[
        transaction_id,
        customer_id,
        age,
        gender,
        product_category,
        amount,
        payment_method,
        device,
        browser,
        country,
        ip_address,
        shipping_match,
        transaction_hour,
        transaction_day,
        transaction_month
    ]], columns=[
        "Transaction_ID",
        "Customer_ID",
        "Age",
        "Gender",
        "Product_Category",
        "Amount",
        "Payment_Method",
        "Device",
        "Browser",
        "Country",
        "IP_Address",
        "Shipping_Address_Match",
        "Transaction_Hour",
        "Transaction_Day",
        "Transaction_Month"
    ])

    try:

        # Scale Input
        input_scaled = scaler.transform(input_df)

        # Prediction
        prediction = model.predict(input_scaled)

        st.markdown("---")

        st.subheader("Prediction Result")

        if prediction[0] == 1:
            st.error("🚨 Fraud Transaction")
        else:
            st.success("✅ Legitimate Transaction")

        if hasattr(model, "predict_proba"):

            probability = model.predict_proba(input_scaled)[0]

            st.write("### Prediction Confidence")

            st.progress(float(max(probability)))

            st.write(
                f"✅ Legitimate : {probability[0]*100:.2f}%"
            )

            st.write(
                f"🚨 Fraud : {probability[1]*100:.2f}%"
            )

        with st.expander("View Input Data"):

            st.dataframe(input_df)

    except Exception as e:

        st.error(f"Prediction Error : {e}")

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
"""
<center>

<b>Developed by Praveen N</b>

<br>

B.E CSE (Cyber Security)

<br>

Machine Learning Project

</center>
""",
unsafe_allow_html=True
)