# ✈️ Flight Price Predictor

A Streamlit web app that predicts flight ticket prices based on user inputs like airline, source, destination, stops, and flight times.  
It uses a machine learning model trained on real-world flight data.

🔗 **Live Demo:** [https://flightpricepredictor-wfxpnhuxqx5hwrlmjswcif.streamlit.app/](#)

---

## 🚀 Features

- Predicts flight prices using a trained Random Forest model
- Clean and interactive Streamlit UI
- Automatically handles time, duration, and stop conversions
- Real-time prediction on user input

---

## 🧠 Model Details

- Preprocessing includes time-based feature extraction (hour, minute, day, month)
- One-hot encoding of categorical features like Airline, Source, etc.
- Random Forest Regressor trained on cleaned dataset
- Evaluation using MAE and R² score

---

## 🔍 Use Cases and Insights

### 📊 Use Case: Airline vs. Price Analysis
> How does the choice of airline influence pricing?
- _Hint: Some low-cost carriers consistently show cheaper prices._
- 📷 ![airline vs price](https://github.com/user-attachments/assets/9a3f7506-4a72-440c-829b-c43f9a592731)

---

### ⛔ Use Case: Do Total Stops Affect the Price?
> Direct vs 1-stop vs multi-stop — is cheaper always slower?
- 📷 _Add bar chart comparing stops vs avg price_  
![total_stops](https://github.com/user-attachments/assets/318a02b2-acca-4599-b5c3-75fe9c6950a4)


---

### ⏱ Use Case: Does Duration Impact Flight Price?
> Longer flights cost more? Or is it the route and airline?
- 📷 _Add scatterplot or boxplot for Duration vs Price_  
![image](https://github.com/user-attachments/assets/3cab6cbd-b9ec-41eb-b540-7617c5b1e2cf)


---

### 📅 Case Study: When Do Most Flights Take Off?
> Analyze popular departure times and their effect on price.
- 📷 _Add histogram of departure hours_  
![flight_time](https://github.com/user-attachments/assets/d557229c-721e-443f-875b-35defd597a55)


---

## 🛠️ How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/flight-price-predictor.git
   cd flight-price-predictor
