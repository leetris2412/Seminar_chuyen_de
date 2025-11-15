import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from nlp_core import analyze_sentiment  # <--- Import "bộ não" bạn vừa làm

# --- 1. CẤU HÌNH DATABASE (SQLite) ---
DB_NAME = "sentiment_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tạo bảng nếu chưa có
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  text_input TEXT,
                  sentiment_label TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(text, label):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Lưu thời gian hiện tại
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Parameterized query để chống SQL Injection
    c.execute("INSERT INTO history (text_input, sentiment_label, timestamp) VALUES (?, ?, ?)",
              (text, label, time_now))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect(DB_NAME)
    # Load dữ liệu ra DataFrame để hiển thị bảng đẹp
    df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC LIMIT 50", conn)
    conn.close()
    return df

# --- 2. GIAO DIỆN STREAMLIT ---
st.set_page_config(page_title="Đánh giá cảm xúc", page_icon="🤖")

# Khởi tạo DB
init_db()

st.title("🤖 Trợ lý Phân loại Cảm xúc Tiếng Việt")
st.caption("Sử dụng mô hình VisoBERT + Hybrid Rules")

# Chia giao diện thành 2 cột
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Nhập văn bản")
    user_input = st.text_area("Nhập câu tiếng Việt tại đây:", height=150)
    
    if st.button("Phân tích ngay", type="primary"):
        if user_input.strip():
            with st.spinner("Đang phân tích..."):
                # Gọi hàm NLP của bạn
                result = analyze_sentiment(user_input)
                
                if result:
                    sentiment = result['sentiment']
                    
                    # Hiển thị kết quả đẹp
                    if sentiment == "POSITIVE":
                        st.success(f"### Kết quả: TÍCH CỰC (POSITIVE) 😊")
                    elif sentiment == "NEGATIVE":
                        st.error(f"### Kết quả: TIÊU CỰC (NEGATIVE) 😡")
                    else:
                        st.info(f"### Kết quả: TRUNG TÍNH (NEUTRAL) 😐")
                    
                    # Lưu vào Database
                    save_to_db(user_input, sentiment)
                    st.toast("Đã lưu kết quả vào lịch sử!", icon="✅")
                else:
                    st.error("Có lỗi xảy ra khi xử lý.")
        else:
            st.warning("Vui lòng nhập nội dung!")

with col2:
    st.subheader("clock: Lịch sử gần đây")
    # Nút làm mới lịch sử
    if st.button("Tải lại lịch sử"):
        st.rerun()
        
    df_history = load_history()
    if not df_history.empty:
        st.dataframe(df_history[['text_input', 'sentiment_label', 'timestamp']], hide_index=True)
    else:
        st.write("Chưa có dữ liệu.")