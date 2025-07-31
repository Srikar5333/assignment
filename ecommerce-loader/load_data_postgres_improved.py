import pandas as pd
import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

# Load environment variables (create a .env file with your credentials)
load_dotenv()

def connect_to_postgres():
    """Establish connection to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'ecommerce'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'your_password'),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("Please check:")
        print("1. PostgreSQL is running")
        print("2. Database 'ecommerce' exists")
        print("3. Credentials are correct")
        return None

def create_table_if_not_exists(cursor):
    """Create the products table if it doesn't exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        cost DECIMAL(10,2),
        category VARCHAR(255),
        name VARCHAR(255),
        brand VARCHAR(255),
        retail_price DECIMAL(10,2),
        department VARCHAR(255),
        sku VARCHAR(255),
        distribution_center_id INTEGER
    );
    """
    cursor.execute(create_table_sql)

def load_data():
    """Load data from CSV to PostgreSQL"""
    # Load CSV
    try:
        df = pd.read_csv('products.csv')
        print(f"📊 Loaded {len(df)} rows from products.csv")
    except FileNotFoundError:
        print("❌ products.csv not found in current directory")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # Connect to PostgreSQL
    conn = connect_to_postgres()
    if not conn:
        return

    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    create_table_if_not_exists(cursor)
    
    # Insert data with progress tracking
    inserted_count = 0
    skipped_count = 0
    
    for index, row in df.iterrows():
        try:
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
            inserted_count += 1
            
            # Show progress every 1000 rows
            if (index + 1) % 1000 == 0:
                print(f"Progress: {index + 1}/{len(df)} rows processed")
                
        except Exception as e:
            print(f"❌ Error inserting row {index + 1}: {e}")
            skipped_count += 1
            continue

    conn.commit()
    print(f"✅ Data loading completed!")
    print(f"📈 Inserted: {inserted_count} rows")
    print(f"⏭️  Skipped: {skipped_count} rows")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_data() 