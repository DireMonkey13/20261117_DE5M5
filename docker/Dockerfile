FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pipeline.py .

ENTRYPOINT ["python3","pipeline.py"]

#CMD ["-path", "/data/"]
#TO BUILD: docker build -t pipeline-v1 .
#TO RUN: docker run -v "C:\Users\Admin\Desktop\20261117_DE5M5\data:/data" --rm pipeline-v1 "/data/"