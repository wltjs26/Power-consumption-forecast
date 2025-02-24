- Overview
1. **Introduction**

      - This project developed an AI model to predict power consumption based on building types and spatiotemporal information. The training data included information on temperature, wind speed, humidity, and other factors for 100 buildings. XGBoost and Random Forest models were used to predict power consumption. Evaluation results showed that the Random Forest model predicted with high accuracy (R²=0.995), but additional model improvements are needed for specific building types and exceptional situations such as holidays.

1. **Result**

    - The Random Forest model accurately predicted power consumption across most building types, effectively reflecting key factors such as seasonality and time of day. However, for certain outlier data points (e.g., holidays and specific building types), additional feature engineering or model improvement is needed. These results are expected to provide practical support for power usage management and energy optimization strategies.

## 📊 Prediction Results
Here is the predicted power consumption:

![Prediction Result](https://github.com/wltjs26/Power-consumption-forecast/blob/main/prediction_result.png)
