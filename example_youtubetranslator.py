from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import  XSD 


from util.namespace import MBA
from util.model import Process, Message

# Create the graph
graph = Graph()


# Messages, DDD Value objects
youtube_url = Message("Youtube Link")
youtube_url.set_datatype("messages/link.proto")
youtube_url.add_to(graph)


youtube_metadata = Message("Youtube metadata")
youtube_metadata.set_datatype("messages/metadata.proto")
youtube_metadata.add_to(graph)

download_url = Message("Download Link")
download_url.set_datatype("messages/link.proto")
download_url.add_to(graph)

transcription = Message("Transcription")
transcription.set_datatype("messages/transcription.proto")
transcription.add_to(graph)

sentences_message = Message("Sentences")
sentences_message.set_datatype("messages/sentences.proto")
sentences_message.add_to(graph)

words_translated = Message("Translated Words")
words_translated.set_datatype("messages/words_translated.proto")
words_translated.add_to(graph)

words_weighted = Message("Weighted Words")
words_weighted.set_datatype("messages/words_weighted.proto")
words_weighted.add_to(graph)

# processes, DDD Services
frontend = Process("Frontend")
frontend.set_output(youtube_url)
frontend.add_to(graph)

download_metadata = Process("Download Metadata")
download_metadata.set_input(youtube_url)
download_metadata.set_output(youtube_metadata)
download_metadata.add_to(graph)

message_mapper = Process("Map Metadata")
message_mapper.set_input(youtube_metadata)
message_mapper.set_output(download_url)
message_mapper.add_to(graph)

download_transcription = Process("Download Transcription")
download_transcription.set_input(download_url)
download_transcription.set_output(transcription)
download_transcription.add_to(graph)

parsing = Process("Parse Text")
parsing.set_input(transcription)
parsing.set_output(sentences_message)
parsing.add_to(graph)

translate = Process("Translate")
translate.set_input(sentences_message)
translate.set_output(words_translated)
translate.add_to(graph)

weight_words = Process("Weight Words")
weight_words.set_input(sentences_message)
weight_words.set_output(words_weighted)
weight_words.add_to(graph)

#save
graph.serialize(destination="puml/youtubetranslator.ttl",format='turtle')
