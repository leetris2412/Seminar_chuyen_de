# 🤖 Đồ án: Trợ lý Phân loại Cảm xúc Tiếng Việt (Seminar)

Đây là đồ án môn học Chuyên đề Seminar, mục tiêu xây dựng một ứng dụng web đơn giản để phân loại cảm xúc (Tích cực, Tiêu cực, Trung tính) từ văn bản tiếng Việt.

Ứng dụng sử dụng phương pháp **Hybrid AI**, kết hợp mô hình Transformer (VisoBERT) và bộ lọc quy tắc (Rule-based) để đạt độ chính xác cao trên bộ dữ liệu kiểm thử.

## 🌟 Tính năng chính

* Phân loại văn bản tiếng Việt thành 3 nhãn: **POSITIVE** (Tích cực), **NEGATIVE** (Tiêu cực), **NEUTRAL** (Trung tính).
* Sử dụng mô hình `5CD-AI/Vietnamese-Sentiment-visobert` được tối ưu cho văn phong mạng xã hội.
* Áp dụng bộ lọc từ khóa (Rule-based) để xử lý các trường hợp AI dễ nhầm lẫn (ví dụ: "mệt mỏi", "thất bại").
* Tự động lưu lại lịch sử phân loại vào cơ sở dữ liệu SQLite.
* Hiển thị lịch sử 50 lần phân loại gần nhất.

## 🚀 Công nghệ sử dụng

* **Ngôn ngữ:** Python 3.11
* **Giao diện (Frontend):** Streamlit
* **Xử lý NLP (Backend):** Thư viện `transformers` của Hugging Face
* **Nền tảng (Framework):** PyTorch
* **Cơ sở dữ liệu:** SQLite3

## 🛠️ Cài đặt và Hướng dẫn chạy

Vui lòng thực hiện theo các bước sau để chạy ứng dụng trên máy của bạn.

**1. Clone repository (Tải code về):**
```bash
git clone [https://github.com/letris2412/Seminar_chuyen_de.git](https://github.com/letris2412/Seminar_chuyen_de.git)
cd Seminar_chuyen_de
```

**2. Tạo môi trường ảo (venv):**
* *Lưu ý: Đây là bước bắt buộc để tránh xung đột thư viện.*
```bash
python -m venv venv
```

**3. Kích hoạt môi trường ảo:**
* Trên Windows (PowerShell/CMD):
    ```powershell
    .\venv\Scripts\activate
    ```
* Trên macOS/Linux:
    ```bash
    source venv/bin/activate
    ```
*(Bạn sẽ thấy chữ `(venv)` xuất hiện ở đầu dòng lệnh)*

**4. Cài đặt các thư viện cần thiết:**
* *File `requirements.txt` đã bao gồm tất cả thư viện (torch, transformers, streamlit...)*
```bash
pip install -r requirements.txt
```

**5. Chạy ứng dụng:**
* *(Lần chạy đầu tiên sẽ mất 1-2 phút để tải mô hình VisoBERT về máy)*
```bash
python -m streamlit run app.py
```

Mở trình duyệt và truy cập vào địa chỉ `http://localhost:8501` để xem kết quả.

## 📂 Cấu trúc thư mục
```
.
├── app.py              # File chính chạy giao diện Streamlit (UI)
├── nlp_core.py         # File chứa lõi xử lý NLP (Hybrid AI)
├── requirements.txt    # Danh sách các thư viện Python
├── .gitignore          # File cấu hình bỏ qua thư mục venv khi push Git
└── sentiment_history.db  # File CSDL (sẽ tự động tạo ra khi chạy app.py)
```

## 🧑‍💻 Tác giả
* **Hoàng Văn Lê Trí** - (Phát triển Lõi NLP & Đánh giá mô hình)
* **Nguyễn Trọng Luân** - (Xây dựng Giao diện & Cơ sở dữ liệu)
```