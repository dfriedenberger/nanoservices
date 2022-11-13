from .namespace import MBA
from .sparql_queries import SparQLWrapper
from rdflib import Graph, Literal, RDF, URIRef


class Task:

    def __init__(self,name,pattern):
        self.pattern = pattern
        self.name = name
        self.assets = []

    def create_asset(self,asset):
        self.assets.append(asset)

class Project:

    def __init__(self):
        self.tasks = []

    def create_task(self,name,pattern):
        task = Task(name,pattern)
        self.tasks.append(task)
        return task

pattern_implementation = {
    "database" : ["README.md" , "database.yml.template" , "credentials.env.template" , "docker-compose.yml" ],
    "cms" : ["README.md" , "database.yml.template" , "credentials.env.template" , "docker-compose.yml" ],
}

def create_service( project  , service ,query_wrapper,service_cache):

    # cache
    if service in service_cache: return
    service_cache.add(service)

    
    uses = query_wrapper.get_out_references(service,MBA.use)
    name = query_wrapper.get_single_object_property(service,MBA.name)
    pattern = query_wrapper.get_object_properties(service,MBA.pattern)

    for use in uses:
        create_service(project,use,query_wrapper,service_cache)

    print("create Task",name,pattern)
    task = project.create_task(name,pattern)

    for p in pattern:

        if p not in pattern_implementation:
            print(f"No Implementation for {p}")
            continue
        for asset in pattern_implementation[p]:
            task.create_asset(asset)
      



    
def implementation(graph : Graph):
    
    query_wrapper = SparQLWrapper(graph)


    project = Project()
    # Create Config
        
    # Add Implementations or ImplementationTask  to Services
    service_cache = set()
    for service in query_wrapper.get_instances_of_type(MBA.Service):
       create_service(project,service,query_wrapper,service_cache)

    # Add Hardware

    # Add Deployment

    return project