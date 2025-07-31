import pandas as pd
import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

# Load environment variables (create a .env file with your credentials)
load_dotenv()

def connect_to_postgres():
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
        return None

def create_departments_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        );
    ''')

def create_products_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            cost DECIMAL(10,2),
            category VARCHAR(255),
            name VARCHAR(255),
            brand VARCHAR(255),
            retail_price DECIMAL(10,2),
            department_id INTEGER,
            sku VARCHAR(255),
            distribution_center_id INTEGER,
            CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id)
        );
    ''')

def populate_departments(cursor, departments):
    for dept in departments:
        cursor.execute(
            "INSERT INTO departments (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
            (dept,)
        )

def get_department_id(cursor, dept_name):
    cursor.execute("SELECT id FROM departments WHERE name = %s;", (dept_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def load_data():
    try:
        df = pd.read_csv('products.csv')
        print(f"📊 Loaded {len(df)} rows from products.csv")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    conn = connect_to_postgres()
    if not conn:
        return
    cursor = conn.cursor()

    # 1. Create departments table
    create_departments_table(cursor)
    # 2. Extract unique departments
    unique_departments = df['department'].dropna().unique()
    # 3. Populate departments table
    populate_departments(cursor, unique_departments)
    # 4. Create products table (with department_id FK)
    create_products_table(cursor)
    conn.commit()

    # 5. Insert products with department_id
    inserted_count = 0
    skipped_count = 0
    for index, row in df.iterrows():
        try:
            dept_id = get_department_id(cursor, row['department'])
            sql = '''
                INSERT INTO products (
                    id, cost, category, name, brand, retail_price, department_id, sku, distribution_center_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            '''
            values = (
                int(row['id']),
                float(row['cost']),
                row['category'],
                row['name'],
                row['brand'],
                float(row['retail_price']),
                dept_id,
                row['sku'],
                int(row['distribution_center_id'])
            )
            cursor.execute(sql, values)
            inserted_count += 1
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