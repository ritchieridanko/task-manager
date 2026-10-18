# ---------- Build Stage ----------
FROM python:3.11-alpine3.19 AS builder

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set work directory
WORKDIR /app

# Install Python dependencies into a venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY backend/app/ ./app/

# ---------- Runtime Stage ----------
FROM python:3.11-alpine3.19

# Install runtime dependencies
RUN apk add --no-cache libpq

# Set work directory
WORKDIR /app

# Copy venv from Build Stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy app source from Build Stage
COPY --from=builder /app/app ./app

# Copy Alembic migration files
COPY backend/alembic.ini ./
COPY backend/alembic/ ./alembic/

# Copy and set up entrypoint script
COPY backend/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Set entry point and run app
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python3", "-m", "app.main"]
