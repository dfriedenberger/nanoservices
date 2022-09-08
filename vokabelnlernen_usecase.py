from sys import implementation
from util.model import Model, ModelFactory , Interface
from util.rdf_util import create_graph
from util.rdf2puml import rdf2puml, rdf2pumlByRelation

from util.namespace import MBA

from util.enrichment import enrichment
from util.implementation import implementation


# TODO: generate from graphml-File or comparable Tool

model = Model()
modelFactory = ModelFactory(model)


# Databases 
repository = modelFactory.create_service("media-repository").set_pattern('repository')

media = modelFactory.create_message("media")
media.add("id","UUID")
media.add("title","STRING")
media.add("config","JSON")

subtitle = modelFactory.create_message("subtitle")
subtitle.add("id","UUID")
subtitle.add("media_id","UUID")
subtitle.add("language","STRING")
subtitle.add("format","STRING")
subtitle.add("data","TEXT")

repository.add_data(media)
repository.add_data(subtitle)



# External Services
youtube_service = modelFactory.create_service("youtube.com").set_pattern('extern')
opensubtitle_service = modelFactory.create_service("opensubtitle.org").set_pattern('extern')
deepl_service = modelFactory.create_service("deepl.com").set_pattern('extern')


# Internal Service

## text.frittenburger.de

text_service = modelFactory.create_service("text-service").set_pattern('intern')

text_service_input = modelFactory.create_message("text-service-input")
text_service_output = modelFactory.create_message("text-service-output")
text_service.add_interface(Interface("text-service-interface",input = text_service_input,output = text_service_output))

#UI 
## api


# vocabulary from Youtube Video, opensubtitles.org , Songtext

api_service = modelFactory.create_service("ui-api").set_pattern('api')

media_id_response = modelFactory.create_message("media-id-response")
media_id_response.add("media_id","UUID")

youtube_url_request = modelFactory.create_message("youtube-url")
youtube_url_request.add("url","STRING")

api_service.add_interface(Interface("add_youtube_url",input = youtube_url_request,output = media_id_response))

opensubtitles_id_request = modelFactory.create_message("opensubtitles-id")
opensubtitles_id_request.add("id","INT")

api_service.add_interface(Interface("add_opensubtitles_id",input = opensubtitles_id_request,output = media_id_response))


vocabulary_list_request = modelFactory.create_message("vocabulary-list-request")
vocabulary_list_request.add("id","INT")

vocabulary_list_response = modelFactory.create_message("vocabulary-list-response")
vocabulary_list_response.add("id","INT")

api_service.add_interface(Interface("list",input = vocabulary_list_request,output = vocabulary_list_response))

vocabulary_request = modelFactory.create_message("vocabulary-request")
vocabulary_request.add("id","UUID")

vocabulary_response = modelFactory.create_message("vocabulary-response")
vocabulary_response.add("id","UUID")

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

