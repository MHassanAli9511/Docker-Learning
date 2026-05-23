FROM python:3.8-slim
WORKDIR /app

COPY . .

RUN pip install flask redis
EXPOSE 5000
CMD ["python", "My_Flask_app.py"]