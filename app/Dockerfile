FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \ 
   pip install -r requirements.txt && \
    pip install --upgrade mysql-connector-python

COPY . .

# Load environment variables from .env file
ENV AWS_REGION ${AWS_REGION}
ENV SECRET_NAME ${SECRET_NAME}

CMD ["python", "app.py"]
