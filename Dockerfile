# 1. Use an official, lightweight Python runtime base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy our requirements file first to take advantage of Docker caching layers
COPY requirements.txt .

# 4. Install production dependencies cleanly without storing cache files
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire project code into the container
COPY . .

# 6. Expose the port that our FastAPI server runs on
EXPOSE 8000

# 7. Set the Python path variable so imports find the src folder
ENV PYTHONPATH=/app

# 8. Command to start the FastAPI server via Uvicorn when the container launches
CMD ["python", "src/main.py"]
