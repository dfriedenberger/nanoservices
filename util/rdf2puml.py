from rdflib import URIRef, Graph

from .puml_utils import PumlModel
from .sparql_queries import SparQLWrapper
from .namespace import MBA


def add_node(puml,wrapper,instance):
    type = wrapper.get_type(instance).split("#")[1]
    name = wrapper.get_single_object_property(instance,MBA.name)

    # Todo Redesign Group
    group = ["system"] # default

    groups = wrapper.get_object_properties(instance,MBA.group)
    if len(groups) > 0:
        group = groups[0].split(".")
    
    #Workaround (extern)
    patterns = wrapper.get_object_properties(instance,MBA.pattern)
    if "extern" in patterns: group = []



    puml.create_node(instance,name,type,group)

def rdf2puml(graph : Graph) -> PumlModel:

    puml = PumlModel("Architecture")
    wrapper = SparQLWrapper(graph)

    for instance in wrapper.get_instances():
        add_node(puml,wrapper,instance)

    for (n1,n2) in wrapper.get_references():
        puml.create_relation(n1,n2)

    puml.finish()
    return puml 




def rdf2pumlByRelation(graph : Graph,relation_type : URIRef) -> PumlModel:

    puml = PumlModel("Architecture")
    wrapper = SparQLWrapper(graph)

    for (n1,n2) in wrapper.get_references_by_type(relation_type):
        add_node(puml,wrapper,n1)
        add_node(puml,wrapper,n2)
        puml.create_relation(n1,n2)


    puml.finish()
    return puml 
