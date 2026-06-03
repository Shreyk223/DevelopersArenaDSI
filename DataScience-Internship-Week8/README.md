# 📈 Data Analysis Project Report: Capstone Business Analysis

## 📌 Project Description
This project represents a complete, real-world data science workflow that solves a critical business challenge: **Customer Lifetime Value (CLTV) and Churn Optimization**. By extracting, cleaning, and merging a CRM database (`customer_churn.csv`) with a POS transactional database (`sales_data.csv`), this project bridges the gap between technical data science (EDA, statistical hypothesis testing) and business intelligence. The capstone culminates in an executive implementation plan designed to reduce attrition and maximize cross-selling revenue based on mathematically validated insights.

---

## 🎯 Objectives
- **Data Engineering:** Solve primary key mismatches via string manipulation to successfully execute a Left Join, merging transactional data while preserving a core 500+ row demographic dataset.
- **End-to-End Analysis:** Execute a complete pipeline within a modular structure: Data Cleaning -> EDA -> Statistical Testing.
- **Hypothesis Validation:** Utilize `scipy.stats` to mathematically test assumptions rather than relying purely on observational visualization.
- **Actionable Recommendations:** Translate mathematical findings (T-tests, p-values) into a phased 90-day implementation plan for stakeholders.
- **Professional Documentation:** Deliver a 1-page Executive Summary, a Technical Report, and a Business Presentation.

---

## 🛠️ Technical Requirements Implemented
- **Relational Data Merging:** Implemented `pd.merge(how='left')` to append sparse hardware sales data to a 500-row subscription database without losing churn records.
- **Missing Data Imputation:** Utilized `fillna(0)` to mathematically impute `NaN` sales values post-join, allowing for continuous variable testing on subscription-only users.
- **Advanced Visualizations:** Deployed `seaborn` to build multi-chart matrices, including KDE plots for tenure density, Boxplots for spending distribution, and Pearson Correlation Heatmaps.
- **Hypothesis Testing:** Implemented `stats.ttest_ind()` to evaluate behavioral variances (e.g., hardware buyers vs. non-buyers) against total churn rates.

---

## 🧮 Data Manipulation & Statistical Logic
The program utilizes the following advanced logic to process and present the data:

| Operation Performed | Python Logic Used | Business Insight / Purpose |
|---------------------|-------------------|----------------------------|
| **Primary Key Formatting** | `df['CustomerID'].str.replace('C', '')` | Extracts integer values from mismatched string IDs to allow cross-database merging. |
| **Relational Merge** | `pd.merge(churn, sales, on='CustNum', how='left')` | Preserves the 500-row CRM database while attaching POS transaction data. |
| **Financial Density** | `sns.violinplot(x='Churn', y='CLTV')` | Maps the exact pricing threshold where customers experience "bill shock" and decide to cancel. |
| **Independent T-Test** | `stats.ttest_ind(churn_charges, retain_charges)` | Compares average monthly charges to mathematically prove if pricing drives churn. |
| **Cohort Grouping** | `pd.qcut(df['Tenure'], q=4)` | Divides customers into distinct lifespan brackets to pinpoint exactly *when* churn occurs. |

---

## ⚙️ Setup & Installation
1. Install Python on your system
2. Install required libraries by running: `pip install pandas numpy scipy matplotlib seaborn jupyter`
3. Download or clone this repository
4. Ensure `sales_data.csv` and `customer_churn.csv` are placed in the `data/` directory
5. Run the notebooks using Jupyter, executing them sequentially (`1_data_cleaning.ipynb` -> `2_eda.ipynb` -> `3_analysis.ipynb`)

---

## 📊 Sample Input
*The pipeline processes raw transactional and retention data. Here is a sample of the data being evaluated:*

**CRM Data:** CustomerID: C00002 | Tenure: 21 | MonthlyCharges: 113 | Contract: Month-to-month | Churn: 1
**POS Data:** Customer_ID: CUST002 | Product: Headphones | Quantity: 4 | Price: 15406 | Total_Sales: 61624

## 📊 Result for Sample Data:
========================================
✅ Data Cleaned and Merged Successfully.
Merged Dataset Shape: (500, 17) -> Requirement of 500+ rows met!

STATISTICAL HYPOTHESIS TESTING
TEST 1: Hardware Buyers vs Subscription-Only Churn
→ RESULT: Null Hypothesis Tested.

TEST 2: Churn vs Monthly Charges
p-value: 0.0163
→ RESULT: REJECT Null Hypothesis. High monthly charges significantly increase churn risk.
========================================

---

## 📂 Project Files
- `notebooks/` – Directory containing the modular Python analytical pipeline
- `README.md` – Project description and documentation
- `data/` – Directory containing the raw and cleaned datasets
- `requirements.txt` – Dependencies (pandas, scipy, seaborn, etc.)
- `reports/executive_summary.pdf` - business findings
- `reports/technical_report.pdf` - Deep-dive into ETL and algorithms
- `presentation/business_presentation.pptx` - Slide deck for stakeholder presentation
