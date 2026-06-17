# Use a small, official Python image
FROM python:3.12-slim

# Set the folder inside the container where commands will run
WORKDIR /app

# Install the Flask package
RUN pip install --no-cache-dir flask

# Copy your app.py file into the container
COPY app.py .

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

