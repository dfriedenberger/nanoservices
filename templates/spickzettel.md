

# Installation, Build and Test


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
