# nanofunctions

gen software system from nanofunction definition

## Install

### General
```
pip install rdflib
pip install pubsub
```

### Protobuf
```
apt-get install protobuf-compiler
```

### Plantuml
```
apt-get install openjdk-11-jdk
apt-get install graphviz
```
Download jar from https://plantuml.com/de/download

### Extend Nano puml

https://materialdesignicons.com/
java -jar ../plantuml.1.2020.15.jar -encodesprite 16z foo.png


## Generate rdf Models 
```
python example_signalaspectdetection.py
python example_youtubetranslator.py
```

## Generate Network Diagram
```
python create_network_diagram.py puml/youtubetranslator.ttl
```


## Generate Documentation

TODO: generate class, sequenz, deplyoment, ... diagramms


## Generate System

```
python generate.py --rdf-model tmp/youtubetranslator.ttl --architecture plain-monolith-python --output-folder impl
```
```
python generate.py --rdf-model tmp/youtubetranslator.ttl --architecture pubsub-monolith-python --output-folder impl
```

```
python generate.py --rdf-model tmp/youtubetranslator.ttl --architecture microservices --output-folder impl
```

```
Test
```
python -m impl.main
```

Pytest
```
pytest impl/
```



## Generate Miroservice system


## Convert puml to png
```
cd puml
java -Dplantuml.include.path="." -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.1.2020.15.jar *.puml
```
