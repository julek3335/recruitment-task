FROM python:3.8-alpine
RUN mkdir /app
ADD project /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "app.py"]