# Base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY templates templates
COPY main.py .
COPY wsgi.py .

# Expose the desired port
EXPOSE 8080

# Specify the command to run when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "60", "wsgi:app"]