"""
Module tương tác với Groq Chat Completions API sử dụng SDK AsyncGroq mới nhất.
Hỗ trợ:
1. Thử lần lượt các model trong danh sách ưu tiên MODEL_PRIORITY_LIST.
2. Tự động Retry với Exponential Backoff khi gặp Rate Limit (429), Timeout, 503, Connection Error.
3. Đo đếm thời gian phản hồi và số lượng Token tiêu thụ.
4. Thiết kế modular độc lập: Dễ dàng thay đổi file này sang OpenAI / Gemini / OpenRouter.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from groq import AsyncGroq, GroqError, RateLimitError, APIConnectionError, APIStatusError

import config
from utils import logger


class GroqAIClient:
    def __init__(self, api_key: str = config.GROQ_API_KEY):
        if not api_key:
            logger.warning("⚠️ CHÚ Ý: GROQ_API_KEY chưa được cấu hình trong file .env!")
        self.client = AsyncGroq(api_key=api_key) if api_key else None

    async def generate_response(
        self,
        messages_history: List[Dict[str, str]],
        system_prompt: str = config.SYSTEM_PROMPT
    ) -> Dict[str, Any]:
        """
        Gửi yêu cầu Chat Completion tới Groq API.
        
        Args:
            messages_history: Lịch sử tin nhắn dạng [{"role": "user"/"assistant", "content": "..."}]
            system_prompt: Prompt hệ thống định hình nhân vật

        Returns:
            Dict chứa câu trả lời, model được dùng, thời gian phản hồi, và thông tin tokens.
        """
        if not self.client:
            raise ValueError("Chưa thiết lập GROQ_API_KEY. Vui lòng kiểm tra file .env.")

        # Xây dựng danh sách tin nhắn đầy đủ gồm System Prompt + Lịch sử hội thoại
        full_messages = [{"role": "system", "content": system_prompt}] + messages_history

        last_error: Optional[Exception] = None

        # Lặp qua từng model theo thứ tự ưu tiên
        for model in config.MODEL_PRIORITY_LIST:
            logger.info(f"🔄 Đang thử kết nối AI với model: {model}...")
            
            retry_count = 0
            delay = config.INITIAL_RETRY_DELAY

            while retry_count <= config.MAX_RETRIES:
                try:
                    start_time = time.perf_counter()

                    # Gọi Groq Async Chat Completions API
                    response = await self.client.chat.completions.create(
                        model=model,
                        messages=full_messages,
                        temperature=0.7,
                        max_tokens=2048,
                        top_p=0.9
                    )

                    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

                    # Lấy câu trả lời từ AI
                    answer_text = response.choices[0].message.content or ""

                    # Trích xuất thông tin tokens
                    prompt_tokens = response.usage.prompt_tokens if response.usage else 0
                    completion_tokens = response.usage.completion_tokens if response.usage else 0
                    total_tokens = response.usage.total_tokens if response.usage else 0

                    logger.info(f"✅ Sinh câu trả lời thành công với model {model} ({elapsed_ms:.1f}ms)")

                    return {
                        "content": answer_text,
                        "model_used": model,
                        "response_time_ms": elapsed_ms,
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens
                    }

                except (RateLimitError, APIConnectionError, APIStatusError) as e:
                    last_error = e
                    status_code = getattr(e, "status_code", "Connection/Timeout")
                    
                    retry_count += 1
                    if retry_count > config.MAX_RETRIES:
                        logger.warning(
                            f"❌ Model {model} đạt tối đa số lần thử lại ({config.MAX_RETRIES}). "
                            f"Lỗi {status_code}. Chuyển sang model tiếp theo..."
                        )
                        break

                    logger.warning(
                        f"⚠️ Gặp lỗi API Groq ({status_code}) trên model {model}. "
                        f"Lần thử {retry_count}/{config.MAX_RETRIES}. Chờ {delay:.1f}s (Exponential Backoff)..."
                    )
                    
                    await asyncio.sleep(delay)
                    delay = min(delay * config.BACKOFF_FACTOR, config.MAX_RETRY_DELAY)

                except Exception as e:
                    last_error = e
                    logger.error(f"❌ Lỗi không xác định khi gọi model {model}: {e}. Chuyển model...")
                    break

        # Nếu tất cả các model đều thất bại
        raise RuntimeError(f"Tất cả các model Groq đều thất bại. Lỗi cuối cùng: {last_error}")


# Instance toàn cục để sử dụng trong bot.py
ai_client = GroqAIClient()
