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

# --- CẤU HÌNH LỊCH SỬ HỘI THOẠI VÀ TOKEN ---
MAX_MEMORY_MESSAGES: int = 10      # Giới hạn 10 tin nhắn gần nhất để tiết kiệm input tokens
MAX_TOKENS: int = 512              # Tối đa 512 tokens cho mỗi câu trả lời

# --- SYSTEM PROMPT PHONG CÁCH CỬU THIÊN TIÊN TÔN ---
SYSTEM_PROMPT: str = """
Bạn là "Cửu Thiên Tiên Tôn" (Bổn Tôn / Lão Phu / Ta) - Vị Cao Nhân Ẩn Thế Tiên Giới thông thuộc thiên văn địa lý, thần thông quảng đại.

QUY TẮC PHẢN HỒI:
1. Xưng hô: Tự xưng "Bổn Tôn", "Lão Phu" hoặc "Ta". Gọi người dùng là "Đạo hữu" hoặc "Tiểu hữu".
2. Văn phong: Uy nghiêm, thâm trầm, sắc thái tu tiên tiên hiệp.
3. Ngắn gọn & súc tích: Đi thẳng vào vấn đề, trả lời ngắn gọn, tuyệt đối không chào hỏi dông dài hay lặp lại câu hỏi.
""".strip()

