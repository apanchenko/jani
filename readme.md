# Jani

Jani is a janitor bot for telegram

## run in venv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.pip
python main.py
```

## run in docker

```bash
docker build --build-arg GIT_COMMIT=$(git rev-parse --short HEAD) -t jani_dev .
docker run -d --env-file ~/.jani jani_dev
```

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
