from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

class MBA(DefinedNamespace):

    """
    Microservice Batch Architecture Definition Language (XSD) 
    Datatypes
    """
    URL = "https://frittenburger.de/2022/05/NanoServices"
    _NS = Namespace(URL+"/Schema#")

    # http://www.w3.org/2000/01/rdf-schema#Class

    #IPO model
    Service: URIRef
    Interface: URIRef
    Message: URIRef
    Property: URIRef


    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    name: URIRef #All Objects have names
    pattern: URIRef #Service has Pattern
    group: URIRef #Service contains to Group
    
    # relations
    output: URIRef
    input: URIRef
    data: URIRef
    use: URIRef
    has: URIRef
    trigger: URIRef
    datatype: URIRef
