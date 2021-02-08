# Jani

Jani is a janitor bot for telegram

## Flow

```bash
git checkout master
git merge dev
git tag -a 0.1.12
git push --tags
./build.sh
```

## Run bot in docker

```bash
docker build --build-arg GIT_COMMIT=$(git rev-parse --short HEAD) -t registry.digitalocean.com/apanchenko/jani:0.1 .
docker run -d --rm --name jani --env-file ~/.jani --cap-drop ALL jani
docker logs jani --follow
docker stop jani
```

## Run without docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.pip
python main.py
```

## [Push to DOCR](https://www.digitalocean.com/docs/container-registry/quickstart/)

```bash
docker tag jani registry.digitalocean.com/apanchenko/jani
docker push registry.digitalocean.com/apanchenko/jani
docker pull registry.digitalocean.com/apanchenko/jani
```
