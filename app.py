import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="PO Lookup", page_icon="📦")

# Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\India\Downloads\po-lookup-app-c66d1c29c0f1.json", scope)
client = gspread.authorize(creds)

# Load sheet
sheet = client.open("PURCHASE ORDER").sheet1
values = sheet.get_all_values()

# Skip metadata rows and use actual headers (assuming row 2)
headers = values[0]        # Row 2 = actual column headers
data = values[1:]          # From Row 3 onward = data
df = pd.DataFrame(data, columns=headers)

# Clean column names
df.columns = df.columns.str.strip()

# App UI
st.title("📦 PURCHASE ORDER DATA VIEWER SYSTEM")
po_input = st.text_input("Enter PO Number")

if po_input:
    result = df[df['PO # :'].str.upper() == po_input.upper()]
    
    if not result.empty:
        row = result.iloc[0]
        st.success("✅ PO Found")
        st.write(f"**Date:** {row['DATE:']}")
        st.write(f"**Vendor:** {row['VENDOR']}")
        st.write(f"**Item:** {row['PARTICULARS']}")
        st.write(f"**Shade:** {row['SHADE']}")
        st.write(f"**Ordered Qty:** {row['QTY']}")
        st.write(f"**Received Qty:** {row['RECEIVED Qty']}")
        pending = float(row['QTY'].replace(',', '')) - float(row['RECEIVED Qty'])
    else:
        st.error("❌ PO Number not found.")
