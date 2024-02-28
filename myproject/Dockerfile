FROM python:3.9

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World


# Run app.py when the container launches
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
