import pandas as pd
import matplotlib.pyplot as plt
import os

def setup_folders():
    #Creates folders if not existing in path
    for folder in ['visualizations','report']:
        os.makedirs(folder, exist_ok=True)

def main():
    setup_folders()
    print("Starting E-Commerce Data Visualization Pipeline..\n")

    #1. Loading Data
    try:
        file_path = r"D:\Week4_Project\data\sales_data.csv"
        df = pd.read_csv(file_path)
        print(f"Data successfully loaded from {file_path}")
    except FileNotFoundError:
        print(f"Error: Data not found at {file_path}")
        return

    #2. Cleaning Data
    missing_val = df.isnull().sum().sum()
    if missing_val>0:
        df.dropna(inplace=True)
        print(f"Cleaned {missing_val} missing values from the dataset.")
    else:
        print("Data is already clean. No missing values found.")

    #3. Analyzing data
    total_revenue = df['Total_Sales'].sum()
    product_sales = df.groupby('Product')['Total_Sales'].sum().sort_values()
    region_sales = df.groupby('Product')['Total_Sales'].sum().sort_values()
    region_sales = df.groupby('Region')['Total_Sales'].sum()

    print(f"\n Numerical Insights: ")
    print(f"Total Revenue: Rs {total_revenue:,.2f}")
    print(f"Top Product: {product_sales.index[1]}")

    #4. Data Visualization
    print("\n General Visualizations...")

    #Chart1: Bar chart (Sales by product)
    plt.figure(figsize=(10,6))
    product_sales.plot(kind='barh', color = '#4C72B0', edgecolor='black')
    plt.title('Total Revenue by Product Category', fontsize=14, fontweight='bold')
    plt.xlabel('Total Sales (₹)', fontsize=12)
    plt.ylabel('Product', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('visualizations/sales_by_product.png', dpi=300)
    plt.close()
    print("Bar chart saved: visualizations/sales_by_product.png")

    # Chart 2: Pie Chart (Sales by Region)
    plt.figure(figsize=(8, 8))
    region_sales.plot(kind='pie', autopct='%1.1f%%', startangle=140, 
                      colors=['#55A868', '#C44E52', '#8172B3', '#CCB974'])
    plt.title('Revenue Distribution by Region', fontsize=14, fontweight='bold')
    plt.ylabel('') # Hide default pandas ylabel
    plt.tight_layout()
    plt.savefig('visualizations/sales_by_region.png', dpi=300)
    plt.close()
    print("Pie chart saved: visualizations/sales_by_region.png")

    print("\n Pipeline complete! Charts are ready for your report.")

if __name__ == "__main__":
    main()
    
