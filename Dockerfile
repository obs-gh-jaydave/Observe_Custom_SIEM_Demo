FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ .

# Default command to run the script
CMD [ "python", "generate_events.py" ]