# Use the official Python image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose the port Django runs on
EXPOSE 8000

# Run Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
