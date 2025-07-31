import pandas as pd
import psycopg2

# Load CSV
df = pd.read_csv('products.csv')

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="ecommerce",
    user="postgres",          # Replace if different
    password="your_password"  # Replace with your PostgreSQL password
)

cursor = conn.cursor()

# Insert data row by row
for _, row in df.iterrows():
    sql = """
        INSERT INTO products (
            id, cost, category, name, brand, retail_price, department, sku, distribution_center_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """
    values = (
        int(row['id']),
        float(row['cost']),
        row['category'],
        row['name'],
        row['brand'],
        float(row['retail_price']),
        row['department'],
        row['sku'],
        int(row['distribution_center_id'])
    )
    cursor.execute(sql, values)

conn.commit()
print("✅ Data loaded successfully.")

cursor.close()
conn.close()