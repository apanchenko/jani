FROM python:3.8-slim

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY ./requirements.pip . 
RUN pip install --no-cache-dir -r requirements.pip

COPY ./client ./client
COPY main.py .

CMD [ "python", "main.py" ]
