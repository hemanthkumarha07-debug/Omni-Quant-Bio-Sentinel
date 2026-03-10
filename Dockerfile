# Use a Python image with build tools for dlib
FROM python:3.11-slim

# Install system dependencies for OpenCV and dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project (including the .dat landmark file)
COPY . .

# Launch the Fusion Hub
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]