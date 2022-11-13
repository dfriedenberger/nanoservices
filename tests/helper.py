def _short(o):
    return str(o).split("#")[-1]

def get_instances(graph):
        q = """
            SELECT ?s
            WHERE {
                ?s a ?t .
            }
            """
        return [_short(r['s']) for r in graph.query(q)]
       

def get_references(graph):
        q = """
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o .
                ?s a ?t1 .
                ?o a ?t2 .
            }
            """
        return [(_short(r['s']),_short(r['p']),_short(r['o'])) for r in graph.query(q)]