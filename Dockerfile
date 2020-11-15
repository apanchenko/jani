FROM python:3.8-slim

WORKDIR /usr/app

COPY ./requirements.pip . 
RUN pip install --no-cache-dir -r requirements.pip

COPY ./client .

CMD [ "python", "main.py" ]
