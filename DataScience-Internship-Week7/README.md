# 📈 Data Analysis Project Report: Statistical Business Analysis

## 📌 Project Description
This project represents an advanced statistical business analysis pipeline built using Python. By leveraging the `scipy`, `statsmodels`, and `pandas` libraries, raw e-commerce and customer retention data are transformed into mathematically validated business insights. The analysis focuses on testing data distributions, generating confidence intervals, proving correlations, and executing rigorous hypothesis testing to empower data-driven decision-making.

---

## 🎯 Objectives
- Utilize the `scipy.stats` library for advanced hypothesis testing (T-tests, ANOVA, Shapiro-Wilk).
- Generate exact p-values to mathematically prove or disprove business assumptions.
- Calculate 95% Confidence Intervals to determine exact margins of error for revenue projections.
- Build an Ordinary Least Squares (OLS) Linear Regression model to quantify variance.
- Consolidate statistical output into an actionable, non-technical executive summary.

---

## 🛠️ Technical Requirements Implemented
- **Data Distributions:** Used `stats.shapiro()` to test for normality, mathematically proving the sales data is right-skewed and non-normal.
- **Hypothesis Testing:** Implemented `stats.ttest_ind()` and `stats.f_oneway()` to evaluate demographic and regional variance against total sales and churn rates.
- **Regression Modeling:** Leveraged `statsmodels.api` to fit a linear regression model, calculating R-squared to define the exact mathematical impact of volume on revenue.
- **Confidence Intervals:** Deployed `stats.t.ppf()` and `stats.sem()` to establish a strict 95% confidence boundary for the population mean.

---

## 🧮 Data Manipulation & Statistical Logic
The program utilizes the following advanced statistical logic to process and present the data:

| Operation Performed | Python Logic Used | Business Insight / Purpose |
|---------------------|-------------------|----------------------------|
| **Normality Test** | `stats.shapiro(sales['Total_Sales'])` | Evaluates if the data follows a bell curve. (Result: Non-normal, highly skewed by VIP purchases). |
| **Independent T-Test** | `stats.ttest_ind(churn_yes, churn_no)` | Compares the average monthly charges of churned vs. retained customers to see if pricing drives churn. |
| **ANOVA Testing** | `stats.f_oneway(*regions)` | Evaluates multiple categories simultaneously to see if geography significantly impacts sales averages. |
| **Confidence Interval**| `stats.t.ppf((1 + 0.95) / 2., n-1)` | Calculates the exact margin of error, allowing the business to project minimum and maximum average revenue accurately. |
| **Linear Regression** | `sm.OLS(Y, X).fit()` | Builds a mathematical model to quantify exactly how much total revenue variance is dictated purely by quantity sold. |

---

## ⚙️ Setup & Installation
1. Install Python on your system
2. Install required libraries by running: `pip install pandas numpy scipy statsmodels matplotlib seaborn jupyter`
3. Download or clone this repository
4. Ensure `sales_data.csv` and `customer_churn.csv` are placed in the root directory
5. Run the notebook using Jupyter: `jupyter notebook statistical_analysis.ipynb`

---

## 📊 Sample Input
*The pipeline processes raw transactional and retention data. Here is a sample of the data being evaluated:*

**Sales Data:**
Date: 2024-01-01 | Product: Phone | Quantity: 7 | Price: 37300 | Region: East | Total_Sales: 261100

## 📊 Result for Sample Data:
========================================
✅ Data loaded successfully.
Descriptive Statistics Calculated.
Shapiro-Wilk Test for Normality - p-value: 0.00000
Data is NOT normally distributed (Reject H0)
T-test (Churn vs MonthlyCharges) p-value: 0.0163
Average Total Sales: ₹123,650.48 ± ₹19,874.13
Linear Regression R-squared: 0.4735
========================================

---

## 📂 Project Files
- `statistical_analysis.ipynb` – Main Python statistical analysis notebook
- `README.md` – Project description
- `sales_data.csv` & `customer_churn.csv` – Raw datasets
- `hypothesis_tests_results.txt` – Exported plain-text results of exact p-values
- `requirements.txt` – Dependencies (pandas, scipy, statsmodels, etc.)
- `Statistical_Analysis_Report.pdf` - Final business analysis and executive summary
