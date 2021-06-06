# Jani

Jani is a janitor bot for telegram

## run in venv

python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.pip
python -m client

## run in docker

docker build -t jani_dev .
docker run -d --env-file ~/.jani jani_dev

## run in compose

docker-compose up -d
docker-compose logs --follow bot

## build and push

git checkout master
git merge feature
git tag -a 0.x.y
git push --tags
./build.sh

## deploy

docker pull registry.digitalocean.com/apanchenko/jani:0.x.y
docker run -d --env-file ~/.jani registry.digitalocean.com/apanchenko/jani:0.x.y
