FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY . .

# Install dependencies
RUN uv sync --frozen

# Hugging Face Spaces requires port 7860
EXPOSE 7860

# Run both servers via start script
CMD ["bash", "start.sh"]