    # Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements files to the container
COPY requirements.txt requirements_dev.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements_dev.txt

# Copy the rest of the application code to the container
COPY . .

# Set the default command to run the compiler
CMD ["python", "nexus.py"]