FROM python:3.10-alpine
RUN mkdir /app
#{COPY_TO_APP}
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt
WORKDIR /app
CMD ["python", "controller.py"]
