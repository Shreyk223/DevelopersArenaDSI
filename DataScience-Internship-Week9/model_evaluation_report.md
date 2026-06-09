# 📈 Data Analysis Project Report: House Price Prediction (Machine Learning)

## 📌 Project Description
This project represents a complete, end-to-end Machine Learning workflow that solves a critical real estate valuation challenge. By ingesting, cleaning, and encoding a dataset of 300 properties (`house_data.csv`), this project bridges the gap between exploratory data analysis and predictive AI. Two distinct models were developed: a baseline Linear Regression model and an advanced Random Forest Regressor. The project culminates in a highly accurate predictive model (97.11% variance explained) capable of automating property valuations based on structural and locational attributes.

---

## 🎯 Objectives
- **Data Engineering & Preprocessing:** Handle categorical variables via One-Hot Encoding to ensure mathematical compatibility with machine learning algorithms.
- **Cross-Validation Prep:** Implement a strict 80/20 Train-Test split to ensure models are evaluated on completely unseen data, preventing overfitting.
- **Model Development:** Train both a baseline model (`LinearRegression`) and an advanced ensemble algorithm (`RandomForestRegressor`).
- **Performance Evaluation:** Utilize `scikit-learn` metrics to calculate Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R² Scores.
- **Actionable Recommendations:** Extract "Feature Importances" from the decision trees to advise stakeholders on which housing attributes drive the most financial value.

---

## 🛠️ Technical Requirements Implemented
- **Categorical Encoding:** Implemented `pd.get_dummies(drop_first=True)` to convert categorical strings (Location, Property Type) into ML-ready binary matrices, avoiding the dummy variable trap.
- **Data Splitting:** Utilized `train_test_split(test_size=0.2, random_state=42)` to isolate 60 records strictly for unbiased model evaluation.
- **Ensemble Learning:** Deployed `RandomForestRegressor(n_estimators=100)` to capture complex, non-linear relationships between variables (e.g., how an extra bedroom's value changes depending on if it's in the city vs. rural).
- **Advanced Visualizations:** Deployed `matplotlib` and `seaborn` to build predictive accuracy charts (Actual vs. Predicted scatter plots with baseline regression lines) and Feature Importance bar charts.

---

## 🧮 Data Manipulation & Statistical Logic
The program utilizes the following advanced machine learning logic to process and predict the data:

| Operation Performed | Python Logic Used | Business Insight / Purpose |
|---------------------|-------------------|----------------------------|
| **Feature Encoding** | `pd.get_dummies(df, columns=['Location'])` | Transforms text-based locational data into binary numbers so the AI algorithm can process it mathematically. |
| **Data Splitting** | `train_test_split(X, y, test_size=0.2)` | Hides 20% of the data from the model during training to ensure the final accuracy score reflects real-world performance. |
| **Model Training** | `rf_model.fit(X_train, y_train)` | Feeds the structural data into 100 decision trees to learn the complex mathematical patterns dictating house prices. |
| **Model Prediction** | `rf_model.predict(X_test)` | Forces the model to guess the prices of the 60 hidden houses to test its applied accuracy. |
| **Accuracy Scoring** | `r2_score(y_test, rf_preds)` | Calculates the percentage of variance explained by the model to determine overall reliability (Result: 97.11%). |

---

## ⚙️ Setup & Installation
1. Install Python on your system (3.8+ recommended)
2. Install required machine learning libraries by running: `pip install pandas numpy scikit-learn matplotlib seaborn jupyter`
3. Download or clone this repository
4. Ensure `house_data.csv` is placed in the root directory
5. Run the notebook using Jupyter, executing it sequentially (`house_price_prediction.ipynb`)

---

## 📊 Sample Input
*The pipeline processes raw structural and locational data to predict financial value. Here is a sample of the data being evaluated:*

**Property Data:** Area: 3712 sq_ft | Bedrooms: 4 | Bathrooms: 3 | Age: 36 | Location: Rural | Type: House
**Actual Price:** $22,260,000

## 📊 Result for Sample Data:
========================================
✅ Models trained successfully!

--- Linear Regression Performance ---
MAE: $2,188,736.34
R² Score: 0.9406

--- Random Forest Regressor Performance ---
MAE: $1,493,949.17
R² Score: 0.9711

→ RESULT: Random Forest significantly outperforms baseline. 
→ INSIGHT: Area (Square Footage) and Location Zoning are the top two drivers of pricing variance.
========================================

---

## 📂 Project Files
- `house_price_prediction.ipynb` – Main Python machine learning pipeline
- `README.md` – Project description and documentation
- `house_data.csv` – Primary training and testing dataset
- `requirements.txt` – Dependencies (pandas, scikit-learn, seaborn, etc.)
- `predictions_vs_actual.png` - Visual documentation of the model's predictive accuracy
- `model_evaluation_report.md` - Deep-dive into model selection, methodology, and feature importance insights
