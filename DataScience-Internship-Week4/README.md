# 📈 Data Analysis Project Report: E-Commerce Sales Visualization

## 📌 Project Description
This project represents a complete, end-to-end data analysis pipeline built using Python. By leveraging the `pandas` library for data manipulation and the `matplotlib` library for visual rendering, a raw e-commerce dataset is transformed into actionable business intelligence. The analysis focuses on identifying high-performing product categories and mapping regional revenue distribution through automatically generated visual charts.

---

## 🎯 Objectives
- Build a complete programmatic data pipeline: Load -> Clean -> Analyze -> Visualize.
- Implement robust error handling (`try-except` blocks) to prevent program crashes during file operations.
- Utilize `matplotlib.pyplot` to generate at least two distinct chart types (Bar Chart and Pie Chart).
- Extract and document meaningful business insights based on the generated visualizations.

---

## 🛠️ Technical Requirements Implemented
- **Data Ingestion & Error Handling:** Used `pandas.read_csv()` wrapped in a `try-except` block to safely load the dataset and alert the user if the file is missing.
- **Data Cleaning:** Implemented `df.isnull().sum()` and `df.dropna()` to automatically detect and remove incomplete or corrupted records.
- **Data Aggregation:** Segregated data using `groupby()` to calculate sum totals across specific dimensions (Product and Region).
- **Data Visualization:** Integrated `matplotlib.pyplot` to render horizontal bar charts (`kind='barh'`) and pie charts (`kind='pie'`), programmatically saving high-resolution files (`dpi=300`) to a dedicated folder.

---

## 🧮 Data Visualization Logic
The program utilizes the following combined pandas and matplotlib logic to extract and visualize metrics from the raw data:

| Visualization Generated | Python Logic Used | Business Insight |
|-------------------------|-------------------|------------------|
| **Product Performance (Bar Chart)** | `df.groupby('Product')['Total_Sales'].sum().plot(kind='barh')` | Identifies a clear hierarchy of product performance, highlighting that high-ticket electronics drive the vast majority of revenue. |
| **Regional Distribution (Pie Chart)** | `df.groupby('Region')['Total_Sales'].sum().plot(kind='pie')` | Maps geographical dependencies, allowing for supply chain optimization in dominant regions (e.g., North and East). |

---

## ⚙️ Setup & Installation
1. Install Python on your system
2. Install required libraries by running: 'pip install matplotlib'
3. Download or clone this repository
4. Ensure `sales_data.csv` is placed inside the `data/` folder
5. Run the program using:
   `python main.py`

---

## 📊 Sample Input
*The dataset contains 100 transactional records. Here is a sample of the raw data being processed:*

Date: 2024-01-01
Product: Phone
Quantity: 7
Price: 37300
Customer_ID: CUST001
Region: East
Total_Sales: 261100

## 📊 Result for Sample Data:
========================================
🎨 GENERATING VISUALIZATIONS...
========================================
✅ Bar chart saved: visualizations/sales_by_product.png
✅ Pie chart saved: visualizations/sales_by_region.png

🎉 Pipeline complete! Charts are ready for your report.
========================================

---

## 📂 Project Files
- `main.py` – Main Python data pipeline script
- `data/sales_data.csv` – Raw dataset
- `visualizations/sales_by_product.png` – Output Bar Chart
- `visualizations/sales_by_region.png` – Output Pie Chart
- `requirements.txt` – Dependencies (pandas, matplotlib)

---

## 📚 What I Learned
From this project, I learned how to:
- Successfully combine `pandas` and `matplotlib` to handle both mathematical logic and visual output in a single script.
- Implement error handling (`try-except`) to gracefully manage missing files instead of crashing the program.
- Customize charts (adjusting DPI for high-resolution images, formatting labels, applying custom hex colors, and using `tight_layout()`).
- Realize the power of automated Python reporting over manual Excel charting; this script can now be reused infinitely on future datasets with zero manual effort.
