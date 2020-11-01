# Jani

Jani is a janitor bot for telegram

## Run bot in virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip instsall -r requirements.pip
```

## Run bot in container

```bash
docker build -f Dockerfile -t jani .
docker run -d --rm --name jani jani
docker logs jani
docker stop jani
```
