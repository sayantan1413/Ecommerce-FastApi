# E-Commerce API

## Overview

This is an E-Commerce API built using FastAPI and MongoDB. The API provides endpoints for managing products and processing orders.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [Folder Structure](#folder-structure)
- [Testing Endpoints](#license)

## Features

- Add new products to the inventory
- Retrieve a list of products with filtering options
- Create orders with multiple items
- Automatic generation of order timestamp
- Update product quantities based on orders

## Requirements

- Python 3.7 or higher
- MongoDB

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ecommerce-api.git
   cd ecommerce-api
   ```

2. Create Virtual Environment and configure env

   ```bash
   python3 -m venv venv
   source venv/bin/activate

   # Configure ENV file

   touch .env

   # Add this line in ENV

   MONGODB_ATLAS_CONNECTION_STRING="your_connection_string"

   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure MongoDB connection in `config.py`.

## Usage

1. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

2. Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to access the Swagger documentation.

3. Explore and test the API using the interactive Swagger UI.

## API Endpoints

- **Add Product:** `POST /products/add-product/`
- **List Products:** `GET /products/products/`
- **Create Order:** `POST /orders/create-order/`

For detailed API documentation, refer to [API Documentation](http://localhost:8000/docs).

## Contributing

Contributions are welcome! If you'd like to contribute, please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## Folder Structure

```
ecommerce-api/
│
├── app/
│ ├── **init**.py
│ ├── main.py
│ └── server/
│ ├── **init**.py
│ ├── app.py
│ ├── database.py
│ ├── models/
│ │ ├── **init**.py
│ │ ├── order.py
│ │ └── product.py
│ └── routes/
│ ├── **init**.py
│ ├── orders.py
│ └── products.py
└── requirements.txt
```

## Testing the endpoints

### Add Products

#### Description:

This endpoint is responsible to add a product.

#### Https Method:

Post

#### Curl Request:

`curl --location 'http://127.0.0.1:8000/products/add-product/' \
--header 'Content-Type: application/json' \
--data '{"name": "Asus Laptop", "price": 200.00, "quantity": 30}'`

#### Example Response

`{
    "id": "65bcebf526dea3612c07a761",
    "name": "Asus Laptop",
    "price": 200.0,
    "quantity": 30
}`

### Get All Products

#### Description:

This endpoint is responsible to list all the products available.

#### Https Method:

Get

#### Curl Request:

`curl --location 'http://localhost:8000/products/products/'`

#### Optional Parameters:

1. min_price
2. max_price

#### Example Response

`{
    "data": [
        {
            "id": "65baa76b535233d7f86388c7",
            "name": "HP Laptop",
            "price": 99.99,
            "quantity": 8
        },
        {
            "id": "65bb85ed644b654ccd54b5bf",
            "name": "Lenovo Laptop",
            "price": 100.0,
            "quantity": 20
        },
        {
            "id": "65bcebf526dea3612c07a761",
            "name": "Asus Laptop",
            "price": 200.0,
            "quantity": 30
        }
    ],
    "page": {
        "limit": 10,
        "next_offset": null,
        "prev_offset": null,
        "total": 3
    }
}`

### Create Orders

#### Description:

This endpoint is responsible to create a order with list of products.

#### Https Method:

Post

#### Curl Request:

`curl --location 'http://localhost:8000/orders/create-order/' \
--header 'Content-Type: application/json' \
--data '{
  "items": [
    {
      "productId": "65baa76b535233d7f86388c7",
      "boughtQuantity": 2,
      "unitPrice": 99.99
    }
  ],
  "userAddress": {
    "city": "Kolkata",
    "country": "India",
    "zipCode": "700153"
  }
}'`

#### Example Response

`{
    "id": "65bb865450c1712e89216785",
    "createdOn": "2024-02-01T11:53:54.997632",
    "items": [
        {
            "productId": "65baa76b535233d7f86388c7",
            "boughtQuantity": 2
        }
    ],
    "userAddress": {
        "city": "Kolkata",
        "country": "India",
        "zipCode": "700153"
    },
    "totalAmount": 199.98
}`
