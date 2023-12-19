# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Don't forget to copy to usr/scr/app
# Set the working directory in the container
WORKDIR /app

# Need to find a way to setup env var using a .sh file 
# issue: script is bin/sh and I need bin/bash -> could use GitHub secrets 
# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --no-cache-dir -e 'backend/src'

# Need to run uvicorn server 
# Make port 80 available to the world outside this container
EXPOSE 80


