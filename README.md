# E-Commerce Supply Chain & Demand Forecasting Project 🚀

An end-to-end data engineering and data science project designed to optimize supply chain operations and forecast daily product demand. This project orchestrates a complete data pipeline starting from a relational database, moving through machine learning algorithms, and concluding with an interactive business intelligence dashboard.

---

## 📈 Project Architecture & Pipeline

[SQL Server] ──(Data Modeling & Views)──> [Python / Pandas] ──(Feature Engineering)──> [Random Forest Regressor] ──(Predictions)──> [SQL Server (Results Table)] ──> [Power BI Interactive Dashboard]

---

1. **Data Engineering (SQL Server):** Modeled raw relational database tables and constructed optimized views to aggregate transactional metrics into continuous daily time-series data.
2. **Data Science & ML (Python):** Developed an end-to-end script to handle missing dates (resampling), perform advanced feature engineering (lag features, calendar variations), train a Random Forest Regressor model, and validate the model's accuracy.
3. **Data Visualization (Power BI):** Integrated the prediction outputs back into SQL Server to design an executive-level operational dashboard highlighting actual vs. predicted inventory demands, total revenues, and seasonal sales trends.

---

## 📊 Business Intelligence Dashboard (Power BI)

Here is the interactive operational dashboard designed to guide supply chain managers and executive stakeholders in decision-making:

### 🔍 Actual vs. Predicted Demand Overview
![Power BI Dashboard Overview](powerbı.png)

### 📈 Detailed Sales Trends & Key Performance Indicators (KPIs)
![Power BI Dashboard Analytics](powerbı2.png)

---

## 🛠️ Tech Stack & Skills Demonstrated

* **Database & Engineering:** SQL Server, T-SQL, PyODBC, Relational Data Modeling, Views.
* **Data Science & Analytics:** Python, Pandas, NumPy, Scikit-Learn (Random Forest Regressor), Time-Series Resampling, Feature Engineering.
* **Evaluation Metrics:** Mean Absolute Error (MAE), Root Mean Squared Error (RMSE).
* **Business Intelligence:** Power BI Desktop, Data Modeling (1:1 Relationships), DAX, Interactive Report Designing.

---

## 🚀 How to Run the Project

1. **Database Setup:** Run the script in `v_DailySupplyChainForecast.sql` on your local SQL Server instance to generate the core analytical view.
2. **Model Training & Extraction:** Execute the Python pipeline to extract data, engineer time-series features, train the predictive model, and export results back to the database:
   ```bash
   python supply_chain_forecast.py

Dashboard Reporting: Open ecommerce_supply_chain_project.pbix via Power BI Desktop, refresh the data source using your local SQL Server credentials , and explore the insights!
