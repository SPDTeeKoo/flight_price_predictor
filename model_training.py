import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
df = pd.read_excel("Data_Train.xlsx")  

# Drop rows with missing Price
df.dropna(subset=["Price"], inplace=True)

# Fill missing categorical values with 'No info'
df["Additional_Info"].fillna("No info", inplace=True)
df["Total_Stops"].fillna("1 stop", inplace=True)

# Drop rows with missing Duration or Price
df.dropna(subset=["Duration"], inplace=True)

# Feature Engineering
df["Journey_day"] = pd.to_datetime(df["Date_of_Journey"], format="%d/%m/%Y").dt.day
df["Journey_month"] = pd.to_datetime(df["Date_of_Journey"], format="%d/%m/%Y").dt.month

df["Dep_hour"] = pd.to_datetime(df["Dep_Time"]).dt.hour
df["Dep_minute"] = pd.to_datetime(df["Dep_Time"]).dt.minute

df["Arrival_hour"] = pd.to_datetime(df["Arrival_Time"]).dt.hour
df["Arrival_minute"] = pd.to_datetime(df["Arrival_Time"]).dt.minute

# Duration processing
df["Duration_hour"] = df["Duration"].str.extract('(\d+)h').fillna(0).astype(int)
df["Duration_minute"] = df["Duration"].str.extract('(\d+)m').fillna(0).astype(int)

# Clean stops
df["Total_Stops"] = df["Total_Stops"].replace({
    'non-stop': 0,
    '1 stop': 1,
    '2 stops': 2,
    '3 stops': 3,
    '4 stops': 4
}).astype(int)

# Drop unused columns
df.drop(["Route", "Date_of_Journey", "Dep_Time", "Arrival_Time", "Duration"], axis=1, inplace=True)

# One-hot encoding
df = pd.get_dummies(df, drop_first=True)

# Features and target
X = df.drop("Price", axis=1)
y = df["Price"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Evaluation
pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, pred))
print("R2 Score:", r2_score(y_test, pred))

# Save model and column names
with open("flight_price_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model_columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("✅ Model and columns saved!")
