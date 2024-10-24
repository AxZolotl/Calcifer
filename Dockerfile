FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV http_proxy=deb.debian.org/debian
ENV https_proxy=deb.debian.org/debian

# Install necessary packages and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgtk-3-dev \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    gcc \
    tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Copy local code to the container image.
COPY . /app

# Install Python dependencies (from config/requirements.txt)
COPY config/requirements.txt /app/config/
RUN pip install --upgrade pip && pip install --root-user-action=ignore -r /app/config/requirements.txt

# Give execution permissions to the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
