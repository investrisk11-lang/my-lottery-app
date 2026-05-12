import os
import subprocess
import sys

# --- ส่วนบังคับติดตั้ง Library อัตโนมัติ ---
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from st_gsheets_connection import GSheetsConnection
except ImportError:
    install('st-gsheets-connection')
    install('pandas')
    st.rerun()
# -------------------------------------

import streamlit as st
import pandas as pd
from st_gsheets_connection import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="VIP Lottery", layout="wide")

# เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=["Timestamp", "User", "Number", "Type", "Amount"])

# ส่วนแสดงผล (Login)
if "role" not in st.session_state:
    st.title("🔐 ระบบจัดการหวย VIP")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("เข้าสู่ระบบ"):
        if user == "admin" and pwd == "9999":
            st.session_state["role"], st.session_state["user_name"] = "admin", "เจ้ามือ"
            st.rerun()
        elif user == "seller" and pwd == "1111":
            st.session_state["role"], st.session_state["user_name"] = "seller", "คนขาย A"
            st.rerun()
        else: st.error("ข้อมูลไม่ถูกต้อง")
else:
    role, user_name = st.session_state["role"], st.session_state["user_name"]
    df_base = get_data()
    st.sidebar.write(f"ผู้ใช้: {user_name}")
    if st.sidebar.button("ออกจากระบบ"):
        del st.session_state["role"]
        st.rerun()
    st.write(f"สวัสดีคุณ {user_name} ระบบพร้อมทำงานแล้วครับ")
    st.dataframe(df_base)
