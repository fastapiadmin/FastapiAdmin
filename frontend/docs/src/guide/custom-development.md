# Custom Development Guide

## Overview

This guide provides instructions for customizing and extending FastapiAdmin to meet your specific business needs.

## Backend Customization

### Adding New Models

```python
from sqlalchemy import Column, Integer, String, Text
from fastapi_admin.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
```

### Creating Custom APIs

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_admin.database import get_db
from .models import Product

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.get("/")
async def get_products(db: AsyncSession = Depends(get_db)):
    products = await db.query(Product).all()
    return {"products": products}

@router.post("/")
async def create_product(product: Product, db: AsyncSession = Depends(get_db)):
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return {"product": product}
```

## Frontend Customization

### Adding New Components

```vue
<template>
  <div class="product-form">
    <h2>Add New Product</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>Product Name</label>
        <input v-model="product.name" type="text" required>
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea v-model="product.description"></textarea>
      </div>
      <div class="form-group">
        <label>Price</label>
        <input v-model.number="product.price" type="number" required>
      </div>
      <button type="submit">Save</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const product = ref({
  name: '',
  description: '',
  price: 0
})

const submitForm = async () => {
  const response = await fetch('/api/v1/products', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(product.value)
  })
  
  if (response.ok) {
    alert('Product created successfully!')
  }
}
</script>
```

### Customizing the Dashboard

```vue
<template>
  <div class="custom-dashboard">
    <h1>Custom Dashboard</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Total Products</h3>
        <p>{{ productCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Orders</h3>
        <p>{{ orderCount }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const productCount = ref(0)
const orderCount = ref(0)

onMounted(async () => {
  // Fetch dashboard data
  const productsResponse = await fetch('/api/v1/products')
  const productsData = await productsResponse.json()
  productCount.value = productsData.products.length
  
  const ordersResponse = await fetch('/api/v1/orders')
  const ordersData = await ordersResponse.json()
  orderCount.value = ordersData.orders.length
})
</script>
```

## Miniprogram Customization

### Adding New Pages

```vue
<template>
  <view class="product-list">
    <view class="product-item" v-for="product in products" :key="product.id">
      <text class="product-name">{{ product.name }}</text>
      <text class="product-price">¥{{ product.price }}</text>
      <button @click="viewDetails(product.id)">View Details</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const products = ref([])

onMounted(async () => {
  const response = await uni.request({
    url: '/api/v1/products'
  })
  products.value = response.data.products
})

const viewDetails = (productId) => {
  uni.navigateTo({
    url: `/pages/product/detail?id=${productId}`
  })
}
</script>
```

## Best Practices

1. **Modular Development**: Organize your code into modules based on functionality
2. **Version Control**: Use Git to track changes and collaborate with team members
3. **Testing**: Write unit tests for critical functionality
4. **Documentation**: Keep your code well-documented
5. **Security**: Follow security best practices for API development

## Deployment

After customizing your FastapiAdmin application, you can deploy it using the same deployment methods described in the deployment guide.

```bash
# Build the frontend
cd frontend
npm run build

# Build the backend (if using Docker)
docker build -t fastapiadmin-backend .

# Start all services
docker-compose up -d
```

## Troubleshooting

### Common Issues

1. **API Endpoints Not Found**: Check your router configuration and ensure endpoints are properly registered
2. **Database Connection Errors**: Verify your database credentials and network connectivity
3. **Frontend Build Failures**: Check for syntax errors in your Vue components
4. **CORS Issues**: Ensure your CORS configuration allows requests from your frontend domain

### Debugging Tips

1. **Enable Debug Mode**: Set `DEBUG=True` in your backend configuration
2. **Check Logs**: Monitor backend and frontend logs for error messages
3. **Use Browser DevTools**: Inspect network requests and console errors
4. **Test APIs Directly**: Use tools like Postman to test API endpoints

## Conclusion

FastapiAdmin provides a flexible foundation for building custom backend systems. By following this guide, you can extend the platform to meet your specific business requirements while maintaining a clean and maintainable codebase.