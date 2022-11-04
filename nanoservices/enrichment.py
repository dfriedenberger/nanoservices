from .graphwrapper import GraphWrapper
from .namespace import MBA
from .sparql_queries import SparQLWrapper

from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import  XSD 

# Add job-controller, job-scheduler's
# Add mqtt, Add db, Add keycloak
# module -> Impl
# Add Deployments
# Add Config
# Aspekte wie logging, tracing events, ... hinzufügen

def enrichment(graph : Graph) -> None:

    query_wrapper = SparQLWrapper(graph)
    create_wrapper = GraphWrapper(graph)

    repositories = []
    jobs = []

    triggers_send = []
    triggers_recv = []

    
    for service in query_wrapper.get_instances_of_type(MBA.Service):
        for pattern in query_wrapper.get_object_properties(service,MBA.pattern):
            if pattern == "repository":
                repositories.append(service)
            if pattern == "job":
                jobs.append(service) 
        
        for triggered_service in query_wrapper.get_out_references(service,MBA.trigger):
            triggers_send.append(service)
            triggers_recv.append(triggered_service)
    
    # strategy handle job patterns -> change of structure (jobs did not recv triggers)
    ## Alternative waere aws Batch Jobs
    if len(jobs) > 0:
        # add job-repository
        rdf_job_repository = create_wrapper.add_named_instance(MBA.Service,"job-repository")
        create_wrapper.add_str_property(MBA.pattern,rdf_job_repository,"repository")
        repositories.append(rdf_job_repository)

        #Add Queue
        rdf_msg = create_wrapper.add_named_instance(MBA.Message,"job")
        properties = { "id" : "UUID" ,  "job" : "JSON" , "state" : "STRING"}
        for k in properties:
            rdf_prop = create_wrapper.add_named_instance(MBA.Property,k,unique_name="job-"+k)
            create_wrapper.add_str_property(MBA.datatype,rdf_prop,properties[k])
            create_wrapper.add_reference(MBA.has,rdf_msg,rdf_prop)
        create_wrapper.add_reference(MBA.data,rdf_job_repository,rdf_msg)

        # add job-controller
        rdf_job_controller = create_wrapper.add_named_instance(MBA.Service,"job-controller")
        create_wrapper.add_str_property(MBA.pattern,rdf_job_controller,"job-controller")
        create_wrapper.add_reference(MBA.use,rdf_job_controller,rdf_job_repository)

        # add job-scheduler's
        rdf_job_scheduler = create_wrapper.add_named_instance(MBA.Service,"job-scheduler")
        create_wrapper.add_str_property(MBA.pattern,rdf_job_scheduler,"job-scheduler")
        create_wrapper.add_reference(MBA.use,rdf_job_scheduler,rdf_job_repository)

        for job in jobs:
            # add use
            create_wrapper.add_reference(MBA.use,rdf_job_scheduler,job)
            # delete jobs from triggers_recv
            if job in triggers_recv:
                triggers_recv.remove(job)

        triggers_recv.append(rdf_job_controller)
       

        #grouping
        create_wrapper.add_str_property(MBA.group,rdf_job_repository,'system.job.management')
        create_wrapper.add_str_property(MBA.group,rdf_job_controller,'system.job.management')
        create_wrapper.add_str_property(MBA.group,rdf_job_scheduler,'system.job.management')
        for job in jobs:
            create_wrapper.add_str_property(MBA.group,job,'system.job')


    # strategy handle repository patterns
    if len(repositories) > 0:
        # add database
        rdf_db = create_wrapper.add_named_instance(MBA.Service,"db")
        create_wrapper.add_str_property(MBA.pattern,rdf_db,"database")

        for rdf_repository in repositories:
            create_wrapper.add_reference(MBA.use,rdf_repository,rdf_db)

        #grouping
        create_wrapper.add_str_property(MBA.group,rdf_db,'system.infrastructure')

    # strategy handle pub-sub communication
    ## yes for tracing, Global parameter
    if len(triggers_recv) > 0 or len(triggers_send) > 0:
        rdf_mqtt = create_wrapper.add_named_instance(MBA.Service,"mqtt")
        create_wrapper.add_str_property(MBA.pattern,rdf_mqtt,"pubsub-broker")

        for t in triggers_send:
            create_wrapper.add_reference(MBA.use,t,rdf_mqtt)
        for t in triggers_recv:
            create_wrapper.add_reference(MBA.use,t,rdf_mqtt)

        #Todo create Topics


        create_wrapper.add_str_property(MBA.group,rdf_mqtt,'system.infrastructure')

    #VPC or distributed over Internet

    