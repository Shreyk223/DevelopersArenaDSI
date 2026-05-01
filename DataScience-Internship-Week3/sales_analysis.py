import pandas as pd

def main():
    print("Welcome to Sales Data Analysis. \n")

    #1. Loading the dataset
    try:
        df = pd.read_csv(r'D:\sales_data.csv')
        print("Dataset loaded succesfully.")
    except FileNotFoundError:
        print("Error: 'sales_data.csv' not found. Please ensure the file is in the same directory.")
        return

    #2. Exploring data
    # (.shape[]) returns a tuple
    print (f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.\n")

    #3. Cleaning data
    #Checking for missing values across the DataFrame
    missing_values = df.isnull().sum().sum()
    if missing_values > 0:
        print (f"Found {missing_values} missing values. Cleaning data...")
        df.dropna(inplace=True)
    else:
        print("No missing values found. Data is clean.")

    #4. Analyze Sales (Calculate metrics)       
    # Metric 1: Total Revenue (Sum of Total_Sales column)
    total_revenue = df['Total_Sales'].sum()
    
    # Metric 2 & 3: Best-selling product (Group by Product, sum the Quantities)
    best_product = df.groupby('Product')['Quantity'].sum().idxmax()
    best_product_qty = df.groupby('Product')['Quantity'].sum().max()
    
    # Metric 4: Average Sale Value (Mean of Total_Sales)
    avg_sale_value = df['Total_Sales'].mean()
    
    # Metric 5: Total Items Sold
    total_quantity = df['Quantity'].sum()
    
    # 5. Create Report (Display formatted output)
    print("SALES ANALYSIS REPORT")

    # The :,.2f formats numbers with commas and 2 decimal places
    print(f"Total Revenue:         ₹{total_revenue:,.2f}")
    print(f"Average Sale Value:    ₹{avg_sale_value:,.2f}")
    print(f"Total Items Sold:      {total_quantity} units")
    print(f"Best-Selling Product:  {best_product} ({best_product_qty} units sold)")
    print("Analysis complete.")

if __name__ == "__main__":
    main()

    
