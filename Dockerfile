FROM python:3.12-alpine AS builder
RUN apk update && apk upgrade
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-alpine
RUN apk update && apk upgrade
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["python3", "app.py"]
