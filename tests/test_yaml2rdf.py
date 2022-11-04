from nanoservices.yaml2rdf import create_rdf_graph_from_yaml
from rdflib import Graph


def short(o):
    return str(o).split("#")[-1]

def get_instances(graph):
        q = """
            SELECT ?s
            WHERE {
                ?s a ?t .
            }
            """
        return [short(r['s']) for r in graph.query(q)]
       

def get_references(graph):
        q = """
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o .
                ?s a ?t1 .
                ?o a ?t2 .
            }
            """
        return [(short(r['s']),short(r['p']),short(r['o'])) for r in graph.query(q)]

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