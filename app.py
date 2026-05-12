import streamlit as st
import pandas as pd
from st_gsheets_connection import GSheetsConnection

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="VIP Lottery System", layout="wide")

# 2. เชื่อมต่อฐานข้อมูล Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# ฟังก์ชันอ่านข้อมูล
def get_data():
    try:
        return conn.read(ttl=0)
    except:
        # ถ้าไม่มีข้อมูล ให้สร้างตารางเปล่าที่มีหัวตารางตามที่เราตั้งไว้ใน Sheets
        return pd.DataFrame(columns=["Timestamp", "User", "Number", "Type", "Amount"])

# 3. ระบบ Login
if "role" not in st.session_state:
    st.title("🔐 ระบบจัดการหวย VIP (Login)")
    user = st.text_input("ชื่อผู้ใช้งาน (Username)")
    pwd = st.text_input("รหัสผ่าน (Password)", type="password")
    if st.button("เข้าสู่ระบบ"):
        if user == "admin" and pwd == "9999":
            st.session_state["role"], st.session_state["user_name"] = "admin", "เจ้ามือ"
            st.rerun()
        elif user == "seller" and pwd == "1111":
            st.session_state["role"], st.session_state["user_name"] = "seller", "คนขาย A"
            st.rerun()
        else:
            st.error("รหัสผ่านไม่ถูกต้อง")
else:
    role = st.session_state["role"]
    user_name = st.session_state["user_name"]
    df_base = get_data()

    st.sidebar.title(f"👤 {user_name}")
    if st.sidebar.button("ออกจากระบบ"):
        del st.session_state["role"]
        st.rerun()

    # --- ส่วนของคนขาย (Seller) ---
    if role == "seller":
        st.title("📝 บันทึกยอดขาย")
        num = st.text_input("เลข (00-99)", max_chars=2)
        amt = st.number_input("จำนวนเงิน (บาท)", min_value=0, step=10)
        
        if st.button("ส่งยอด 🚀"):
            if len(num) == 2 and amt > 0:
                new_entry = pd.DataFrame([{
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "User": user_name,
                    "Number": num,
                    "Type": "บน",
                    "Amount": amt
                }])
                updated_df = pd.concat([df_base, new_entry], ignore_index=True)
                conn.update(data=updated_df)
                st.success("บันทึกข้อมูลเรียบร้อย!")
                st.rerun()
            else:
                st.warning("กรุณาใส่เลข 2 หลักและระบุจำนวนเงิน")

    # --- ส่วนของเจ้ามือ (Admin) ---
    elif role == "admin":
        st.title("📊 แผงควบคุมเจ้ามือ")
        st.metric("ยอดขายรวมทั้งหมด", f"{df_base['Amount'].astype(float).sum():,.2f} ฿")
        st.write("รายการขายล่าสุด:")
        st.dataframe(df_base, use_container_width=True)
