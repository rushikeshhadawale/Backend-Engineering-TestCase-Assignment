# sample_data.py
from app import app
from models import db, Company, Warehouse, Supplier, Product, Inventory, Sale
from datetime import datetime, timedelta

with app.app_context():
    db.create_all()

    c = Company(name="Example Co")
    db.session.add(c)
    db.session.commit()

    w = Warehouse(company_id=c.id, name="Main Warehouse", location="Mumbai")
    db.session.add(w)

    s = Supplier(name="Supplier Corp", contact_email="orders@supplier.com")
    db.session.add(s)
    db.session.commit()

    p = Product(name="Widget A", sku="WID-001", price=9.99, low_stock_threshold=20)
    p.suppliers.append(s)
    db.session.add(p)
    db.session.commit()

    inv = Inventory(product_id=p.id, warehouse_id=w.id, quantity=5)
    db.session.add(inv)

    sale = Sale(product_id=p.id, warehouse_id=w.id, quantity=1, timestamp=datetime.utcnow() - timedelta(days=3))
    db.session.add(sale)

    db.session.commit()
    print("Sample data created.")
