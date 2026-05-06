## 1. Executive Summary
This project represents a complete, end-to-end data analysis pipeline built using Python. By leveraging the pandas library for data manipulation and the matplotlib library for visual rendering, a raw e-commerce dataset (100 transactional records) was successfully transformed into actionable business intelligence. The analysis focused on identifying high-performing product categories and mapping regional revenue distribution to assist in future business decision-making.

## 2. Project Objectives
*Design a complete programmatic data pipeline: Load -> Clean -> Analyze -> Visualize.
*Implement robust error handling (try-except blocks) to ensure the program does not crash if files are missing or paths are incorrect.
*Utilize matplotlib.pyplot to generate at least two distinct chart types (Bar Chart and Pie Chart).
*Extract and document meaningful business insights based on the generated visualizations.

## 3. Setup & Environment Documentation

Language: Python 3.13.x

Core Libraries: pandas (data structures), matplotlib (data visualization)

File Architecture: The project was built using a strictly organized offline folder structure:

data/ - Contains the raw sales_data2.csv file.

visualizations/ - The output directory where the Python script automatically saves generated .png charts.

main.py - The primary executable script.

## 4. Data Processing Methodology

Data Ingestion: The CSV file was loaded from a localized D: drive path using pd.read_csv().

Data Cleaning: An automated audit was conducted using df.isnull().sum(). The script was programmed to utilize df.dropna() to dynamically remove any corrupted or missing rows, ensuring mathematical aggregations remained accurate.

Data Aggregation: The groupby() function was utilized to segment the data by 'Product' and 'Region', aggregating the 'Total_Sales' for each category.

## 5. Visual Insights & Business Findings

Insight 1: Product Performance (Bar Chart)
<img width="3000" height="1800" alt="sales_by_product" src="https://github.com/user-attachments/assets/f5dabe19-ea60-4ff8-86cb-f7bc34d52ec7" />

Analysis: Laptops are the Primary Revenue Driver: Laptops dominate the sales charts by a significant margin, bringing in nearly Rs 4 million. This indicates that high-ticket electronics are the core of the business's revenue stream.

A Clear Middle Tier: Tablets and Phones are performing very similarly, both hovering just below the Rs 3 million mark. They form a solid, reliable secondary revenue source.

Accessories Lag Behind: Monitors and Headphones are the lowest performers, generating less than Rs 1.5 million each.

Actionable Takeaway: The company should ensure a robust supply chain and allocate the majority of its marketing budget toward Laptops, Tablets, and Phones, as these products yield the highest return on investment.

Insight 2: Regional Revenue Distribution (Pie Chart)
<img width="2400" height="2400" alt="sales_by_region" src="https://github.com/user-attachments/assets/b1606c1d-f7f1-40ac-abd5-2bc7a0054208" />

North and South Dominate: The business is heavily reliant on the North (32.2%) and South (30.2%) regions. Combined, these two territories account for nearly two-thirds (62.4%) of the total company revenue.

The West is Underperforming: The West region is the weakest link, contributing only 17.2% to the total sales.

Actionable Takeaway: Logistics and warehouse storage should be heavily concentrated in the North and South to ensure fast delivery times where demand is highest. Additionally, the company should investigate why the West is underperforming—it may require targeted regional marketing campaigns or specific promotional discounts to boost adoption in that area.

## 6. Technical Learnings & Conclusion
This project solidified the transition from basic scripting to building functional data pipelines. Key technical takeaways include:

Library Integration: Successfully combining pandas and matplotlib to handle both the mathematical logic and the visual output in a single script.

Chart Customization: Learning how to adjust DPI for high-resolution images, format labels, apply custom hex color codes, and use plt.tight_layout() to ensure professional, presentation-ready charts.

Automated Reporting: Realizing the power of Python over traditional tools like Excel; this script can now be reused infinitely. If next month's sales data is dropped into the folder, the script will instantly generate updated charts and metrics with zero manual effort.
