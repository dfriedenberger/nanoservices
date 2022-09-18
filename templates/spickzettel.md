

# Installation, Build and Test


## ziel

```
python gen-config.py
docker-compose up
init database ? Autoscripts from compose

```


## Database
```
db> docker-compose up
```

## MQTT
```
mqtt> docker-compose up
```

## repositories

media-repository, job-repository

```
python create_database.py
python create_tables.py
```

### job-controller
```
job-controller> python controller.py
```
```
docker build -t frittenburger/vocabulary-job-controller:0.0.1 .
```
```
docker run -it frittenburger/vocabulary-job-controller:0.0.1
```

## ui-service

### Implementierung

TODO: post methoden implementieren

### Test
```
ui-api> python server.py
```

```
docker build -t frittenburger/vocabulary-ui:0.0.1 .
```
```
docker run -it -p 8881:8881 frittenburger/vocabulary-ui:0.0.1
```


## download

TODO: implementieren

### Test
```
download> python main.py --id f2a68aa9-3b77-4578-bf4e-9150cbdf028c
```

```
docker build -t frittenburger/vocabulary-download-job:0.0.1 .
```
```
docker run -it frittenburger/vocabulary-download-job:0.0.1 python main.py --id f2a68aa9-3b77-4578-bf4e-9150cbdf028c
```

## parsing

TODO: implementieren

### Test
```
download> python main.py --id 00a2b563-0dfb-4c85-ae7d-354071b4d9b6
```
```
docker build -t frittenburger/vocabulary-parsing-job:0.0.1 .
```
