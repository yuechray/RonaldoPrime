from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class CategoriesTable(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)

class ManufacturersTable(Base):
    __tablename__ = "manufacturers"

    manufacturer_id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer_name: Mapped[str]  = mapped_column(String(100), nullable=False)

class StoresTable(Base):
    __tablename__ = "stores"

    store_id: Mapped[int] = mapped_column(primary_key=True)
    store_name: Mapped[str] = mapped_column(String(255), nullable=False)

class ProductsTable(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.manufacturer_id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"))
    date_price_change: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    new_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    is_available: Mapped[bool] = mapped_column(default=True, nullable=False)

class DeliveriesTable(Base):
    __tablename__ = "deliveries"

    deliveries_id: Mapped[int]  = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.store_id"))
    delivery_date: Mapped[datetime] = mapped_column (DateTime, nullable=False)
    product_count: Mapped[int] = mapped_column (Integer, nullable=False)

class CustomersTable(Base):
    __tablename__= "customers"

    customer_id: Mapped[int]  = mapped_column(primary_key=True)
    customer_fname: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_lname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)

class PurchasesTable(Base):
    __tablename__ = "purchases"

    purchase_id: Mapped[int]  = mapped_column(primary_key=True)
    customer_id: Mapped[int]  = mapped_column(ForeignKey("customers.customer_id"))
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.store_id"))
    purchase_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class PurchaseItemsTable(Base):
    __tablename__ = "purchase_items"

    purchase_items_id: Mapped[int]  = mapped_column(primary_key=True)
    purchases_id: Mapped[int]  = mapped_column(ForeignKey("purchases.purchase_id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    product_count: Mapped[int] = mapped_column (Integer, nullable=False)
    product_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

