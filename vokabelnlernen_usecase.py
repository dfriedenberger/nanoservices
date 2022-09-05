from util.model import Model, ModelFactory , Interface
from util.rdf_util import create_graph
from util.rdf2puml import rdf2puml, rdf2pumlByRelation

from util.namespace import MBA

from util.enrichment import enrichment

# TODO: generate from graphml-File or comparable Tool

model = Model()
modelFactory = ModelFactory(model)


# Databases 
repository = modelFactory.create_service("subtitle-repository").set_pattern('repository')


# External Services
youtube_service = modelFactory.create_service("youtube.com").set_pattern('extern')
opensubtitle_service = modelFactory.create_service("opensubtitle.org").set_pattern('extern')
deepl_service = modelFactory.create_service("deepl.com").set_pattern('extern')


# Internal Service

## text.frittenburger.de

text_service = modelFactory.create_service("text-service")

text_service_input = modelFactory.create_message("text-service-input")
text_service_output = modelFactory.create_message("text-service-output")
text_service.add_interface(Interface("text-service-interface",input = text_service_input,output = text_service_output))

#UI 
## api



api_service = modelFactory.create_service("ui-api")

movie_search_request = modelFactory.create_message("movie-search-request")
movie_search_response = modelFactory.create_message("movie-search-response")
api_service.add_interface(Interface("search",input = movie_search_request,output = movie_search_response))

vocabulary_list_request = modelFactory.create_message("vocabulary-list-request")
vocabulary_list_response = modelFactory.create_message("vocabulary-list-response")
api_service.add_interface(Interface("list",input = vocabulary_list_request,output = vocabulary_list_response))

vocabulary_request = modelFactory.create_message("vocabulary-request")
vocabulary_response = modelFactory.create_message("vocabulary-response")
api_service.add_interface(Interface("export",input = vocabulary_request,output = vocabulary_response))

api_service.add_use(repository)



# Pipeline (pub-sub)

## Jobs

### Download Subtitle
download_job = modelFactory.create_service("download").set_pattern("job")
download_job.add_use(youtube_service)
download_job.add_use(opensubtitle_service)
download_job.add_use(repository)

api_service.add_trigger(download_job)


### Parsing/Annotating Subtitle
parsing_job = modelFactory.create_service("parsing").set_pattern("job")
parsing_job.add_use(text_service)
parsing_job.add_use(repository)

download_job.add_trigger(parsing_job)

### Translate Vocabulary
translate_job = modelFactory.create_service("translate").set_pattern("job")
translate_job.add_use(deepl_service)
translate_job.add_use(repository)

parsing_job.add_trigger(translate_job)

## UI (external Task for Angular Developer)
user_interface = modelFactory.create_service("user-interface").set_pattern("ui")
user_interface.add_use(api_service)


# Create Rdf-Model
graph = create_graph(model)
graph.serialize(destination="puml/vokabellernen.ttl",format='turtle')




# Create Simple Architektur

## Grouping der Elemente (austauschbare Strategy), unabhängige Module , lose Kopplung



## enrichment (impl, deployments)
enrichment(graph)



## Die Templates 'impl' generieren
## Die Deplyoments 'deployments' generieren (Readme)

#generate(graph)

# Create C4 Model
puml = rdf2puml(graph)
puml.serialize(filename="puml/vokabellernen.puml")


puml2 = rdf2pumlByRelation(graph,MBA.use)
puml2.serialize(filename="puml/vokabellernen_use.puml")
### 

