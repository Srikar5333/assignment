# PostgreSQL Setup Guide

## 1. Install PostgreSQL

1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer and follow these steps:
   - Choose your installation directory
   - Set a password for the postgres user (remember this!)
   - Keep the default port (5432)
   - Install all components

## 2. After Installation

1. Open pgAdmin (comes with PostgreSQL)
2. Connect to the server using the password you set
3. Create a new database called "ecommerce"

## 3. Create the Products Table

Run this SQL in pgAdmin or psql:

```sql
CREATE TABLE products (
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
```

## 4. Update the Python Script

Update the password in `load_data_postgres.py` with the password you set during PostgreSQL installation.

## 5. Run the Script

```bash
python load_data_postgres.py
``` 