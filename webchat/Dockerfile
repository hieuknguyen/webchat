FROM python:3.10-slim

# Cài các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    libgl1-mesa-glx \
    tesseract-ocr \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Tạo thư mục dự án
WORKDIR /app

# Copy requirements và cài đặt
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn
COPY . .

# Mở port Django
EXPOSE 8000

# Chạy server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
