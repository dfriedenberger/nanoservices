from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import  XSD 


from util.namespace import MBA
from util.model_deprecated import Process, Message

# Create the graph
graph = Graph()


# Messages, DDD Value objects
image_msg = Message("Image")
image_msg.set_datatype("messages/image.proto")
image_msg.add_to(graph)

clipped_msg = Message("Clipped Image")
clipped_msg.set_datatype("messages/clipped.proto")
clipped_msg.add_to(graph)

ellipses_msg = Message("Ellipses")
ellipses_msg.set_datatype("messages/ellipses.proto")
ellipses_msg.add_to(graph)

color_msg = Message("Color")
color_msg.set_datatype("messages/color.proto")
color_msg.add_to(graph)

radius_msg = Message("Radius")
radius_msg.set_datatype("messages/radius.proto")
radius_msg.add_to(graph)

position_msg = Message("Position")
position_msg.set_datatype("messages/position.proto")
position_msg.add_to(graph)

# processes, DDD Services
detect_signal = Process("Detect Signal")
detect_signal.set_input(image_msg)
detect_signal.set_output(clipped_msg)
detect_signal.add_to(graph)


detect_ellipses = Process("Detect Ellipses")
detect_ellipses.set_input(clipped_msg)
detect_ellipses.set_output(ellipses_msg)
detect_ellipses.add_to(graph)

#Feature functions
feature_color = Process("Detect Color")
feature_color.set_input(ellipses_msg)
feature_color.set_output(color_msg)
feature_color.add_to(graph)

feature_radius = Process("Detect Radius")
feature_radius.set_input(ellipses_msg)
feature_radius.set_output(radius_msg)
feature_radius.add_to(graph)

feature_position = Process("Detect Position")
feature_position.set_input(ellipses_msg)
feature_position.set_output(position_msg)
feature_position.add_to(graph)

#save
graph.serialize(destination="puml/signalaspectdetection.ttl",format='turtle')
