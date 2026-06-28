FROM python:3.12-slim AS builder
RUN apt update && apt upgrade -y
WORKDIR /app
COPY requirements.txt .
RUN pip install --user  -r requirements.txt

FROM python:3.12-slim
RUN apt update && apt upgrade -y
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
