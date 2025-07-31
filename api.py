from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'ecommerce'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'your_password'),
        port=os.getenv('DB_PORT', '5432')
    )

app = Flask(__name__)
api = Api(app)

class ProductList(Resource):
    def get(self):
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT id, cost, category, name, brand, retail_price, department, sku, distribution_center_id FROM products ORDER BY id LIMIT %s OFFSET %s",
                (per_page, offset)
            )
            rows = cur.fetchall()
            products = [
                {
                    "id": row[0],
                    "cost": float(row[1]),
                    "category": row[2],
                    "name": row[3],
                    "brand": row[4],
                    "retail_price": float(row[5]),
                    "department": row[6],
                    "sku": row[7],
                    "distribution_center_id": row[8]
                }
                for row in rows
            ]
            cur.close()
            conn.close()
            return jsonify(products)
        except Exception as e:
            return {"error": str(e)}, 500

class Product(Resource):
    def get(self, product_id):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT id, cost, category, name, brand, retail_price, department, sku, distribution_center_id FROM products WHERE id = %s",
                (product_id,)
            )
            row = cur.fetchone()
            cur.close()
            conn.close()
            if row:
                product = {
                    "id": row[0],
                    "cost": float(row[1]),
                    "category": row[2],
                    "name": row[3],
                    "brand": row[4],
                    "retail_price": float(row[5]),
                    "department": row[6],
                    "sku": row[7],
                    "distribution_center_id": row[8]
                }
                return jsonify(product)
            else:
                return {"error": "Product not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

class DepartmentList(Resource):
    def get(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT d.id, d.name, COUNT(p.id) as product_count
                FROM departments d
                LEFT JOIN products p ON d.id = p.department_id
                GROUP BY d.id, d.name
                ORDER BY d.name
            """)
            departments = [
                {"id": row[0], "name": row[1], "product_count": row[2]}
                for row in cur.fetchall()
            ]
            cur.close()
            conn.close()
            return jsonify(departments)
        except Exception as e:
            return {"error": str(e)}, 500

class Department(Resource):
    def get(self, department_id):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM departments WHERE id = %s", (department_id,))
            row = cur.fetchone()
            cur.close()
            conn.close()
            if row:
                return jsonify({"id": row[0], "name": row[1]})
            else:
                return {"error": "Department not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

class DepartmentProducts(Resource):
    def get(self, department_id):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price, d.name as department, p.sku, p.distribution_center_id
                FROM products p
                LEFT JOIN departments d ON p.department_id = d.id
                WHERE d.id = %s
                ORDER BY p.id
            """, (department_id,))
            products = [
                {
                    "id": row[0],
                    "cost": float(row[1]),
                    "category": row[2],
                    "name": row[3],
                    "brand": row[4],
                    "retail_price": float(row[5]),
                    "department": row[6],
                    "sku": row[7],
                    "distribution_center_id": row[8]
                }
                for row in cur.fetchall()
            ]
            cur.close()
            conn.close()
            if products:
                return jsonify(products)
            else:
                return {"error": "No products found in this department"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(ProductList, '/api/products')
api.add_resource(Product, '/api/products/<int:product_id>')
api.add_resource(DepartmentList, '/api/departments')
api.add_resource(Department, '/api/departments/<int:department_id>')
api.add_resource(DepartmentProducts, '/api/departments/<int:department_id>/products')

if __name__ == '__main__':
    app.run(debug=True)