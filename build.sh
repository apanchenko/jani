JANI_VERSION=$(git describe)

docker build\
    --build-arg GIT_COMMIT=$(git rev-parse --short HEAD)\
    --build-arg JANI_VERSION=$JANI_VERSION\
    -t registry.digitalocean.com/apanchenko/jani:$JANI_VERSION .

docker push registry.digitalocean.com/apanchenko/jani:$JANI_VERSION