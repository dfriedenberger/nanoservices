# nanofunctions

gen software system from nanofunction definition

## Install

### General
```
pip install rdflib
pip install pypubsub
pip install pytest
```

### Protobuf
```
apt-get install protobuf-compiler
pip install protobuf==3.19.0
```

### Plantuml
```
apt-get install openjdk-17-jdk
apt-get install graphviz
```

Download jar from https://plantuml.com/de/download
```
cd puml
wget https://github.com/plantuml/plantuml/releases/download/v1.2022.6/plantuml-1.2022.6.jar
```

### Extend Nano puml

https://materialdesignicons.com/

Open and save with Paint (convert transparent to white)
```
java -jar ../plantuml-1.2022.6.jar -encodesprite 16z foo.png
```

## Generate rdf Models 
```
python example_signalaspectdetection.py
python example_youtubetranslator.py
```

## Generate Documentation

TODO: generate class, sequenz, deplyoment, ... diagramms

### Generate Network Diagram
```
python create_network_diagram.py puml/youtubetranslator.ttl
```

### Convert puml to png
```
cd puml
java -Dplantuml.include.path="." -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml-1.2022.6.jar *.puml
```


## Generate System

### Create messages
```
cd messages
protoc --python_out=../impl *.proto
```

### Monolith

```
python generate.py --rdf-model puml/youtubetranslator.ttl --architecture plain-monolith-python --output-folder impl
```

```
python generate.py --rdf-model puml/youtubetranslator.ttl --architecture pubsub-monolith-python --output-folder impl
```

### Miroservice system

```
python generate.py --rdf-model puml/youtubetranslator.ttl --architecture microservices --output-folder impl
```

### Test / Run skeletons 

Test
```
python -m impl.main
```

### Pytest skeletons 
```
pytest impl/
```

### Sicherheit nicht selbst implementieren
sops (https://github.com/mozilla/sops) , keycloak, vault (https://www.vaultproject.io/) , credstash (https://github.com/fugue/credstash)
