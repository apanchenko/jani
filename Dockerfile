FROM python:3.8-slim

WORKDIR /usr/src/app

COPY ./src .
COPY ./requirements.pip . 
RUN pip install --no-cache-dir -r requirements.pip

CMD [ "python", "jani.py" ]
