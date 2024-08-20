# Start with the official Miniconda image as the base image
FROM continuumio/miniconda3:latest

# Install Tesseract OCR and additional dependencies
# RUN apt-get update && apt-get install -y \
#     tesseract-ocr \
#     libtesseract-dev \
#     libleptonica-dev \
#     && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set PYTHONPATH to include the /app directory
ENV PYTHONPATH=/app

# Create the Conda environment from the environment.yml file
RUN conda env create -f environment.yml

# Activate the environment, install any additional packages, and make sure the environment is activated on container start
SHELL ["conda", "run", "-n", "centauri-ocr-env", "/bin/bash", "-c"]

# Ensure the main.py script is executable
RUN chmod +x main.py

# Activate the environment and run the main.py script by default
CMD ["conda", "run", "--no-capture-output", "-n", "centauri-ocr-env", "python", "main.py"]
