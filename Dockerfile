# Install the base requirements for the app
FROM python:alpine AS base
WORKDIR /app

# Copy everything over
COPY . .

# Install Python requirements
RUN pip install -r requirements.txt

# Start the app
CMD ["python3", "monitor.py", "--handle", "BillNye", "--interval", "1"]
