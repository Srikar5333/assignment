# Ecommerce Data Loader

This project loads product data from a CSV file into a PostgreSQL database.

## Prerequisites

1. **Python 3.8+** (already installed)
2. **PostgreSQL** (needs to be installed)

## Setup Instructions

### 1. Install Python Libraries

The required libraries are already installed:
- `pandas` - for CSV data processing
- `psycopg2-binary` - PostgreSQL adapter for Python
- `python-dotenv` - for environment variable management

### 2. Install PostgreSQL

1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer with these settings:
   - **Password**: Set a strong password (remember this!)
   - **Port**: 5432 (default)
   - **Install all components**

### 3. Set Up Database

After PostgreSQL installation:

1. **Open pgAdmin** (comes with PostgreSQL)
2. **Connect to server** using your password
3. **Create database**:
   - Right-click on "Databases" → "Create" → "Database"
   - Name it: `ecommerce`

4. **Create table** (run this SQL in pgAdmin):
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

### 4. Configure Database Connection

Create a `.env` file in the project directory:
```
DB_HOST=localhost
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
DB_PORT=5432
```

### 5. Run the Data Loader

Use the improved version:
```bash
python load_data_postgres_improved.py
```

Or the original version (update password first):
```bash
python load_data_postgres.py
```

## Files in this Project

- `products.csv` - Source data file
- `load_data_postgres.py` - Original script
- `load_data_postgres_improved.py` - Enhanced version with error handling
- `requirements.txt` - Python dependencies
- `setup_database.sql` - Database setup script
- `setup_postgres.md` - PostgreSQL installation guide

## Troubleshooting

### Connection Refused Error
- **PostgreSQL not running**: Start PostgreSQL service
- **Wrong credentials**: Check your `.env` file
- **Database doesn't exist**: Create the `ecommerce` database

### Permission Errors
- **User doesn't exist**: Create user or use `postgres` superuser
- **Database access denied**: Grant permissions to your user

### Data Loading Issues
- **CSV format**: Ensure `products.csv` is in the correct format
- **Data types**: Check that numeric fields contain valid numbers

## Performance Tips

- The improved script shows progress every 1000 rows
- Uses `ON CONFLICT DO NOTHING` to handle duplicates
- Includes error handling for individual row failures

## Next Steps

After successful data loading, you can:
1. Query the data using SQL
2. Build analytics dashboards
3. Create APIs to access the data
4. Set up automated data refresh processes 