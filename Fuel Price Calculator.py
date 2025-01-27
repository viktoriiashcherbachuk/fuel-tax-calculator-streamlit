#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import pandas as pd  # Import pandas to avoid NameError

# Set custom CSS for background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #aacfc0;  /* Set background color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the title of the app
st.title("Fuel Price Calculator")

# Add a company logo
st.image("C:/Users/vpshc/Downloads/KF.jpg", width=600)  # Adjust width as needed

# Create a container for inputs
st.write(
    "<h4 style='color:#195a3e;'>Please choose product type, province and all possible tax exemptions in order to see the final price:</h4>",
    unsafe_allow_html=True
)

# Create rows for each input using columns
product_col, province_col = st.columns(2)
excise_col, carbon_col = st.columns(2)
provincial_col, trucking_col = st.columns(2)
discount_col, volume_col = st.columns(2)

# Dropdown for choosing the product
product = product_col.selectbox("Choose the product (mandatory): ▼", ["", "Clear Diesel", "Dyed Diesel"])

# Dropdown for choosing the province
provinces = [
    "",  # Empty option
    "Alberta", "British Columbia", "Manitoba", "New Brunswick",
    "Newfoundland & Labrador", "Northwest Territories", "Nova Scotia",
    "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"
]
province = province_col.selectbox("Choose your province (mandatory): ▼", provinces)

# Dropdowns for tax exemptions
excise_tax_exemption = excise_col.selectbox("Federal Excise Tax Exemption ▼", ["", "Yes", "No"])
carbon_tax_exemption = carbon_col.selectbox("Federal Carbon Tax Exemption ▼", ["", "Yes", "No"])
provincial_tax_exemption = provincial_col.selectbox("Provincial Fuel Tax Exemption ▼", ["", "Yes", "No"])

# Input fields for trucking, discount, and volume
trucking_cost = trucking_col.number_input("Trucking:", min_value=0, value=0)
discount_amount = discount_col.number_input("Discount:", min_value=0, value=0)
volume = volume_col.number_input("Volume (liters):", min_value=1, value=1)

# Initialize variables for calculations
product_price = None
federal_excise_tax = None
federal_carbon_tax = None
provincial_fuel_tax = None

# Set product price based on selection
if product == "Clear Diesel":
    product_price = 1.5
elif product == "Dyed Diesel":
    product_price = 1.3

# Calculate taxes based on exemptions
if excise_tax_exemption == "No":
    federal_excise_tax = 0.04
elif excise_tax_exemption == "Yes":
    federal_excise_tax = 0

if carbon_tax_exemption == "No":
    federal_carbon_tax = 0.2139
elif carbon_tax_exemption == "Yes":
    federal_carbon_tax = 0

# Calculate provincial fuel tax based on conditions
if provincial_tax_exemption == "Yes":
    provincial_fuel_tax = 0
else:
    if province == "":
        provincial_fuel_tax = None
    elif province == "Alberta":
        provincial_fuel_tax = 0.04 if product == "Dyed Diesel" else 0.13
    elif province == "British Columbia":
        provincial_fuel_tax = 0.03 if product == "Dyed Diesel" else 0.2267
    elif province == "Manitoba":
        provincial_fuel_tax = 0.03 if product == "Dyed Diesel" else 0.18
    elif province == "New Brunswick":
        provincial_fuel_tax = 0.03 if product == "Dyed Diesel" else 0.232
    elif province == "Newfoundland & Labrador":
        provincial_fuel_tax = 0.03 if product == "Dyed Diesel" else 0.205
    elif province == "Northwest Territories":
        provincial_fuel_tax = 0.031 if product == "Dyed Diesel" else 0.131
    elif province == "Nova Scotia":
        provincial_fuel_tax = 0.03 if product == "Dyed Diesel" else 0.194
    elif province == "Ontario":
        provincial_fuel_tax = 0.045 if product == "Dyed Diesel" else 0.183
    elif province == "Prince Edward Island":
        provincial_fuel_tax = 0.03 if product == "Dyed Diesel" else 0.242
    elif province == "Quebec":
        provincial_fuel_tax = 0.03 if product == "Dyed Diesel" else 0.202
    elif province == "Saskatchewan":
        provincial_fuel_tax = 0.09 if product == "Dyed Diesel" else 0.19
    elif province == "Yukon":
        provincial_fuel_tax = 0.062 if product == "Dyed Diesel" else 0.112

# Calculate final price with tax only when valid selections are made.
product_price_with_tax = (
    (product_price or 0) + (federal_excise_tax or 0) + 
    (federal_carbon_tax or 0) + (provincial_fuel_tax or 0) + 
    trucking_cost - discount_amount
)

# Calculate subtotal and total with GST only when valid selections are made.
subtotal = product_price_with_tax * volume
gst = subtotal * 0.05
total_price = subtotal + gst

# Display results in a structured format using markdown for better visibility.
st.write("#### Final Price Calculation")

results_table_data = {
    'Description': [
        'Product Price',
        'Trucking',
        'Discount',
        'Federal Excise Tax',
        'Federal Carbon Tax',
        'Provincial Fuel Tax',
        'Product Price w/Tax',
        'Volume',
        'Subtotal',
        'GST @ 5%',
        'Total'
    ],
    'Amount': [
        f"${product_price:.2f}" if product_price is not None else "",
        f"${trucking_cost:.2f}",
        f"${discount_amount:.2f}",
        f"${federal_excise_tax:.2f}" if federal_excise_tax is not None else "",
        f"${federal_carbon_tax:.2f}" if federal_carbon_tax is not None else "",
        f"${provincial_fuel_tax:.2f}" if provincial_fuel_tax is not None else "",
        f"${product_price_with_tax:.2f}",
        f"{volume} liters",
        f"${subtotal:.2f}",
        f"${gst:.2f}",
        f"<b>${total_price:.2f}</b>"   # Make Total bold using HTML tags.
    ]
}

results_df = pd.DataFrame(results_table_data)

# Display the results as a table without row numbers and column names.
st.write(results_df.to_html(escape=False), unsafe_allow_html=True)   # Display HTML table with bold total.



# In[ ]:




