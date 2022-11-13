from nanoservices.yaml2rdf import create_rdf_graph_from_yaml
from rdflib import Graph
from helper import get_instances, get_references

def test_create_simple_model_from_yaml():
    yaml = """
services:
    # repository for data
    mysql:
        pattern: db

    # Internal Service
    wordpress:
        pattern: cms
        uses: [mysql]
    """
    graph = create_rdf_graph_from_yaml(yaml)
    assert isinstance(graph,Graph)

    assert get_instances(graph) == ["Service_mysql",  "Service_wordpress"]
    assert get_references(graph) == [("Service_wordpress" , "use" , "Service_mysql")]