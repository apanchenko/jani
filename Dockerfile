FROM python:3.8-slim

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# install required libs
COPY ./requirements.pip . 
RUN pip install -U pip \
   && pip install --no-cache-dir -r requirements.pip

# copy jani sources
COPY ./client ./client

# set version
ARG JANI_VERSION
ENV JANI_VERSION=$JANI_VERSION

# set commit hash
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

CMD [ "python", "-m", "client" ]
