# Build an image for the Todo web service.
# Base: For reproducibility, explicitly specify slim-bullseye or slim-bookworm.
FROM python:3.11-slim

# Set the working directory inside the container. Makes all paths relative to this.
WORKDIR /app

# Install netstat (net-tools) and ping (iputils-ping) for debugging.
# 'curl' package installs *many* others (> 15MB downloads) so skip it.
# Better to install curl as needed in a running container
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends net-tools iputils-ping && \
#    rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code. The actual target dir is /app/
COPY  ./src  .

# Run the FastAPI application with Uvicorn.
# "--reload" causes app to check for changes to Python code and dynamically reload.
# Remove "--reload" arg for production use.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
