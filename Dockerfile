# Use a base image with Python 3
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install system dependencies required for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8050

# Run the application
CMD ["python3", "main.py"]

