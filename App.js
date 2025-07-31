import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link, useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const API_BASE = "http://localhost:5000/api";

function DepartmentsList() {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_BASE}/departments`)
      .then(res => setDepartments(res.data))
      .catch(() => setDepartments([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading departments...</div>;
  if (!departments.length) return <div>No departments found.</div>;

  return (
    <div>
      <h3>Departments</h3>
      <ul>
        {departments.map(dept => (
          <li key={dept.id}>
            <Link to={`/departments/${dept.id}`}>{dept.name} ({dept.product_count})</Link>
          </li>
        ))}
      </ul>
      <Link to="/">All Products</Link>
    </div>
  );
}

function DepartmentPage() {
  const { id } = useParams();
  const [department, setDepartment] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    // Fetch department info
    axios.get(`${API_BASE}/departments/${id}`)
      .then(res => setDepartment(res.data))
      .catch(() => setDepartment(null));
    // Fetch products in department
    axios.get(`${API_BASE}/departments/${id}/products`)
      .then(res => setProducts(res.data))
      .catch(() => setProducts([]))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div>Loading department...</div>;
  if (!department) return <div>Department not found.</div>;

  return (
    <div>
      <button onClick={() => navigate(-1)}>Back</button>
      <h2>{department.name}</h2>
      <p>Products in this department: {products.length}</p>
      <ul>
        {products.map(prod => (
          <li key={prod.id}>
            <Link to={`/products/${prod.id}`}>{prod.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ProductsList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_BASE}/products`)
      .then(res => setProducts(res.data))
      .catch(() => setProducts([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading products...</div>;
  if (!products.length) return <div>No products found.</div>;

  return (
    <div>
      <h2>All Products</h2>
      <ul>
        {products.map(prod => (
          <li key={prod.id}>
            <Link to={`/products/${prod.id}`}>{prod.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_BASE}/products/${id}`)
      .then(res => setProduct(res.data))
      .catch(() => setProduct(null))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (!product) return <div>Product not found.</div>;

  return (
    <div>
      <h2>{product.name}</h2>
      <p><b>Category:</b> {product.category}</p>
      <p><b>Brand:</b> {product.brand}</p>
      <p><b>Price:</b> ${product.retail_price}</p>
      <p><b>Department:</b> {product.department}</p>
      <Link to="/">Back to list</Link>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div style={{ display: "flex" }}>
        <div style={{ width: "250px", marginRight: "2rem" }}>
          <DepartmentsList />
        </div>
        <div style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<ProductsList />} />
            <Route path="/products/:id" element={<ProductDetail />} />
            <Route path="/departments/:id" element={<DepartmentPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
