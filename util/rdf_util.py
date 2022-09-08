from .model import Service, Model
from .namespace import MBA

from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import  XSD 

def type_str(type : URIRef) -> str:
    s = str(type)
    return s.split("#")[1]

def create_ref(type : URIRef,name : str) -> URIRef:
    id = type_str(type) + "_"+name.replace("-","_")
    return URIRef(MBA.URL+"#"+id)

class GraphWrapper:

    def __init__(self,graph : Graph):
        self.graph = graph

    def add_named_instance(self,type : URIRef,name : str,unique_name : str = None) -> URIRef:
        if unique_name == None: unique_name = name
        rdf_object  = create_ref(type,unique_name)
        self.graph.add((rdf_object, RDF.type, type))
        self.graph.add((rdf_object, MBA.name, Literal(name, datatype=XSD.string)))
        return rdf_object
    
    def add_reference(self,type : URIRef,source : URIRef,target : URIRef) -> None:
        self.graph.add((source, type, target))

    def add_str_property(self,type : URIRef,source : URIRef,value : str) -> None:
        self.graph.add((source, type, Literal(value, datatype=XSD.string)))

def create_graph(model: Model) -> Graph:

    graph = Graph()
    wrapper = GraphWrapper(graph)


    for message in model.messages:
        #Add Message
        rdf_msg = wrapper.add_named_instance(MBA.Message,message.name)
        for k in message.properties:
            rdf_prop = wrapper.add_named_instance(MBA.Property,k,unique_name=message.name+"-"+k)
            wrapper.add_str_property(MBA.datatype,rdf_prop,message.properties[k])
            wrapper.add_reference(MBA.has,rdf_msg,rdf_prop)
        
    for service in model.services:
        #Add service
        rdf_object = wrapper.add_named_instance(MBA.Service,service.name)

        #Pattern
        for pattern in service.patterns:
            wrapper.add_str_property(MBA.pattern,rdf_object,pattern)
    
        for datum in service.data:
            rdf_data = create_ref(MBA.Message,datum.name)
            wrapper.add_reference(MBA.data,rdf_object,rdf_data)

        for interface in service.interfaces:
            rdf_interface  = wrapper.add_named_instance(MBA.Interface,interface.name)
            
            # service use interface
            wrapper.add_reference(MBA.has,rdf_object,rdf_interface)


            rdf_input_msg = create_ref(MBA.Message,interface.input.name)
            wrapper.add_reference(MBA.input,rdf_interface,rdf_input_msg)

        
            rdf_output_msg = create_ref(MBA.Message,interface.output.name)
            wrapper.add_reference(MBA.output,rdf_interface,rdf_output_msg)
          

        for use in service.uses:
            rdf_service = create_ref(MBA.Service,use.name)
            wrapper.add_reference(MBA.use,rdf_object,rdf_service)

        for trigger in service.triggers:
            rdf_service = create_ref(MBA.Service,trigger.name)
            wrapper.add_reference(MBA.trigger,rdf_object,rdf_service)

    return graph

