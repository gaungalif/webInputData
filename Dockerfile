# Gunakan image Python dari Docker Hub
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Buat dan pindahkan ke direktori kerja /app
WORKDIR /app

# Install dependensi
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy sumber kode aplikasi ke dalam container
COPY . /app/

# Expose port yang akan digunakan oleh aplikasi Flask
EXPOSE 5000

# CMD untuk menjalankan aplikasi Flask
CMD ["python", "app.py"]
