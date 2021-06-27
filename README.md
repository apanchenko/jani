# Jani

Jani is a janitor bot for telegram

## commands

- /help
- /mychats
- /ping
- /reload
- /version

## admin commands

- /allchats

## test run in compose

docker build -t jani_dev .
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
