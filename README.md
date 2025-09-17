# Backend-Engineering-TestCase-Assignment
StockFlow – Inventory Management API A backend project built with Python (Flask) and MySQL for managing products, warehouses, and suppliers. It provides REST APIs to:   Add new products  , Check low stock alerts , Manage inventory data  This project demonstrates API development, database design, and backend integration with MySQL.

1️)Install Python
Download and install Python (3.9+ recommended) → python.org/downloads

2️)Install MySQL
Download MySQL → dev.mysql.com/downloads/mysql

3️)Create Database

Open MySQL shell and run:

CREATE DATABASE stockflow;
CREATE USER 'stockuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON stockflow.* TO 'stockuser'@'localhost';
FLUSH PRIVILEGES;

4️)Clone Repository
git clone https://github.com/rushikeshhadawale/Backend-Engineering-TestCase-Assignment.git
cd stockflow

5️)Install Dependencies
pip install -r requirements.txt

6️)Insert Sample Data
python sample_data.py

7️)Run the API
python app.py

Server runs at → http://127.0.0.1:5000/

 API Endpoints
 Add Product (POST)

POST http://127.0.0.1:5000/api/products

Request Body (JSON):

{
  "name": "Widget B",
  "sku": "WID-002",
  "price": "15.50",
  "warehouse_id": 1,
  "initial_quantity": 50
}


Response:

{"message": "Product created", "product_id": 2}

Low Stock Alerts (GET)

GET http://127.0.0.1:5000/api/companies/1/alerts/low-stock

Response:

{
  "alerts": [
    {
      "product_id": 1,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_id": 1,
      "warehouse_name": "Main Warehouse",
      "current_stock": 5,
      "threshold": 20,
      "days_until_stockout": 5.0,
      "supplier": {
        "id": 1,
        "name": "Supplier Corp",
        "contact_email": "orders@supplier.com"
      }
    }
  ],
  "total_alerts": 1
}
