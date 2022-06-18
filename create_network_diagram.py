import os
import argparse
from rdflib import Graph

from util.namespace import MBA
from util.puml_utils import PumlModel, write_puml_file
from util.sparql_queries import SparQLWrapper

# main
parser = argparse.ArgumentParser(description='Create Network from rdf model.')
parser.add_argument('file', type=argparse.FileType('r'),nargs='+',help='rdf model file')
args = parser.parse_args()


for file in args.file:

    graph = Graph()
    graph.parse(file)

    wrapper = SparQLWrapper(graph)

    model = PumlModel("IPO Model")
    for (s,o) in wrapper.get_references():

        model.create_node(s, wrapper.get_single_object_property(s,MBA.name), wrapper.get_type(s).split('#')[-1])
        model.create_node(o, wrapper.get_single_object_property(o,MBA.name), wrapper.get_type(o).split('#')[-1])
        model.create_relation(s,o)

    filename = f"{os.path.splitext(file.name)[0]}.puml"
    write_puml_file(model.finish(),filename)
    print("Created",filename)



 