FROM python:alpine3.7
COPY etl.py /app/etl.py
RUN ["pip", "install", "elasticsearch", "requests","retrying"] 
ENTRYPOINT ["python", "/app/etl.py","--log=INFO"]

