# 📜 HƯỚNG DẪN TRIỂN KHAI BOT DISCORD TU TIÊN AI 24/7 (GROQ API + RAILWAY)

Dự án Bot Discord AI phong cách Tu Tiên Tiên Hiệp hoàn chỉnh bằng Python 3.12, sử dụng **discord.py** mới nhất và **Groq Chat Completions API** (Llama 3.3 70B Versatile).

---

## 🌟 Chức năng nổi bật

- 📊 **Cơ Sở Trí Thức từ Excel / CSV**: Tự động tra cứu dữ liệu từ file `data.xlsx` hoặc `knowledge.csv` để trả lời chính xác khi người dùng đặt câu hỏi.
- 🤖 **Phong cách Vô Danh Lão Tổ**: Xưng hô "lão phu/tiểu hữu", khẩu khí uy nghiêm, điềm tĩnh, đi thẳng vào trọng tâm tiết kiệm token.
- ⚡ **Groq SDK Cực Nhanh**: Tốc độ phản hồi cực cao với danh sách model ưu tiên tự động chuyển đổi:
  1. `llama-3.3-70b-versatile`
  2. `openai/gpt-oss-120b`
  3. `llama-3.1-8b-instant`
- 🛡️ **Exponential Backoff & Retry**: Tự động thử lại khi gặp 429 Rate Limit, Timeout, 503 Service Unavailable hoặc lỗi kết nối.
- 🧠 **Memory Management (20 tin nhắn)**: Lưu lịch sử hội thoại riêng biệt theo từng Channel.
- ✂️ **Tự động chia nhỏ văn bản (>2000 chars)**: Giữ nguyên định dạng Markdown & Code block.
- 💬 **Chế độ phản hồi linh hoạt**: Chỉ trả lời trong `CHANNEL_ID` cố định HOẶC khi được `@mention`.
- 📊 **Hệ thống Logging chi tiết**: Đo thời gian (ms), số lượng tokens, tên user, channel và model sử dụng.
- 🚀 **Sẵn sàng chạy 24/7 trên Railway**: Kèm sẵn file `Procfile`, `runtime.txt`, `requirements.txt`.

---

## 📁 Cấu trúc thư mục Project

```text
.
├── bot.py           # Entry point khởi chạy bot, xử lý sự kiện Discord
├── config.py        # Cấu hình biến môi trường, system prompt, model priority
├── groq_client.py   # Wrapper kết nối Groq SDK + Exponential Backoff
├── memory.py        # Quản lý bộ nhớ lịch sử chat từng channel (Max 20 msgs)
├── utils.py         # Hàm cắt tin nhắn >2000 ký tự, logger định dạng
├── requirements.txt # Danh sách thư viện Python cần thiết
├── .env.example     # File mẫu cấu hình biến môi trường
├── Procfile         # Cấu hình Worker khởi chạy trên Railway
└── runtime.txt      # Phiên bản Python 3.12.2
```

---

## 🛠️ Hướng dẫn cài đặt & Chạy Local (Máy tính cá nhân)

### Bước 1: Tải mã nguồn & Tạo môi trường ảo
```bash
# Clone hoặc tải dự án về máy
git clone https://github.com/your-username/discord-tutien-ai-bot.git
cd discord-tutien-ai-bot

# Tạo môi trường ảo Python 3.12
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate

# Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt
```

### Bước 2: Tạo ứng dụng Bot trên Discord Developer Portal
1. Truy cập [Discord Developer Portal](https://discord.com/developers/applications).
2. Nhấn **New Application**, đặt tên cho Bot (ví dụ: `Cửu Thiên Tiên Tôn`).
3. Vào mục **Bot**:
   - Nhấn **Reset Token** để lấy `DISCORD_TOKEN`.
   - Cuộn xuống phần **Privileged Gateway Intents**: BẬT **Message Content Intent** (Bắt buộc để bot đọc tin nhắn).
4. Vào mục **OAuth2 -> URL Generator**:
   - Select Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Read Message History`, `Embed Links`, `Attach Files`, `Use External Emojis`.
   - Copy đường link tạo ra để mời Bot vào Server Discord của bạn.

### Bước 3: Cấu hình File `.env`
Tạo file `.env` dựa trên file `.env.example`:
```env
DISCORD_TOKEN="Token_discord_bot_cua_ban"
GROQ_API_KEY="Key_groq_api_cua_ban"
CHANNEL_ID="1234567890123456789" # Hoặc để 0 nếu muốn bot trả lời khi mention ở mọi channel
```

### Bước 4: Chạy thử Bot
```bash
python bot.py
```

---

## ☁️ Hướng dẫn Triển khai 24/7 Miễn phí / Giá rẻ trên Railway & GitHub

### Bước 1: Đẩy mã nguồn lên GitHub
1. Tạo một repository mới trên GitHub (Ví dụ: `discord-tutien-bot`).
2. Push toàn bộ mã nguồn lên GitHub:
   ```bash
   git init
   git add .
   git commit -m "Khởi tạo Bot Tu Tiên Discord"
   git branch -M main
   git remote add origin https://github.com/USERNAME/discord-tutien-bot.git
   git push -u origin main
   ```

### Bước 2: Triển khai trên Railway
1. Đăng ký/Đăng nhập tài khoản tại [Railway.app](https://railway.app/).
2. Nhấn **New Project** -> chọn **Deploy from GitHub repo**.
3. Chọn Repository `discord-tutien-bot` vừa push.
4. Sau khi import project, vào tab **Variables** trên Railway và thêm các biến môi trường:
   - `DISCORD_TOKEN` = `...`
   - `GROQ_API_KEY` = `...`
   - `CHANNEL_ID` = `...`
5. Railway sẽ tự động nhận diện file `Procfile` (`worker: python bot.py`) và triển khai bot chạy 24/7!
6. Kiểm tra tab **Logs** trên Railway để xác nhận dòng `✨ BOT ONLINE THÀNH CÔNG`.

---

## 📜 Giấy phép & Đóng góp
Dự án được phát hành theo giấy phép MIT. Mọi ý kiến đóng góp hoặc yêu cầu tính năng vui lòng tạo Issue trên GitHub!
