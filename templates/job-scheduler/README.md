

## Build
docker build -t frittenburger/{name}:{version} .

## Test
docker run -it frittenburger/{name}:{version} python main.py [options] 