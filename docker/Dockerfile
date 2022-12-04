FROM python@sha256:62cb64d073a60a041978385fefea85495fd1c17e4299c36469474f49db3e8297

WORKDIR /app

ADD src /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "main.py"]