from sys import implementation
from util.rdf2puml import rdf2puml, rdf2pumlByRelation

from util.namespace import MBA

from util.yaml2rdf import create_rdf_from_yaml

from util.enrichment import enrichment
from util.implementation import implementation







# Create Rdf-Model
graph = create_rdf_from_yaml("vokabelnlernen.yml")
graph.serialize(destination="puml/vokabellernen.ttl",format='turtle')

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
graph.serialize(destination="puml/vokabellernen_enriched.ttl",format='turtle')



implementation(graph,"vokabelnlernen_impl")


## Die Templates 'impl' generieren
## Die Deplyoments 'deployments' generieren (Readme)

#generate(graph)

# Create C4 Model
puml = rdf2puml(graph)
puml.serialize(filename="puml/vokabellernen.puml")


puml2 = rdf2pumlByRelation(graph,MBA.use)
puml2.serialize(filename="puml/vokabellernen_use.puml")
### 

