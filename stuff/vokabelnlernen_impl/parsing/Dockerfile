FROM python:3.10-alpine
RUN mkdir /app
COPY src/ /app/src
COPY repository.yml /app
COPY pubsub.yml /app
COPY main.py /app
COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt
WORKDIR /app
