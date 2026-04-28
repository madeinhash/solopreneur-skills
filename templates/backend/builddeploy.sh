docker stop be || true
docker rm be || true
docker build -t be .
docker run -d -p 4000:4000 --name be be
docker image prune -f