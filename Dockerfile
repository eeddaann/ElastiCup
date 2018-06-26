FROM python:alpine3.7
COPY etl.py /app/etl.py
RUN ["pip", "install", "elasticsearch", "requests"] 
ENTRYPOINT ["python", "/app/etl.py"]

