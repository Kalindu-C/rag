FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files from root
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen

# Copy frontend application code
COPY frontend/ ./

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["uv", "run", "streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]