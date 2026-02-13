# Multi-stage Docker build for manim-nodes

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Backend with MANIM
FROM python:3.10-slim

# Install system dependencies (including build tools for pycairo/manim)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    g++ \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    texlive-fonts-recommended \
    cm-super \
    dvipng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./backend/static

# Create data directories
RUN mkdir -p /app/data/projects /app/data/exports /app/data/temp

# Expose port
EXPOSE 8000

# Environment variables
ENV DATA_DIR=/app/data
ENV EXPORT_DIR=/app/data/exports
ENV TEMP_DIR=/app/data/temp

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
