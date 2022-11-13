from nanoservices.enrichment import enrichment
from nanoservices.yaml2rdf import create_rdf_graph_from_yaml
from helper import get_instances, get_references


def create_graph_from_yaml_file(filename):
    with open(filename) as f:
        return create_rdf_graph_from_yaml(f.read())

def test_enrichment_cms():
    
    graph = create_graph_from_yaml_file("tests/data/cms.yml")

    enrichment(graph)

    assert get_instances(graph) == ["Service_cms",  "Service_db"]
    assert get_references(graph) == [("Service_cms" , "use" , "Service_db")]

def test_enrichment_repository():
    
    graph = create_graph_from_yaml_file("tests/data/repository.yml")

    enrichment(graph)

    assert get_instances(graph) == ["Service_repository",  "Service_db"]
    assert get_references(graph) == [("Service_repository" , "use" , "Service_db")]