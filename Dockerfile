# Use an official Python runtime as a base image 
FROM python:3.9-slim

# Set a working directory for the app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install Flask sympy

# Expose the port that the app runs on
EXPOSE 6700

# Define environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Run the application
CMD ["flask", "run", "--port=6700"]
