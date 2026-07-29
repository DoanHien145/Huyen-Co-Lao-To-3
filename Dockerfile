FROM python:3.12-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép và cài đặt các thư viện cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn bot vào container
COPY . .

# Chạy bot Discord
CMD ["python", "bot.py"]
