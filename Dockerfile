
# Use official Python image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    texlive-full \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install manim and qiskit with extras
RUN pip install --no-cache-dir \
    'manim' \
    'qiskit[visualization,all]' \
    'qiskit-aer' \
    'jupyterlab'

# Set working directory
WORKDIR /app
COPY . .

# Default command (can override when running)
CMD ["python", "-c", "import qiskit; print('Qiskit version:', qiskit.__version__)"]