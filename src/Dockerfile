FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /app/

WORKDIR /app/

RUN pip install --trusted-host pypi.python.org --upgrade pip setuptools wheel

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app/

CMD ["/usr/local/bin/python", "app.py"]
