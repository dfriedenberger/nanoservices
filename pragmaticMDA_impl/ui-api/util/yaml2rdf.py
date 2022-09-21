import yaml

from .namespace import MBA

from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import  XSD 


from .rdf_util import GraphWrapper, create_ref


def create_rdf_from_yaml(text):
        try:
            architecture_cim =  yaml.safe_load(text)

            graph = Graph()
            wrapper = GraphWrapper(graph)


            # Step one , create MessageId, Service, Interface  Ids
            #TODO Validate

            if 'messages' in architecture_cim:
                for message_name in architecture_cim['messages']:
                    message = architecture_cim['messages'][message_name]

                    rdf_msg = wrapper.add_named_instance(MBA.Message,message_name)
                    
                    if message:
                        for property_name in message:
                            property = message[property_name]
                            rdf_prop = wrapper.add_named_instance(MBA.Property,property_name,unique_name=message_name+"-"+property_name)
                            wrapper.add_str_property(MBA.datatype,rdf_prop,property)
                            wrapper.add_reference(MBA.has,rdf_msg,rdf_prop)

            if 'services' in architecture_cim:
                for service_name in architecture_cim['services']:
                    service = architecture_cim['services'][service_name]
                    rdf_service = wrapper.add_named_instance(MBA.Service,service_name)

                #Pattern
                    
                    # pattern , interfaces, data, uses

                    if 'pattern' in service:
                        pattern = service['pattern']
                        wrapper.add_str_property(MBA.pattern,rdf_service,pattern)

                    if 'interfaces' in service:
                        interfaces = service['interfaces']
                        for interface_name in interfaces:
                            interface = interfaces[interface_name]
                            rdf_interface  = wrapper.add_named_instance(MBA.Interface,interface_name)
            
                            # service use interface
                            wrapper.add_reference(MBA.has,rdf_service,rdf_interface)


                            rdf_input_msg = create_ref(MBA.Message,interface['input'])
                            wrapper.add_reference(MBA.input,rdf_interface,rdf_input_msg)

                    
                            rdf_output_msg = create_ref(MBA.Message,interface['output'])
                            wrapper.add_reference(MBA.output,rdf_interface,rdf_output_msg)


                    if 'data' in service:
                        data = service['data']
                        for datum in data:
                            rdf_data = create_ref(MBA.Message,datum)
                            wrapper.add_reference(MBA.data,rdf_service,rdf_data)
                        
                    if 'triggers' in service:
                        triggers = service['triggers']
                        for trigger_name in triggers:
                            rdf_trigger = create_ref(MBA.Service,trigger_name)
                            wrapper.add_reference(MBA.trigger,rdf_service,rdf_trigger)

                    if 'uses' in service:
                        uses = service['uses']
                        for use_name in uses:
                            rdf_use = create_ref(MBA.Service,use_name)
                            wrapper.add_reference(MBA.use,rdf_service,rdf_use)

            return graph

        except yaml.YAMLError as exc:
            print(exc)
