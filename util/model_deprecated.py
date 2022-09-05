from .namespace import MBA
from rdflib import Literal, RDF, URIRef , Seq, BNode
from rdflib.namespace import  XSD 


def get_type(t):
    return t.split('#')[-1]

def get_id(name):
    return name.lower().replace(" ","_")

class Entity:

    def __init__(self,type,name):
        self.type = type
        self.name = name
        self.id = get_id(name)
        self.root =  get_type(type) +"/" + self.id
        self.rdf_object  = URIRef(MBA.URL+"#" + self.root)
        self.input = None
        self.output = None

    def set_input(self,message):
        self.input = message
    
    def set_output(self,message):
        self.output = message

    def add_to(self,graph):
        graph.add((self.rdf_object, RDF.type, self.type))
        graph.add((self.rdf_object, MBA.name, Literal(self.name, datatype=XSD.string)))
        if self.input:
            graph.add((self.input.get_rdf(), MBA.input,self.rdf_object))
        if self.output:
            graph.add((self.rdf_object, MBA.output,self.output.get_rdf()))

    def get_rdf(self):
        return self.rdf_object

class Process(Entity):
    def __init__(self,name):
        Entity.__init__(self,MBA.Process,name)

class Message(Entity):

    def __init__(self,name):
        Entity.__init__(self,MBA.Message,name)
        self.datatype = None

    def set_datatype(self,datatype):
        self.datatype = datatype #TODO read protobuf file and convert to Datatype

    def add_to(self,graph):
        Entity.add_to(self,graph)
        graph.add((self.rdf_object, MBA.datatype, Literal(self.datatype, datatype=XSD.string)))



