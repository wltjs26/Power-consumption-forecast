## 📄 Power Consumption Prediction AI Model Development
This repository contains an AI model for predicting power consumption using building and spatiotemporal data.

🔹 Overview
Accurate power consumption prediction is crucial for stable and efficient energy supply.
This project leverages simulation models to develop an AI algorithm capable of predicting power consumption.

📌 Objective:
Develop a model that predicts power consumption at specific time points using building and spatiotemporal data.

📄 Full Report:
📑 Click here to view the full report (https://github.com/wltjs26/Power-consumption-forecast/blob/main/%5BReport%5D%20Power%20Consumption%20Prediction%20AI%20Model%20Development.docx)


🔹 Data Information
Training Data
100 buildings' data from June 1, 2022 – August 24, 2022
Includes temperature, precipitation, wind speed, humidity, solar radiation, solar energy, and power consumption (kWh) at hourly intervals.
Building Information
Includes building type, total area, cooling area, solar capacity, ESS storage capacity, and PCS capacity.
Validation Data
Forecast data from August 25, 2022 – August 31, 2022
Includes temperature, precipitation, wind speed, and humidity.
🔹 Data Preprocessing
(1) Initial Data Preparation
Datetime Conversion: Convert the datetime column into a proper date-time format.
Sorting & Index Reset: Ensure consistency by sorting data chronologically and grouping by building_type.
(2) Adding Weekday and Weekend Indicators
Weekday Indicator: 0-6 (Monday to Sunday)
Weekend Indicator: True/False
(3) Setting Holiday Conditions by Building Type
Discount Mart: Holidays on 2nd & 4th Sundays of each month
Data Center: Operates 24/7, so holidays = 0
Other Buildings: Compared weekend vs weekday power consumption to assign holidays.
📌 Holiday Distribution by Building Type
Building Type	No Holiday	Holiday
Apartment	16320	0
Commercial	11712	4608
Data Center	10200	0
Department Store & Outlet	16320	0
Discount Mart	15360	960
Hospital	11712	4608
Hotel & Resort	16320	0
Knowledge Industry Center	11712	4608
Other Buildings	30600	0
Public	11712	4608
Research Center	11712	4608
University	11712	4608
🔹 Model Development
(1) Feature Engineering & Data Splitting
Feature Variables (X):
temperature, wind speed, humidity, total area, cooling area, parking, month, time of day, day of the week, holiday
Target Variable (y):
power_consumption_kWh
Train-Test Split:
Training: 80%
Validation: 20%
(2) Model Training
📌 Algorithms Used:
✅ Random Forest
✅ XGBoost

(3) Model Evaluation
Model	MSE	R² Score
Random Forest	30,290.97	0.9951
XGBoost	150,683	0.9754
📌 Random Forest outperformed XGBoost with higher accuracy (lower MSE, higher R²).

(4) Final Model Prediction
Random Forest was applied to test data for final predictions.
Results visualization:
📊 Predicted power consumption values after the red dotted line.
🔹 Conclusion
The Random Forest model effectively predicted power consumption across most building types.
Seasonality & time-of-day effects were well captured.
Challenges:
Some outliers (holidays, specific building types) require further feature engineering & model improvements.
Practical Impact:
This model can help in power usage management & energy optimization strategies.
📄 Full Report:
📑 Click here to view the full report

🚀 Future Work

Improve feature engineering to better handle holidays.
Explore deep learning models (LSTMs, CNNs) for time series forecasting.
Optimize hyperparameters for XGBoost to improve performance.
