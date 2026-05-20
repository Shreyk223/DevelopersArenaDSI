# 📈 Data Analysis Project Report: Customer Sales & Churn Analysis

## 📌 Project Description
This project represents an advanced relational data analysis pipeline built using Python. By leveraging the pandas library, disconnected sales and customer retention databases are cleaned, transformed, and merged. The analysis focuses on extracting deep insights into purchasing behavior, localized cross-selling patterns, and customer churn vulnerabilities, culminating in a multi-chart executive dashboard generated via matplotlib.

## 🎯 Objectives
-Build an advanced data manipulation pipeline: Clean -> Extract -> Merge -> Pivot -> Visualize.
-Solve primary key mismatches between datasets using string manipulation.
-Perform time-series grouping by extracting months and years from raw datetime strings.
-Utilize matplotlib.pyplot subplots to generate a unified 4-chart executive dashboard.
-Extract and document meaningful business insights regarding customer lifetime value and retention.

## 🛠️ Technical Requirements Implemented
-String Operations & Cleaning: Used .str.replace() to strip alphabetical characters from mismatched IDs, allowing for a clean relational database join.
-Relational Data Merging: Implemented pd.merge(how='inner') to combine sales transactions with customer profiles based on a unified primary key.
-Advanced Aggregation: Utilized pd.pivot_table() to create multidimensional summaries (Region vs. Product) and applied multi-conditional filtering (&) to isolate VIP customer segments.
-Subplot Visualization: Integrated plt.subplots(2, 2) to render a 2x2 grid containing line charts, horizontal bar charts, vertical bar charts, and scatter plots, saving the unified dashboard as a high-resolution image.

## 🧮 Data Manipulation & Visualization Logic
The program utilizes the following advanced pandas logic to process and visualize the relational data:

Operation Performed	Python Logic Used	Business Insight / Purpose
Data Merging	pd.merge(sales, churn, on='CustNum', how='inner')	Combines transactional data with demographic data to see who is buying what.
Pivot Table Summary	pd.pivot_table(df, index='Region', columns='Product', aggfunc='sum')	Identifies cross-selling patterns, revealing which specific products dominate in which specific regions.
Multi-Condition Filtering	df[(df['Total_Sales'] > 100k) & (df['Tenure'] >= 12)]	Isolates the "VIP Segment" to prove that high-value, long-term customers have a 0% churn rate.
Dashboard Grid	fig, axs = plt.subplots(2, 2)	Consolidates monthly trends, product performance, top customers, and churn risk into a single executive view.

## ⚙️ Setup & Installation
-Install Python on your system
-Install required libraries by running: pip install pandas matplotlib jupyter
-Download or clone this repository
-Ensure sales_data.csv and customer_data.csv are placed in the root directory
-Run the notebook using Jupyter, or execute the script using: python customer_analysis.py

## 📊 Sample Input
The pipeline processes two separate datasets. Here is a sample of the raw data being joined:

Sales Data: Date: 2024-01-01 | Product: Phone | Customer_ID: CUST001 | Total_Sales: 261100

Customer Data: CustomerID: C00001 | Tenure: 6 | MonthlyCharges: 64 | Churn: 0

## 📊 Result for Sample Data:
======================================== 🔗 Datasets merged successfully. Total records: 100

### 📊 QUICK METRICS: Total Revenue: ₹12,365,048.00 Average Order: ₹123,650.48 Top Customer: CUST016 (₹373,932.00)

🎨 Generating Sales Dashboard... 

## 📂 Project Files
customer_analysis.ipynb – Main Python data pipeline notebook
analysis_report.pdf – Final business analysis and executive summary
sales_data.csv – Raw transactional dataset
requirements.txt – Dependencies (pandas, matplotlib, jupyter)
plotly.gif - Demo plotly visualization
