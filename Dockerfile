FROM python:3.8-slim

WORKDIR /usr/app

COPY ./client .
COPY ./requirements.pip . 
RUN pip install --no-cache-dir -r requirements.pip

CMD [ "python", "jani.py" ]
