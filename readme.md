# Jani

Jani is a janitor bot for telegram

## Run bot

```bash
docker build -t jani .
docker run -d --rm --name jani --env-file ~/.jani jani
docker run -d --rm --name jani --env-file ~/.jani --cap-drop ALL jani
docker logs jani --follow
docker stop jani
```

## [Push to DOCR](https://www.digitalocean.com/docs/container-registry/quickstart/)

```bash
docker tag <IMAGE ID> registry.digitalocean.com/apanchenko/jani
docker push registry.digitalocean.com/apanchenko/jani
```
