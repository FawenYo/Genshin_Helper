# python:3.11.3-alpine
FROM python@sha256:caafba876f841774905f73df0fcaf7fe3f55aaf9cb48a9e369a41077f860d4a7

RUN apk add --no-cache gcc musl-dev linux-headers python3-dev
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV TZ=Asia/Taipei

ADD . /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "src/main.py"]