# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

FROM python:3.12.8-slim

#This will set the working directory within the container to /app
WORKDIR /app
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install pdfplumber
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch to the non-privileged user to run the application.

# Copy the source code into the container.
COPY ./src/Utils_AI.py .
COPY ./src/QnA_over_docs_streamlit.py .

# Expose the port that the application listens on.
EXPOSE 8085

# Run the application.
CMD ["streamlit", "run", "QnA_over_docs_streamlit.py"]
 # Always give commands in double quotes
