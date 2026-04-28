import streamlit as st
import pandas as pd
from core.database import MongoDBClient

# Cấu hình trang
st.set_page_config(page_title="Crypto Analysis Dashboard", layout="wide")

st.title("📊 Hệ thống Theo dõi Dữ liệu Tiền mã hóa")
st.markdown("Dữ liệu được cập nhật tự động từ MongoDB")

# 1. Kết nối Database
db_client = MongoDBClient()
db = db_client.db # Lấy đối tượng database trực tiếp

# 2. Sidebar: Bộ lọc dữ liệu
st.sidebar.header("Bộ lọc tùy chỉnh")

# Lấy danh sách tất cả các collection đang có trong DB
all_collections = db.list_collection_names()
crypto_collections = [c for c in all_collections if c.startswith("crypto_") and "klines" in c]

if crypto_collections:
    selected_col = st.sidebar.selectbox("Chọn bảng dữ liệu (Coin_Interval):", sorted(crypto_collections))
    
    # Số lượng dòng muốn hiển thị
    num_rows = st.sidebar.slider("Số lượng bản ghi gần nhất:", 10, 500, 100)

    # 3. Lấy dữ liệu từ MongoDB
    collection = db[selected_col]
    # Lấy dữ liệu mới nhất (sắp xếp theo Open_time giảm dần)
    cursor = collection.find({}, {"_id": 0}).sort("Open_time", -1).limit(num_rows)
    
    df = pd.DataFrame(list(cursor))

    if not df.empty:
        # Làm sạch hiển thị thời gian
        df['Open_time'] = pd.to_datetime(df['Open_time'])
        
        # Hiển thị các chỉ số nhanh (Metrics)
        last_price = df.iloc[0]['Close']
        prev_price = df.iloc[1]['Close'] if len(df) > 1 else last_price
        delta = last_price - prev_price
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Giá hiện tại", f"${last_price:,.2f}", f"{delta:,.2f}")
        col2.metric("Khối lượng (Volume)", f"{df.iloc[0]['Volume']:,.2f}")
        col3.metric("Số lệnh khớp", f"{int(df.iloc[0]['Number_of_trades'])}")

        # 4. Hiển thị Bảng dữ liệu
        st.subheader(f"Bảng chi tiết: {selected_col}")
        st.dataframe(df, use_container_width=True, height=400)
        
        # 5. Vẽ biểu đồ giá đóng cửa đơn giản
        st.subheader("Biểu đồ biến động giá")
        st.line_chart(df.set_index('Open_time')['Close'])
        
        # Nút tải dữ liệu về CSV nếu cần
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Tải bảng này về CSV", csv, "data.csv", "text/csv")
    else:
        st.warning("Bảng này hiện chưa có dữ liệu.")
else:
    st.error("Không tìm thấy dữ liệu crypto trong MongoDB. Hãy chạy main.py trước!")