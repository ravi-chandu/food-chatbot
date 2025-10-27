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
# We've added "--server.headless=true" to fix the "Stopping..." error
# UPDATED to run your "food-chatbot.py" file
CMD ["streamlit", "run", "food-chatbot.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

