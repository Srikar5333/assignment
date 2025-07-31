import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link, useParams } from "react-router-dom";
import axios from "axios";

const API_BASE = "http://localhost:5000/api";

function ProductsList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${API_BASE}/products`)
      .then(res => setProducts(res.data))
      .catch(err => setError("Failed to load products."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!products.length) return <div>No products found.</div>;

  return (
    <div className="container mt-4">
      <h2>Products</h2>
      <ul className="list-group">
        {products.map(prod => (
          <li className="list-group-item" key={prod.id}>
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
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${API_BASE}/products/${id}`)
      .then(res => setProduct(res.data))
      .catch(() => setError("Product not found."))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!product) return <div>Product not found.</div>;

  return (
    <div className="container mt-4">
      <h2>{product.name}</h2>
      <p><b>Category:</b> {product.category}</p>
      <p><b>Brand:</b> {product.brand}</p>
      <p><b>Price:</b> ${product.retail_price}</p>
      <p><b>SKU:</b> {product.sku}</p>
      <p><b>Department:</b> {product.department}</p>
      <p><b>Distribution Center ID:</b> {product.distribution_center_id}</p>
      <Link to="/">Back to list</Link>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ProductsList />} />
        <Route path="/products/:id" element={<ProductDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
