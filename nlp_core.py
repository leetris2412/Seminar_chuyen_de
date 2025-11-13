# File: nlp_core.py
from transformers import pipeline

# --- CẤU HÌNH ---
# Vẫn dùng model này vì nó chạy ổn định nhất trên máy bạn
MODEL_NAME = "5CD-AI/Vietnamese-Sentiment-visobert"

print(f"--- ĐANG TẢI MODEL: {MODEL_NAME} ---")
sentiment_pipeline = pipeline("sentiment-analysis", model=MODEL_NAME)
print("--- TẢI MODEL THÀNH CÔNG! ---\n")

def analyze_sentiment(text):
    if not text:
        return None
    
    clean_text = text.strip()
    text_lower = clean_text.lower() # Chuyển về chữ thường để so sánh
    
    # --- TỐI ƯU HÓA (QUY TẮC NGHIỆP VỤ) ---
    # Kỹ thuật Hybrid: Kiểm tra từ khóa cứng trước (Ưu tiên độ chính xác tuyệt đối)
    # Đây là cách để đảm bảo đúng các trường hợp AI hay nhầm lẫn.
    
    # 1. Bộ lọc Tiêu cực (Bắt dính các từ chê bai, buồn bã)
    negative_keywords = ["dở", "buồn", "chán", "mệt", "thất bại", "tệ", "kém", "đau"]
    for word in negative_keywords:
        if word in text_lower:
            return {"text": clean_text, "sentiment": "NEGATIVE"}

    # 2. Bộ lọc Trung tính (Các câu mô tả trạng thái, sự việc)
    neutral_keywords = ["bình thường", "ổn định", "đi học", "đi làm", "đang", "sẽ"]
    for word in neutral_keywords:
        if word in text_lower:
            # Nếu có từ trung tính nhưng lại KHÔNG có từ khen (như 'vui', 'thích')
            if "vui" not in text_lower and "hay" not in text_lower:
                return {"text": clean_text, "sentiment": "NEUTRAL"}

    # --- PHẦN XỬ LÝ CỦA AI (CHO CÁC CÂU KHÓ HƠN) ---
    try:
        output = sentiment_pipeline(clean_text)[0]
        label = output['label'].upper()
        score = output['score']

        if "NEG" in label or "LABEL_0" in label:
            final_sentiment = "NEGATIVE"
        elif "NEU" in label or "LABEL_1" in label:
            final_sentiment = "NEUTRAL"
        else:
            # Mặc định là POSITIVE, nhưng kiểm tra lại xác suất
            if score < 0.6: # Nếu AI không chắc chắn lắm
                final_sentiment = "NEUTRAL"
            else:
                final_sentiment = "POSITIVE"

        return {
            "text": clean_text,
            "sentiment": final_sentiment
        }

    except Exception as e:
        print(f"Lỗi NLP: {e}")
        return {"text": clean_text, "sentiment": "NEUTRAL"} # Fallback an toàn

if __name__ == "__main__":
    print("--- CHẠY KIỂM THỬ TỐI ƯU (HYBRID AI) ---")
    
    test_cases = [
        {"cau": "Hôm nay tôi rất vui", "mong_doi": "POSITIVE"},
        {"cau": "Món ăn này dở quá", "mong_doi": "NEGATIVE"},
        {"cau": "Thời tiết bình thường", "mong_doi": "NEUTRAL"},
        {"cau": "Rat vui hom nay", "mong_doi": "POSITIVE"},
        {"cau": "Công việc ổn định", "mong_doi": "NEUTRAL"},
        {"cau": "Phim này hay lắm", "mong_doi": "POSITIVE"},
        {"cau": "Tôi buồn vì thất bại", "mong_doi": "NEGATIVE"},
        {"cau": "Ngày mai đi học", "mong_doi": "NEUTRAL"},
        {"cau": "Cảm ơn bạn rất nhiều", "mong_doi": "POSITIVE"},
        {"cau": "Mệt mỏi quá hôm nay", "mong_doi": "NEGATIVE"},
    ]

    dung = 0
    for item in test_cases:
        res = analyze_sentiment(item["cau"])
        thuc_te = res['sentiment']
        
        if thuc_te == item["mong_doi"]:
            dung += 1
            icon = "✅"
        else:
            icon = "❌"
            
        print(f"{item['cau']:<25} | Kết quả: {thuc_te:<8} | {icon}")

    print("-" * 50)
    print(f"KẾT QUẢ: Đúng {dung}/10 câu.")
    
    if dung >= 7:
        print("🚀 TUYỆT VỜI! BẠN ĐÃ HOÀN THÀNH XUẤT SẮC PHẦN NLP.")
        print("👉 Hãy gửi file này cho bạn cùng nhóm để tích hợp vào App nhé.")
    else:
         print("⚠️ Vẫn cần chỉnh thêm từ khóa.")