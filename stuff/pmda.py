import argparse
from pathlib import Path

from util.rdf2puml import rdf2puml, rdf2pumlByRelation
from util.namespace import MBA
from util.yaml2rdf import create_rdf_from_yaml

from util.enrichment import enrichment
from util.implementation import implementation


# main
parser = argparse.ArgumentParser(description='Create Network from rdf model.')
parser.add_argument('--model', required=True,help='yaml model file')

args = parser.parse_args()


filename = args.model

model_key = Path(filename).stem



# Create Rdf-Model
graph = create_rdf_from_yaml(filename)
graph.serialize(destination=f"puml/{model_key}.ttl",format='turtle')

#TODO Validate rdf_graph



# Create Simple Architektur

## Grouping der Elemente (austauschbare Strategy), unabhängige Module , lose Kopplung



## TODO: Fragebogen/Config Architektur Entscheidungen
## Save as Architecture Decision Records 
## VPC vs Internet
## Synchronous and asynchronous point-to-point communication
## Anonymous publish/subscribe

## enrichment (impl, deployments)
enrichment(graph)
graph.serialize(destination=f"puml/{model_key}_enriched.ttl",format='turtle')



implementation(graph,f"{model_key}_impl",model_key)


## Die Templates 'impl' generieren
## Die Deplyoments 'deployments' generieren (Readme)

#generate(graph)

# Create C4 Model
puml = rdf2puml(graph)
puml.serialize(filename=f"puml/{model_key}.puml")


puml2 = rdf2pumlByRelation(graph,MBA.use)
puml2.serialize(filename=f"puml/{model_key}_use.puml")
### 

