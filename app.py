import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# ---------------------- Database Setup ----------------------
DATABASE_URL = 'sqlite:///estore.db'

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# ---------------------- Models ----------------------
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    customer = relationship('Customer', backref='orders')
    product = relationship('Product', backref='orders')

Base.metadata.create_all(engine)

# ---------------------- Functions ----------------------
def add_product(name, price, stock):
    new_product = Product(name=name, price=price, stock=stock)
    session.add(new_product)
    session.commit()
    st.success(f"✅ Product '{name}' added successfully!")

def add_customer(name, email, phone):
    new_customer = Customer(name=name, email=email, phone=phone)
    session.add(new_customer)
    session.commit()
    st.success(f"✅ Customer '{name}' added successfully!")

def add_order(customer_id, product_id, quantity):
    new_order = Order(customer_id=customer_id, product_id=product_id, quantity=quantity)
    session.add(new_order)
    session.commit()
    st.success("✅ Order added successfully!")

# ---------------------- Pages ----------------------
def back_to_home_button():
    col = st.columns([8, 2])[1]
    with col:
        if st.button("⬅ Back to Home", key="back_btn"):
            st.session_state.page = None
            st.rerun()

def products_page():
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🛒 Products - E-Store</h2>", unsafe_allow_html=True)
    back_to_home_button()

    st.subheader("➕ Add New Product")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)

    if st.button("Add Product", type="primary"):
        if name and price and stock:
            add_product(name, price, stock)
        else:
            st.error("⚠️ Please fill all product details.")

    st.subheader("📦 Product List")
    products = session.query(Product).all()
    for product in products:
        st.info(f"🛍️ **{product.name}** - ₹{product.price} - Stock: {product.stock}")

def customers_page():
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>👥 Customers - E-Store</h2>", unsafe_allow_html=True)
    back_to_home_button()

    st.subheader("➕ Add New Customer")
    name = st.text_input("Customer Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    if st.button("Add Customer", type="primary"):
        if name and email and phone:
            add_customer(name, email, phone)
        else:
            st.error("⚠️ Please fill all customer fields.")

    st.subheader("📋 Customer List")
    customers = session.query(Customer).all()
    for customer in customers:
        st.success(f"🙍‍♂️ **{customer.name}** - {customer.email} - {customer.phone}")

def orders_page():
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📦 Orders - E-Store</h2>", unsafe_allow_html=True)
    back_to_home_button()

    st.subheader("➕ Add New Order")
    customer_id = st.number_input("Customer ID", min_value=1, step=1)
    product_id = st.number_input("Product ID", min_value=1, step=1)
    quantity = st.number_input("Quantity", min_value=1, step=1)

    if st.button("Add Order", type="primary"):
        if customer_id and product_id and quantity:
            add_order(customer_id, product_id, quantity)
        else:
            st.error("⚠️ Please fill in all order details.")

    st.subheader("📋 Order List")
    orders = session.query(Order).all()
    for order in orders:
        st.warning(f"Customer ID: {order.customer_id} | Product ID: {order.product_id} | Quantity: {order.quantity}")

# ---------------------- Home Page ----------------------
def home_page():
    st.markdown("<h1 style='text-align: center; color: #2980b9;'> E-Store Management System </h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:16px;'>Choose a section </p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛒 Products", use_container_width=True):
            st.session_state.page = "products"
            st.rerun()
    with col2:
        if st.button("👥 Customers", use_container_width=True):
            st.session_state.page = "customers"
            st.rerun()
    with col3:
        if st.button("📦 Orders", use_container_width=True):
            st.session_state.page = "orders"
            st.rerun()

# ---------------------- Main Function ----------------------
def main():
    st.set_page_config(page_title="E-Store", layout="wide")

    if "page" not in st.session_state:
        st.session_state.page = None

    if st.session_state.page == "products":
        products_page()
    elif st.session_state.page == "customers":
        customers_page()
    elif st.session_state.page == "orders":
        orders_page()
    else:
        home_page()

if __name__ == "__main__":
    main()
