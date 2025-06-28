# Dockerfile for Python Test Automation Framework

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DISPLAY=:99

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    software-properties-common \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install Allure
RUN npm install -g allure-commandline

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install
RUN playwright install-deps

# Copy source code
COPY . .

# Create directories for test outputs
RUN mkdir -p allure-results allure-report screenshots

# Expose port for Allure report
EXPOSE 8080

# Default command
CMD ["pytest", "tests/", "--alluredir=allure-results", "-v"] 