# 📈 Data Analysis Project Report: Interactive Sales Dashboard

## 📌 Project Description
This project represents a data visualization mastery pipeline built using Python. By leveraging the `seaborn`, `matplotlib`, and `plotly` libraries, raw e-commerce data is transformed into a highly visual, interactive dashboard. The analysis focuses on understanding price distributions, regional purchase behaviors, numerical correlations, and time-series trends to empower data-driven decision-making.

---

## 🎯 Objectives
- Utilize the `seaborn` library for advanced statistical visualizations (density, variance, outliers).
- Generate diverse chart types (box plots, violin plots, heatmaps, subplots) to uncover hidden patterns.
- Design cohesive, professional color schemes utilizing built-in seaborn themes.
- Build an interactive, web-ready scatter plot using Plotly Express with dynamic hover data.
- Consolidate multiple static charts into a clean 2x2 subplot dashboard architecture.

---

## 🛠️ Technical Requirements Implemented
- **Statistical Distributions:** Used `sns.boxplot()` and `sns.violinplot()` to visually map data density, variance, and outliers across categorical groups, providing deeper context than simple averages.
- **Correlation Heatmaps:** Implemented `sns.heatmap()` coupled with `.corr()` to mathematically prove the relationship between quantitative variables (Price, Quantity, Total Sales).
- **Grid Layouts:** Leveraged `plt.subplots(2, 2)` to seamlessly bind four distinct Seaborn charts into a single static dashboard matrix.
- **Interactive Web Visualization:** Deployed `px.scatter()` to create a dynamic, 4-dimensional chart (X, Y, Color, and Size) that can be exported as an HTML file with interactive tooltips.

---

## 🧮 Data Manipulation & Visualization Logic
The program utilizes the following advanced visualization logic to process and present the data:

| Operation Performed | Python Logic Used | Business Insight / Purpose |
|---------------------|-------------------|----------------------------|
| **Box Plot Summary** | `sns.boxplot(x='Product', y='Price')` | Identifies median pricing, price variance, and outlier transactions across different product categories. |
| **Density Mapping** | `sns.violinplot(..., inner="quartile")` | Combines box plot features with KDE (Kernel Density Estimation) to show the exact density of quantities ordered per region. |
| **Mathematical Correlation** | `sns.heatmap(df.corr(), annot=True)` | Displays the statistical strength between numerical variables to identify the primary drivers of Total Sales. |
| **Dashboard Grid** | `fig, axs = plt.subplots(2, 2)` | Consolidates regional revenue, time-series trends, transaction volumes, and price clustering into a unified executive view. |
| **Plotly Interactive** | `px.scatter(..., hover_name="Region")` | Allows end-users to dynamically explore precise transaction details by hovering over data points on a web browser. |

---

## ⚙️ Setup & Installation
1. Install Python on your system
2. Install required libraries by running: `pip install pandas matplotlib seaborn plotly jupyter`
3. Download or clone this repository
4. Ensure `sales_data.csv` is placed in the root directory
5. Run the notebook using Jupyter, or execute the script using: `python dashboard.py`

---

## 📊 Sample Input
*The pipeline processes raw transactional data. Here is a sample of the data being visualized:*

**Sales Data:**
Date: 2024-01-01 | Product: Phone | Quantity: 7 | Price: 37300 | Region: East | Total_Sales: 261100

## 📊 Result for Sample Data:
========================================
✅ Data successfully loaded and dates formatted!
🎨 Generating Seaborn Statistical Visualizations...
✨ Generating Plotly Interactive Dashboard...
✅ Saved interactive dashboard as HTML file!
========================================

---

## 📂 Project Files
- `CustomerAnalysis.ipynb` – Main Python data visualization notebook
- `README.md` – Project description
- `sales_data.csv` – Raw transactional dataset
- `plotly.gif` – Demo plotly visualization
- `requirements.txt` – Dependencies (pandas, matplotlib, seaborn, plotly)
- `analysis_report.pdf` – Final business analysis and executive summary
