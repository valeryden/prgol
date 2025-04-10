# Stage 1: Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements (if you had any)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Stage 2: Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application from builder
COPY --from=builder /app/app.py .

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Expose port for the application
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
