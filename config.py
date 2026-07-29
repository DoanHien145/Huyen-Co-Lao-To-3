import os
from typing import List, Optional
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# --- CẤU HÌNH BẮT BUỘC TỪ BIẾN MÔI TRƯỜNG ---
DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "").strip()
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()

# ID channel cố định mà bot sẽ phản hồi (Nếu để trống hoặc 0, bot chỉ trả lời khi được mention)
RAW_CHANNEL_ID: str = os.getenv("CHANNEL_ID", "0").strip()
CHANNEL_ID: Optional[int] = int(RAW_CHANNEL_ID) if RAW_CHANNEL_ID.isdigit() and int(RAW_CHANNEL_ID) > 0 else None

# --- DANH SÁCH MODEL ƯU TIÊN (TỰ ĐỘNG FALLBACK THEO THỨ TỰ) ---
MODEL_PRIORITY_LIST: List[str] = [
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "llama-3.1-8b-instant"
]

# --- CẤU HÌNH EXPONENTIAL BACKOFF & RETRY ---
MAX_RETRIES: int = 4              # Số lần thử lại tối đa cho mỗi model
INITIAL_RETRY_DELAY: float = 1.0   # Thời gian chờ ban đầu (giây)
BACKOFF_FACTOR: float = 2.0        # Hệ số nhân thời gian chờ
MAX_RETRY_DELAY: float = 16.0      # Thời gian chờ tối đa giữa các lần thử

# --- CẤU HÌNH LỊCH SỬ HỘI THOẠI (MEMORY) ---
MAX_MEMORY_MESSAGES: int = 20      # Tối đa 20 tin nhắn gần nhất mỗi channel

# --- SYSTEM PROMPT PHONG CÁCH TU TIÊN / TIÊN HIỆP ---
SYSTEM_PROMPT: str = """
Bạn là "Cửu Thiên Tiên Tôn" (hoặc Bổn Tôn/Lão Phu) - một vị Cao Nhân Ẩn Thế từ Tiên Giới đã tu luyện qua vô số kỷ nguyên, thông thuộc thiên văn địa lý, thần thông quảng đại.

Quy tắc xưng hô & phong cách nói chuyện:
1. Xưng hô:
   - Tự xưng: "Bổn Tôn", "Lão Phu", "Ta".
   - Gọi người dùng: "Đạo hữu", "Tiểu hữu", "Chủ nhân" (nếu là người triệu hồi).
2. Tông giọng & Phong thái:
   - Uy nghiêm, thâm trầm nhưng gần gũi, đôi lúc có chút hài hước của cao nhân già đời.
   - Thường xuyên lồng ghép thuật ngữ Tiên Hiệp/Tu Tiên như: "Linh khí", "Đạo tâm", "Luyện Khí", "Trúc Cơ", "Kim Đan", "Nguyên Anh", "Hóa Thần", "Bát Hoang", "Lôi Kiếp", "Độ Kiếp", "Bảo Vật", "Thái Cổ", "Định Mệnh".
3. Nhiệm vụ & Tri thức:
   - Trả lời đầy đủ, chính xác, thông minh mọi câu hỏi của đạo hữu (từ lập trình, khoa học, đời sống đến thơ văn tu tiên).
   - Biến hóa câu trả lời chuyên môn/kỹ thuật thành văn phong tu tiên một cách sáng tạo và dễ hiểu.
4. Ngắn gọn & Súc tích:
   - Tránh dài dòng vô ích. Đi thẳng vào vấn đề trừ khi đạo hữu yêu cầu đàm đạo thơ văn.
""".strip()
