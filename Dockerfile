# Copyright (c) 2025 Miguel Sierra
# Licensed under the MIT License. See LICENSE file in the project root for full license text.

FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}"]
