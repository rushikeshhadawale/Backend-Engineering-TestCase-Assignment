# models.py
from datetime import datetime, timedelta
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for product-supplier relationship
product_suppliers = db.Table(
    'product_suppliers',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('supplier_id', db.Integer, db.ForeignKey('suppliers.id'), primary_key=True)
)

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    warehouses = db.relationship('Warehouse', backref='company', lazy=True)

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    inventories = db.relationship('Inventory', backref='warehouse', lazy=True)

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255))

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False, index=True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    is_bundle = db.Column(db.Boolean, default=False)
    low_stock_threshold = db.Column(db.Integer, default=10)

    suppliers = db.relationship('Supplier', secondary=product_suppliers, backref=db.backref('products', lazy='dynamic'))
    inventories = db.relationship('Inventory', backref='product', lazy=True)
    sales = db.relationship('Sale', backref='product', lazy=True)

    def has_recent_sales(self, days=30):
        cutoff = datetime.utcnow() - timedelta(days=days)
        return any(s.timestamp >= cutoff for s in self.sales)

    def avg_daily_sales(self, days=30):
        cutoff = datetime.utcnow() - timedelta(days=days)
        total = sum(s.quantity for s in self.sales if s.timestamp >= cutoff)
        return Decimal(total) / Decimal(days) if total > 0 else Decimal('0')

class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)

class InventoryLog(db.Model):
    __tablename__ = 'inventory_logs'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BundleItem(db.Model):
    __tablename__ = 'bundle_items'
    id = db.Column(db.Integer, primary_key=True)
    bundle_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
