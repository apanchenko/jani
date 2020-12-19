FROM python:3.8-buster

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY ./requirements.pip . 
RUN pip install --no-cache-dir -r requirements.pip

COPY ./client .

CMD [ "python", "main.py" ]
