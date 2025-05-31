# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app folder contents to /app
COPY app/ .

# Run the application
CMD ["python", "app.py"]
