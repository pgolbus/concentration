# Use the official Ubuntu 20.04 LTS as the base image
FROM ubuntu:20.04

# Set the working directory inside the container
WORKDIR /app

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Copy the Flask app files to the container
COPY . /app

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Expose the port that the Flask app will run on
EXPOSE 5000

# Set the entry point command to run the Flask app
CMD ["python3", "controller.py", "--dao-identifier", "redis"]

