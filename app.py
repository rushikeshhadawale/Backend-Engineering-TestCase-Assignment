import os
from decimal import Decimal, InvalidOperation
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Company, Warehouse, Product, Inventory

# define routes function first
def register_routes(app):
    @app.route('/')
    def home():
     return {"message": "API is running. Use /api/products or /api/companies/<id>/alerts/low-stock"}


    @app.route('/api/products', methods=['POST'])
    def create_product():
        data = request.json or {}
        if not data.get('name') or not data.get('sku') or data.get('price') is None:
            return {"error": "Missing fields"}, 400
        if Product.query.filter_by(sku=data['sku']).first():
            return {"error": "SKU exists"}, 400

        try:
            price = Decimal(str(data['price']))
        except (InvalidOperation, ValueError):
            return {"error": "Invalid price"}, 400

        product = Product(name=data['name'], sku=data['sku'], price=price,
                          low_stock_threshold=data.get('low_stock_threshold', 10))
        db.session.add(product)
        if data.get('warehouse_id'):
            inv = Inventory(product=product, warehouse_id=data['warehouse_id'],
                            quantity=data.get('initial_quantity', 0))
            db.session.add(inv)
        db.session.commit()
        return {"message": "Product created", "product_id": product.id}, 201
    
    # List all products (GET)
    @app.route('/api/products', methods=['GET'])
    def list_products():
     products = Product.query.all()
     return {
         "products": [
             {"id": p.id, "name": p.name, "sku": p.sku, "price": str(p.price)}
             for p in products
        ]
    }


    @app.route('/api/companies/<int:company_id>/alerts/low-stock')
    def low_stock_alerts(company_id):
        company = Company.query.get(company_id)
        if not company:
            return {"error": "Company not found"}, 404
        alerts = []
        for wh in company.warehouses:
            for inv in wh.inventories:
                product = inv.product
                if inv.quantity < product.low_stock_threshold and product.has_recent_sales():
                    avg = product.avg_daily_sales()
                    alerts.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "sku": product.sku,
                        "warehouse_id": wh.id,
                        "warehouse_name": wh.name,
                        "current_stock": inv.quantity,
                        "threshold": product.low_stock_threshold,
                        "days_until_stockout": None if avg == 0 else float(inv.quantity / avg)
                    })
        return {"alerts": alerts, "total_alerts": len(alerts)}

# now create app
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://stockuser:password@localhost/stockflow'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    Migrate(app, db)
    register_routes(app)   # now works
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
