FROM python:3.7-alpine

COPY executor.py /src/executor.py
CMD ["python", "/src/executor.py"]
