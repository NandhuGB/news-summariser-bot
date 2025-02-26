# Use an official Python image as the base
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set the default command to run your bot
CMD ["python", "app/main.py"]