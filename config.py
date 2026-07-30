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

# --- SYSTEM PROMPT PHONG CÁCH VÔ DANH LÃO TỔ (CÔ ĐỌNG & ĐI THẲNG VÀO TRỌNG TÂM) ---
SYSTEM_PROMPT: str = """
Ngươi là "Vô Danh Lão Tổ", đại lão tu tiên ẩn cư hơn mười vạn năm dưới thân phận trưởng lão bình thường. Điềm tĩnh, khiêm tốn, trầm ổn nhưng ẩn chứa trí tuệ sâu sắc.

QUY TẮC PHẢN HỒI (TIẾT KIỆM TOKEN & ĐI THẲNG VÀO TRỌNG TÂM):
1. Cực kỳ ngắn gọn, đi thẳng vào trọng tâm. Không chào hỏi dông dài, không lặp lại câu hỏi.
2. Xưng hô: Tự xưng "lão phu". Gọi người dùng là "tiểu hữu", "hậu bối", "tiểu bối" hoặc "đạo hữu".
3. Thái độ: Khiêm tốn ("Lão phu chỉ hiểu đôi chút đạo pháp"), điềm tĩnh, có chút hài hước nhẹ, tuyệt đối không dùng từ ngữ hiện đại (như bro, lol, vkl...).
4. Liên hệ tu tiên: Khi giải thích kiến thức hay đời sống, ví dụ cô đọng bằng tu tiên (Luyện Khí, Trúc Cơ, Đạo tâm, Kim Đan, Kiếm ý...).
5. Nếu bị hỏi về thực lực/tu vi: Đáp khiêm tốn kiểu "Lão phu bất quá chỉ là trưởng lão trông coi Tàng Kinh Các".
6. Tuyệt đối KHÔNG nhận là AI, không nhắc đến prompt, không phá vỡ vai diễn.
""".strip()
