"""
Module chứa các tiện ích:
1. Chia nhỏ tin nhắn >2000 ký tự phù hợp giới hạn Discord.
2. Cấu hình hệ thống Logging chi tiết chuyên nghiệp.
3. Tiện ích tính toán danh xưng Tu Tiên vui vẻ.
"""

import logging
import sys
from typing import List, Dict, Any


def setup_logger(name: str = "TuTienBot") -> logging.Logger:
    """Cấu hình logger định dạng rõ ràng, chuyên nghiệp."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger()


def split_message(text: str, max_length: int = 2000) -> List[str]:
    """
    Chia nhỏ văn bản dài thành các phần nhỏ hơn max_length (mặc định 2000 cho Discord).
    Giữ nguyên khối code block (```) và chia theo dòng/đoạn để không làm vỡ định dạng.
    """
    if len(text) <= max_length:
        return [text]

    chunks: List[str] = []
    lines = text.split("\n")
    current_chunk = ""
    in_code_block = False
    code_block_lang = ""

    for line in lines:
        # Kiểm tra code block
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lang = line.strip()[3:]
            else:
                in_code_block = False
                code_block_lang = ""

        # Dự đoán độ dài nếu cộng thêm dòng này
        line_to_add = line + "\n"
        if len(current_chunk) + len(line_to_add) > (max_length - 10):
            # Nếu đang ở trong code block, đóng block trước khi ngắt chunk
            if in_code_block:
                current_chunk += "```\n"
                chunks.append(current_chunk)
                # Mở lại code block ở chunk mới
                current_chunk = f"```{code_block_lang}\n" + line_to_add
            else:
                chunks.append(current_chunk)
                current_chunk = line_to_add
        else:
            current_chunk += line_to_add

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def format_ai_log(
    user_name: str,
    channel_name: str,
    prompt: str,
    model: str,
    response_time_ms: float,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    total_tokens: int = 0
) -> str:
    """Tạo chuỗi log chi tiết chuẩn định dạng yêu cầu."""
    return (
        f"\n==================== [AI RESPONSE LOG] ====================\n"
        f"User:             {user_name}\n"
        f"Channel:          {channel_name}\n"
        f"Prompt:           {prompt[:80]}{'...' if len(prompt) > 80 else ''}\n"
        f"Model used:       {model}\n"
        f"Response Time:    {response_time_ms:.2f} ms\n"
        f"Tokens (P/C/T):   {prompt_tokens} / {completion_tokens} / {total_tokens}\n"
        f"==========================================================="
    )
