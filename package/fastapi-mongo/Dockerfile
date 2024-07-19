#Use the official image as a parent image
FROM python:latest

# Set the working directory
WORKDIR /app

# Install the dependencies
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Start the server
CMD ["uvicorn","main:app","--host","0.0.0.0", "--port", "8000"]

