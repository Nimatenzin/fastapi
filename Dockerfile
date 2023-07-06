# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory to the working directory
COPY app/ .

# Expose the port on which the FastAPI application will run (e.g., 8000)
EXPOSE 8000

# Define the command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
