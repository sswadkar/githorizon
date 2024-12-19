FROM python:3.10-slim

# Set the working directory
WORKDIR /docker


# Copy the app and install dependencies
COPY ./docker .
RUN pip install --no-cache-dir -r requirements.txt

# Install using cache
RUN python3 -c "from litgpt import LLM; LLM.load('microsoft/phi-2')"

# Expose the Flask port
EXPOSE 5000

# Start the server
CMD ["python", "app.py"]