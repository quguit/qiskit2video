# Use official Python image
FROM python:3.11-slim

# Install system dependencies
# - build-essential / python3-dev / pkg-config: needed to build pycairo/manimpango if no prebuilt wheel matches
# - libcairo2-dev / libpango1.0-dev: required by Manim for text/shape rendering
# - ffmpeg: required by Manim for video encoding
# - texlive subset: required by Manim for Tex/MathTex (texlive-full is unnecessary and adds ~5GB)
# - libgl1: required for OpenGL rendering (replaces libgl1-mesa-glx on newer Debian)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    libgl1 \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    tipa \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install all Python dependencies from a single source of truth.
# Pin manim, qiskit, qiskit-aer, jupyterlab in requirements.txt itself
# (avoid a second separate pip install with unpinned versions).
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888

# Default command (override at runtime / in docker-compose.yml)
CMD ["python", "-c", "import qiskit; print('Qiskit version:', qiskit.__version__)"]
