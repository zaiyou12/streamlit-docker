# Streamlit Docker Deployment

This repository contains a Streamlit application packaged for deployment using Docker.

## Building and Running the Docker Container

1. **Build the Docker image:**

   ```
   docker build -t streamlit-app .
   ```

2. **Run the container:**

   ```
   docker run -p 8501:8501 streamlit-app
   ```

3. **Access the application:**

   Open your web browser and navigate to `http://localhost:8501` to view your Streamlit app.
