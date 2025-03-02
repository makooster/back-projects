# Sales and Trading API

Sales and Trading API is a backend service for managing users, products, sales, and trading transactions. The API is built using Django and Django REST Framework (DRF), featuring JWT authentication, role-based permissions, and Swagger documentation.

## Features

- User authentication and JWT-based authorization
- Product and category management
- Sales order tracking
- Trading transactions management
- API documentation with Swagger and Redoc

## Tech Stack

- **Backend**: Django, Django REST Framework (DRF)
- **Authentication**: JWT (Django REST Framework SimpleJWT)
- **Database**: PostgreSQL / SQLite (default)
- **API Docs**: Swagger, Redoc

## Installation

Clone the repository:

```bash
git clone https://github.com/makoster/back_projects/tree/main/sales_trade.git
cd sales-trade-api
```

Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Access the API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **Redoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## API Endpoints

### Authentication

| Method | Endpoint                       | Description              |
|--------|--------------------------------|--------------------------|
| POST   | /api/users/register/           | Register a new user      |
| POST   | /api/users/login/              | Obtain JWT token         |
| POST   | /api/users/token/refresh/      | Refresh JWT token        |
| GET    | /api/users/profile/            | Retrieve or edit user profile |

### Products

| Method | Endpoint                        | Description                      |
|--------|---------------------------------|----------------------------------|
| GET    | /api/products/                  | List all products                |
| POST   | /api/products/                  | Create a new product (Admin/Trader) |
| GET    | /api/products/{id}/             | Retrieve product details         |
| PUT    | /api/products/{id}/             | Update product (Admin/Trader)    |
| DELETE | /api/products/{id}/             | Delete product (Admin/Trader)    |

### Categories

| Method | Endpoint                             | Description                      |
|--------|--------------------------------------|----------------------------------|
| GET    | /api/products/categories/           | List all categories              |
| POST   | /api/products/categories/           | Create a new category (Admin/Trader) |
| GET    | /api/products/categories/{id}/      | Retrieve category details        |
| PUT    | /api/products/categories/{id}/      | Update category (Admin/Trader)   |
| DELETE | /api/products/categories/{id}/      | Delete category (Admin/Trader)   |

### Sales

| Method | Endpoint                          | Description                       |
|--------|-----------------------------------|-----------------------------------|
| GET    | /api/sales/orders/                | List all sales orders             |
| GET    | /api/sales/orders/{id}/           | Retrieve sales order details      |

### Trading

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|------------------------------------|
| GET    | /api/trading/orders/              | List all trading orders           |
| GET    | /api/trading/orders/{id}/         | Retrieve trading order details    |
| GET    | /api/trading/transactions/        | List all transactions             |
| GET    | /api/trading/transactions/{id}/   | Retrieve transaction details      |

## Permissions

- **Admin**: Can manage users, products, categories, and sales.
- **Trader**: Can create and update products and categories.
- **Authenticated Users**: Can view products and place orders.
- **Anonymous Users**: Can only view products.

## Project Structure

```bash
├── sales_trade/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── users/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── permissions.py
├── products/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
├── sales/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
├── trading/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
```

## Deployment

Set up environment variables for production:

```bash
export DEBUG=False
export SECRET_KEY='your-secret-key'
```

Apply database migrations:

```bash
python manage.py migrate
```

Collect static files:

```bash
python manage.py collectstatic
```

Run the production server:

```bash
gunicorn sales_trade.wsgi:application --bind 0.0.0.0:8000
```

## License

This project is licensed under the MIT License.
