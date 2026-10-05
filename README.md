
# Restaurant Management Backend API

A RESTful backend API for a restaurant management platform built using **FastAPI** and **MongoDB**.

## Features

### Authentication

- Customer and Admin registration
- Login with JWT authentication
- Role-based access control
- Secure password hashing

### Menu Management

- Admin can add food items
- Admin can update food items
- Admin can delete food items
- View all menu items
- Search food by name or description
- Filter food by category
- Check food availability

### Customer Features

- View restaurant menu
- Search and filter food
- Place orders
- View order history
- Cancel pending orders

### Order Management

- Customers can place orders
- Automatic total price calculation
- Order status tracking
- Admin can view all orders
- Admin can update order status

Supported order statuses:

- Pending
- Preparing
- Out for delivery
- Delivered
- Cancelled

## Technologies Used

- Python
- FastAPI
- MongoDB
- PyMongo
- JWT Authentication
- Passlib
- Bcrypt
- Pydantic
- Uvicorn

## Project Structure

```text
restaurant-management-backend/
│
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── utils/
│   ├── database.py
│   ├── main.py
│   └── __init__.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

Clone the repository and open the project folder:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd restaurant-management-backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
MONGO_URI=your_mongodb_connection_string
DATABASE_NAME=restaurant_management
JWT_SECRET=your_secret_key
```

> **Security:** Do not share or commit the `.env` file to GitHub.

The `.gitignore` file should include:

```gitignore
venv/
.env
__pycache__/
*.pyc
```

## Run the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test the available API endpoints.

---

# API Endpoints

## Authentication

| Method | Endpoint | Access |
|---|---|---|
| `POST` | `/signup` | Public |
| `POST` | `/login` | Public |

## Menu

| Method | Endpoint | Access |
|---|---|---|
| `POST` | `/menu` | Admin |
| `GET` | `/menu` | Public |
| `GET` | `/menu/{menu_id}` | Public |
| `PUT` | `/menu/{menu_id}` | Admin |
| `DELETE` | `/menu/{menu_id}` | Admin |

## Orders

| Method | Endpoint | Access |
|---|---|---|
| `POST` | `/order` | Customer |
| `GET` | `/my-orders` | Customer |
| `PUT` | `/order/{order_id}/cancel` | Customer |
| `GET` | `/orders` | Admin |
| `PUT` | `/order/{order_id}/status` | Admin |

---

# User Roles

## Customer

Customers can:

- View the restaurant menu
- Search food
- Filter food by category
- Check food availability
- Place orders
- View order history
- Cancel pending orders

## Admin

Admins can:

- Add menu items
- Update menu items
- Delete menu items
- View all orders
- Update order status
- Manage restaurant menu items

---

# Order Flow

The basic customer order workflow is:

```text
Customer
    ↓
Login
    ↓
View / Search Menu
    ↓
Select Food
    ↓
Place Order
    ↓
Pending
    ↓
Preparing
    ↓
Out for delivery
    ↓
Delivered
```

An order may also be cancelled while it is still eligible for cancellation:

```text
Pending
    ↓
Cancelled
```

---

# Authentication

The API uses **JWT Bearer Authentication** for protected endpoints.

After successful login, the API returns an access token.

Copy the returned access token and use the **Authorize** button in Swagger UI.

Enter the token in the following format:

```text
Bearer YOUR_JWT_TOKEN
```

Protected endpoints require a valid JWT token.

> **Security:** Never share your JWT access token publicly.

---

# Menu Management

The restaurant menu can be accessed publicly.

Customers can:

- View all available menu items
- Search food by name
- Search food by description
- Filter food by category
- Check food availability
- View individual menu items

Admins have additional permissions to:

- Create menu items
- Update menu items
- Delete menu items
- Manage food availability

---

# Order Management

Customers can create orders using available menu items.

The backend automatically calculates the total order price based on the selected food items and their quantities.

Customers can:

- Place orders
- View their previous orders
- Track order status
- Cancel eligible pending orders

Admins can:

- View all customer orders
- Update order status
- Manage the order workflow

### Supported Order Statuses

```text
Pending
Preparing
Out for delivery
Delivered
Cancelled
```

---

# Testing

The API was tested using **FastAPI Swagger UI**.

The following functionality was tested and verified:

- Customer signup
- Customer login
- Admin signup
- Admin login
- JWT authentication
- Role-based authorization
- Menu creation
- Menu update
- Menu deletion
- Menu retrieval
- Menu search
- Category filtering
- Food availability
- Order placement
- Automatic total price calculation
- Order history
- Order cancellation
- Admin order management
- Order status updates
- Protected endpoint access

## Role-Based Access Testing

### Customer Access

Customers can access customer-specific functionality such as:

```text
GET /menu
POST /order
GET /my-orders
PUT /order/{order_id}/cancel
```

### Admin Access

Admins can access administrative functionality such as:

```text
POST /menu
PUT /menu/{menu_id}
DELETE /menu/{menu_id}
GET /orders
PUT /order/{order_id}/status
```

Unauthorized users cannot access protected endpoints without a valid JWT token.

---

# Security

The project implements the following security features:

- JWT-based authentication
- Password hashing
- Protected API routes
- Role-based authorization
- Environment variables for sensitive configuration
- `.gitignore` protection for `.env`

Sensitive credentials such as MongoDB connection strings and JWT secrets must never be committed to the repository.

---

# API Workflow

The overall application workflow is:

```text
User Signup
     ↓
User Login
     ↓
JWT Access Token
     ↓
View Restaurant Menu
     ↓
Search / Filter Food
     ↓
Select Food
     ↓
Place Order
     ↓
Order Pending
     ↓
Order Preparing
     ↓
Out for Delivery
     ↓
Delivered
```

For administrative users:

```text
Admin Login
     ↓
JWT Access Token
     ↓
Manage Menu
     ↓
View Orders
     ↓
Update Order Status
     ↓
Manage Restaurant Operations
```

---

# Internship Project

This project was developed as part of a **Backend Development Internship Project**.

The objective was to build a restaurant management backend that demonstrates:

- REST API development
- Authentication and authorization
- Database integration
- Role-based access control
- CRUD operations
- Menu management
- Order management
- API testing using Swagger UI

---

# Future Improvements

Possible future improvements include:

- Online payment integration
- Food image uploads
- Customer profile management
- Restaurant table reservation
- Order notifications
- Email notifications
- SMS notifications
- Admin dashboard
- Restaurant analytics
- Order tracking
- Delivery partner management
- Customer reviews and ratings
- Automated testing
- Rate limiting
- Production logging
- Docker deployment
- Cloud deployment

---

# Author

Developed as part of a **Backend Development Internship Project**.
```
