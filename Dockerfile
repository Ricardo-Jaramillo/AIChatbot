FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port for Streamlit
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "src/main.py"]