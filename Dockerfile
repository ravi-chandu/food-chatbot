# Use a standard Python 3.9 image as the base
FROM python:3.9-slim

# Set the working directory inside the app
WORKDIR /app

# Copy the requirements file in first
COPY requirements.txt .

# Install all your Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your other files (like app.py) into the app
COPY . .

# Tell Hugging Face which port to open
EXPOSE 8501

# The command to run your Streamlit app
# We are running "app.py"
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

