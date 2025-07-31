-- Create database (run this as superuser)
CREATE DATABASE ecommerce;

-- Connect to the ecommerce database and run this:
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

-- Create index for better performance
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category); 