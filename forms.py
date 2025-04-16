import streamlit as st

def product_form():
    with st.form("product_form"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        stock = st.number_input("Stock", min_value=0, step=1)
        submit = st.form_submit_button("Add Product")

        if submit and name and price >= 0 and stock >= 0:
            return {
                'name': name,
                'price': price,
                'stock': stock
            }
        elif submit:
            st.error("All fields are required.")
    return None


def customer_form():
    with st.form("customer_form"):
        name = st.text_input("Customer Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        submit = st.form_submit_button("Add Customer")

        if submit and name and email and phone:
            return {
                'name': name,
                'email': email,
                'phone': phone
            }
        elif submit:
            st.error("All fields are required.")
    return None
