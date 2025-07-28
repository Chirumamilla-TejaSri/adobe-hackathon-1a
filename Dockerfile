# Dockerfile

FROM python:3.10-slim

WORKDIR /app

COPY ./app /app
COPY ./input /app/input
COPY ./output /app/output

RUN pip install pymupdf

CMD ["python", "extract_outline.py"]
