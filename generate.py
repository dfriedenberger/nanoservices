import os
import argparse
from rdflib import Graph

from util.namespace import MBA
from util.puml_utils import PumlModel, write_puml_file
from util.sparql_queries import SparQLWrapper

from util.generator import Function, Variable
from util.templategenerator import PythonTemplateGenerator

from util.pubsubgenerator import PythonPubSubGenerator
from util.plaingenerator import PythonPlainGenerator

def get_name(name):
    return name.lower().replace(" ","_")

def get_type(name):
    return name.split("/")[-1].split(".")[0].capitalize()


# main
parser = argparse.ArgumentParser(description='Create Network from rdf model.')
parser.add_argument('--rdf-model', type=argparse.FileType('r'),required=True,help='rdf model file')
parser.add_argument('--output-folder',required=True,help="Project output folder")
parser.add_argument('--architecture',required=True,help="Architecture(pubsub-monolith-python, plain-monolith-python, microservice")

args = parser.parse_args()

graph = Graph()
graph.parse(args.rdf_model)
wrapper = SparQLWrapper(graph)



#python ?
template = PythonTemplateGenerator(args.output_folder)
 
 
if args.architecture == "pubsub-monolith-python":
    generator = PythonPubSubGenerator(modul = args.output_folder)
elif args.architecture == "plain-monolith-python":
    generator = PythonPlainGenerator(modul = args.output_folder)
else:
    raise ValueError(f"Architecture {args.architecture} is not supported.")




# generate classes 
variables = dict()
for message in wrapper.get_instances(MBA.Message):
    proto = wrapper.get_single_object_property(message,MBA.datatype)
    variables[message] = Variable(get_name(wrapper.get_single_object_property(message,MBA.name)),get_type(proto))
    generator.add_class(variables[message])
    template.create_class(variables[message])


# generate functions
for process in wrapper.get_instances(MBA.Process):
    inputs = wrapper.get_in_references(process,MBA.input)
    outputs = wrapper.get_out_references(process,MBA.output)
    
    input = None 
    if len(inputs) == 1:
        input = variables[inputs[0]]

    output = variables[outputs[0]]

    function = Function(get_name(wrapper.get_single_object_property(process,MBA.name)))

    generator.add_function(function,input,output)
    template.create_function(function,input,output)

    # generate tests 
    template.create_unittest(function,input,output)

# generate integration test / simulation / ...




template.create_file(generator.lines(),"main.py")




 