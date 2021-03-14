# Jani

Jani is a janitor bot for telegram

## run in venv

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.pip
python -m client
```

## run in docker

```bash
docker build -t jani_dev .
docker run -d --env-file ~/.jani jani_dev
```

## run in compose

docker-compose up

## build and push

```bash
git checkout master
git merge feature
git tag -a 0.x.y
git push --tags
./build.sh
```

## deploy

```bash
docker pull registry.digitalocean.com/apanchenko/jani:0.x.y
docker run -d --env-file ~/.jani registry.digitalocean.com/apanchenko/jani:0.x.y
```
