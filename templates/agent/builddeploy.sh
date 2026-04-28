docker stop agent || true
docker rm agent || true
docker build -t agent .
docker run -d -p 8080:8080 --name agent agent
docker image prune -f