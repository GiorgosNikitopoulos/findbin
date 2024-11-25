# Use the official Debian "bookworm" image as the base image
FROM debian:buster

# Set environment variables if needed
ENV DEBIAN_FRONTEND noninteractive

# Update package lists and install any necessary packages
RUN apt-get update && \
    apt-get install -y git
#&& \
    #rm -rf /var/lib/apt/lists/*

RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN python3 -m pip install schedule
RUN python3 -m pip install requests
# Add your application's files to the container
COPY ./app /app
RUN mkdir /data
RUN mkdir /output_data
RUN mkdir /temp

# Set the working directory
WORKDIR /app

# Define the command to run when the container starts
#CMD ["tail", "-f", "/dev/null"]
CMD ["python3.7", "findbin.py"]
#"--polling_time", "60", "--schedule_time", "12"]

# Expose any necessary ports
# EXPOSE <port>

# You can include additional Dockerfile instructions here as needed

