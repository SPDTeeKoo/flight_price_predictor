import streamlit as st
import pandas as pd
import numpy as np
import pickle
import datetime

# Load model and training column names
model = pickle.load(open("flight_price_model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

# UI
st.title("✈️ Flight Price Predictor")

# Input fields
airline = st.selectbox("Airline", ["IndiGo", "Air India", "SpiceJet", "Vistara", "GoAir", "Multiple carriers"])
source = st.selectbox("Source", ["Delhi", "Kolkata", "Mumbai", "Chennai", "Banglore"])
destination = st.selectbox("Destination", ["Cochin", "Delhi", "New Delhi", "Hyderabad", "Kolkata"])
date_of_journey = st.date_input("Journey Date", datetime.date(2024, 1, 1))
dep_time = st.time_input("Departure Time", datetime.time(10, 0))
arrival_time = st.time_input("Arrival Time", datetime.time(12, 0))
stops = st.selectbox("Total Stops", ["non-stop", "1 stop", "2 stops", "3 stops", "4 stops"])
additional_info = st.selectbox("Additional Info", ["No info", "In-flight meal not included", "No check-in baggage included", "1 Long layover", "Business class"])

# Duration
dep_datetime = datetime.datetime.combine(datetime.date.min, dep_time)
arr_datetime = datetime.datetime.combine(datetime.date.min, arrival_time)
if arr_datetime < dep_datetime:
    arr_datetime += datetime.timedelta(days=1)
duration = arr_datetime - dep_datetime
duration_hour = duration.seconds // 3600
duration_minute = (duration.seconds // 60) % 60

# Preprocess user input
def preprocess_input():
    df = pd.DataFrame({
        'Airline': [airline],
        'Source': [source],
        'Destination': [destination],
        'Date_of_Journey': [date_of_journey.strftime("%d/%m/%Y")],
        'Dep_Time': [dep_time.strftime("%H:%M")],
        'Arrival_Time': [arrival_time.strftime("%H:%M")],
        'Duration': [f"{duration_hour}h {duration_minute}m"],
        'Total_Stops': [stops],
        'Additional_Info': [additional_info]
    })

    # Feature engineering
    df["Journey_day"] = pd.to_datetime(df["Date_of_Journey"], format="%d/%m/%Y").dt.day
    df["Journey_month"] = pd.to_datetime(df["Date_of_Journey"], format="%d/%m/%Y").dt.month
    df["Dep_hour"] = pd.to_datetime(df["Dep_Time"]).dt.hour
    df["Dep_minute"] = pd.to_datetime(df["Dep_Time"]).dt.minute
    df["Arrival_hour"] = pd.to_datetime(df["Arrival_Time"]).dt.hour
    df["Arrival_minute"] = pd.to_datetime(df["Arrival_Time"]).dt.minute
    df["Duration_hour"] = duration_hour
    df["Duration_minute"] = duration_minute

    # Clean Total_Stops
    df["Total_Stops"] = df["Total_Stops"].replace({
        "non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4
    }).astype(int)

    # Drop raw cols
    df.drop(["Date_of_Journey", "Dep_Time", "Arrival_Time", "Duration"], axis=1, inplace=True)

    # One-hot encode
    df = pd.get_dummies(df, drop_first=True)

    # Add missing columns
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0

    # Align with model
    df = df[model_columns]

    return df

# Predict button
if st.button("Predict Flight Price"):
    input_df = preprocess_input()
    prediction = model.predict(input_df)
    st.success(f"Estimated Flight Price: ₹{int(prediction[0])}")
