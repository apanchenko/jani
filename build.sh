docker build --build-arg GIT_COMMIT=$(git rev-parse --short HEAD) -t registry.digitalocean.com/apanchenko/jani:0.1.0 .

docker push registry.digitalocean.com/apanchenko/jani:0.1.0