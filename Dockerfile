FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Expose the port your Gunicorn app runs on
EXPOSE 9351

# Run Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9351", "pythonserver:app"]