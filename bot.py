"""
File khởi chạy chính của Bot Discord Tu Tiên AI.
Sử dụng library discord.py mới nhất và lập trình bất đồng bộ 100% (async/await).
"""

import sys
import discord
from discord.ext import commands

import config
from groq_client import ai_client
from memory import memory_manager
from utils import logger, split_message, format_ai_log

# Cấu hình Discord Intents
intents = discord.Intents.default()
intents.message_content = True  # Bắt buộc bật Message Content Intent trên Discord Developer Portal
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Sự kiện được gọi khi Bot đăng nhập thành công vào Discord."""
    logger.info("==================================================")
    logger.info(f"✨ BOT ONLINE THÀNH CÔNG: {bot.user.name} (ID: {bot.user.id})")
    logger.info(f"📌 Đang phục vụ trên {len(bot.guilds)} máy chủ Discord.")
    if config.CHANNEL_ID:
        logger.info(f"🎯 Channel cố định phản hồi ID: {config.CHANNEL_ID}")
    else:
        logger.info("💬 Chế độ tự do: Bot phản hồi khi được @mention trong mọi channel.")
    logger.info("==================================================")

    # Đặt trạng thái hoạt động của Bot
    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name="Kinh Văn Tiên Giới | @mention để đàm đạo"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.event
async def on_message(message: discord.Message):
    """Xử lý mọi tin nhắn đến theo các tiêu chí yêu cầu."""
    # Xử lý lệnh Discord (ví dụ !sync)
    await bot.process_commands(message)

    # 1. Bỏ qua tin nhắn từ chính bot hoặc các bot khác
    if message.author.bot:
        return

    # 2. Kiểm tra điều kiện phản hồi: Được mention HOẶC nằm trong CHANNEL_ID cấu hình
    is_mentioned = bot.user in message.mentions if bot.user else False
    is_in_target_channel = (config.CHANNEL_ID is not None) and (message.channel.id == config.CHANNEL_ID)

    if not (is_mentioned or is_in_target_channel):
        # Nếu không thỏa điều kiện, bỏ qua không phản hồi
        return

    # Làm sạch nội dung câu hỏi (Xóa tag @Bot nếu người dùng mention)
    prompt = message.content
    if bot.user:
        prompt = prompt.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()

    if not prompt:
        # Nếu người dùng chỉ tag bot mà không nhập nội dung
        await message.channel.send(f"Bổn Tôn nghe đây! {message.author.mention} đạo hữu có điều chi cần chỉ giáo?")
        return

    # 3. Hiển thị trạng thái "Typing..." trong lúc AI đang sinh câu trả lời
    async with message.channel.typing():
        # Lịch sử hội thoại của channel hiện tại
        channel_id = message.channel.id

        # Lưu tin nhắn người dùng vào Memory
        memory_manager.add_message(channel_id, "user", prompt)

        # Lấy lịch sử 20 tin nhắn gần nhất
        history = memory_manager.get_history(channel_id)

        try:
            # 4. Gọi Groq AI Client với cơ chế Fallback & Backoff
            result = await ai_client.generate_response(messages_history=history)

            answer_text = result["content"]
            model_used = result["model_used"]
            elapsed_ms = result["response_time_ms"]
            p_tokens = result["prompt_tokens"]
            c_tokens = result["completion_tokens"]
            t_tokens = result["total_tokens"]

            # Lưu câu trả lời của AI vào Memory
            memory_manager.add_message(channel_id, "assistant", answer_text)

            # 5. Chia nhỏ tin nhắn nếu dài hơn 2000 ký tự (Giới hạn của Discord)
            chunks = split_message(answer_text, max_length=1950)

            for chunk in chunks:
                await message.channel.send(chunk)

            # 6. Ghi Log chi tiết hệ thống
            log_str = format_ai_log(
                user_name=f"{message.author.name} ({message.author.id})",
                channel_name=f"{message.channel} ({message.channel.id})",
                prompt=prompt,
                model=model_used,
                response_time_ms=elapsed_ms,
                prompt_tokens=p_tokens,
                completion_tokens=c_tokens,
                total_tokens=t_tokens
            )
            logger.info(log_str)

        except Exception as e:
            logger.error(f"❌ Lỗi xử lý yêu cầu cho {message.author} tại channel {channel_id}: {e}")
            
            # Thông báo lỗi thân thiện chuẩn phong cách Tu Tiên
            error_msg = (
                f"❌ **Linh khí đứt đoạn!** {message.author.mention} đạo hữu thông cảm, "
                f"thiên địa linh khí tạm thời xáo trộn (Groq API gặp sự cố hoặc quá tải). "
                f"Bổn Tôn chưa thể thấu thị thiên cơ lúc này. Vui lòng thử lại sau ít phút!"
            )
            await message.channel.send(error_msg)


def main():
    """Hàm khởi chạy chính kiểm tra cấu hình trước khi chạy bot."""
    if not config.DISCORD_TOKEN:
        logger.critical("❌ THẤT BẠI: Chưa cung cấp DISCORD_TOKEN trong file .env!")
        logger.critical("👉 Vui lòng tạo file .env từ .env.example và điền token hợp lệ.")
        sys.exit(1)

    if not config.GROQ_API_KEY:
        logger.warning("⚠️ CẢNH BÁO: Chưa cung cấp GROQ_API_KEY trong file .env. Bot sẽ không thể kết nối AI!")

    logger.info("🚀 Đang khởi động Bot Discord Tu Tiên AI...")
    try:
        bot.run(config.DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        logger.critical("❌ LỖI ĐĂNG NHẬP: DISCORD_TOKEN không hợp lệ. Vui lòng kiểm tra lại token!")
    except Exception as e:
        logger.critical(f"❌ LỖI KHÔNG MONG MUỐN KHI CHẠY BOT: {e}")


if __name__ == "__main__":
    main()
