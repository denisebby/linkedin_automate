# Use a image with selenium and python
FROM selenium/standalone-chrome:latest

# Set the working directory to /app
WORKDIR /app

# Copy the files to the working directory
COPY requirements.txt .

USER root
# Install pip
RUN set -xe \
    && apt-get update \
    && apt-get -y install python3-pip

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to the working directory
COPY . .

# Run the command to start the application
ENTRYPOINT ["python3", "invite.py"]
