#use lightweight python image
FROM python:3.11-slim

#set up working directory
WORKDIR /app

#Copy Dependencies
COPY ./req.txt .

# install dependencies
RUN pip install --no-cache-dir -r req.txt

# copy app code
COPY app ./app

# Expose port
EXPOSE 8000

# run the server
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]