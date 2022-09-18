import os
from sqlite3 import ProgrammingError
import string
import random
import yaml
import json

from .namespace import MBA
from .sparql_queries import SparQLWrapper
from rdflib import Graph

class NoImplementation:
    def __init__(self):
        self.implementation = "#Implementation"
   
    def add_api(self,interface_name,input_messages,output_messages):
        self.implementation += f"#call {interface_name},{input_messages} => {output_messages}\n"
    
    def code(self):
        return self.implementation

class ApisImplementation:
    
    template_api = """
@app.post("/api/{name}")
async def {name}(request: Request):
    req = await request.json()
    print(req)
    return {output}
    """
    def __init__(self):
        self.implementation = ""
   
    def add_api(self,interface_name,input_messages,output_messages):
        self.implementation += self.template_api.format(name=interface_name,input=", ".join(input_messages),output=", ".join(output_messages))
    
    def code(self):
        return self.implementation

class PojoImplementation:

    template_class = """
class {classname}:

    def __init__(self):
    """

    template_property = """
    
        self.{name} = None
    """

    def __init__(self,classname):
        self.implementation = self.template_class.format(classname=classname)

    def add_property(self,name,type):
        self.implementation += self.template_property.format(name=name)
     
    def code(self):
        return self.implementation

class RepositoryImplementation:

    template_class = """
class {repository}:

    def __init__(self):
    """

    template_init = """
        self.table_{tablename} = Table("{tablename}",{parameters},{types})
    """

    template_crud = """
    def create_{tablename}(self,obj): 
        self.table_{tablename}.create(obj)

    def read_{tablename}(self,id):
        return self.table_{tablename}.read_by_id(id)

    def update_{tablename}(self,obj):
        self.table_{tablename}.update_by_id(obj)
    
    def delete_{tablename}(self,id):
        self.table_{tablename}.delete_by_id(id)
    """

    def __init__(self,repository):
        self.implementation = self.template_class.format(repository=repository)
        self.methods = ""

    def add_table(self,tablename,parameters,types):
        self.implementation += self.template_init.format(tablename=tablename,parameters=parameters,types=types)
        self.methods += self.template_crud.format(tablename=tablename)

    def code(self):
        return self.implementation + self.methods





def get_random_string(seed : int,length : int) -> str:
    # choose from all lowercase letter
    random.seed(seed)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def sql_type(type : str):
    if type == "STRING": return "VARCHAR(100)"
    if type == "UUID": return "VARCHAR(36)"
    if type == "JSON": return "JSON"
    if type == "TEXT": return "TEXT"
    raise ValueError(f"Unknown type {type}")

def upper_camel_case(txt : str):
    p = txt.split("-")
    c = map(lambda w : w[0].upper() + w[1:],p)
    return "".join(c)

def lower_camel_case(txt : str):
    w = upper_camel_case(txt)
    return w[0].lower() + w[1:]

class Template:

    def __init__(self,path):
        with open(path,"r",encoding="UTF-8") as f:
            self.data = f.read()

    def append(self,line : str) -> None:
        self.data += f"{line}\n"

    def replace(self,pattern : str,text : str) -> None:
        #validate
        self.data.index(pattern) #Validation, throws exception
        self.data = self.data.replace(pattern,text)

class Project:

    def __init__(self,root : str,prefix : str):
        self.root = root
        self.prefix = prefix

    def create_subdirectory(self,subpath : str) -> None:
        path = os.path.join(self.root,subpath)
        if os.path.exists(path):
            print("path",path,"exists")
            return
        os.mkdir(path)
        print("path",path,"created")

    def create_file(self,subpath : str, template : Template) -> None:
        path = os.path.join(self.root,subpath)
        if os.path.exists(path):
            with open(path,"r",encoding="UTF-8") as f:
                data = f.read()
                if data == template.data:
                    print("path",path,"exists")
                    return
                with open(path+".merge","w",encoding="UTF-8") as f:
                    f.write(template.data)
                    print("path",path+".merge","created")
                print(f"there are changes in {subpath}, merge manually")
                return   
                #raise ValueError(f"there are changes in {subpath}, merge manually")
        with open(path,"w",encoding="UTF-8") as f:
            f.write(template.data)
            print("path",path,"created")

def create_python_app(service,project,project_name,template_path,program_name,implementation,query_wrapper):

    docker_copy = []
    dependencies = set()
    imports = []
    inits = [] #object initialization

    #if uses 
    docker_copy.append("COPY src/ /app/src")

    for use in query_wrapper.get_out_references(service,MBA.use):
        use_name = query_wrapper.get_single_object_property(use,MBA.name)
        use_pattern = query_wrapper.get_object_properties(use,MBA.pattern)
        use_project_name = use_name

        if "repository" in use_pattern:
            dependencies.add("mysql-connector-python==8.0.30")
            dependencies.add("PyYAML==6.0")

            #add Repository lib
            project.create_subdirectory(f"{project_name}/src")

            repository_config = Template(f"{project.root}/{use_project_name}/repository.yml")
            docker_copy.append("COPY repository.yml /app")

            project.create_file(f"{project_name}/repository.yml",repository_config)

            repository = Template(f"{project.root}/{use_project_name}/{lower_camel_case(use_name)}.py")
            project.create_file(f"{project_name}/src/{lower_camel_case(use_name)}.py",repository)

            imports.append(f"from src.{lower_camel_case(use_name)} import {upper_camel_case(use_name)}")
            inits.append(f"{lower_camel_case(use_name)} = {upper_camel_case(use_name)}()")

        if "pubsub-broker" in use_pattern:
            dependencies.add("paho-mqtt==1.6.1")
            dependencies.add("PyYAML==6.0")

            project.create_subdirectory(f"{project_name}/src")
            
            pubsub_config = Template(f"{project.root}/{use_project_name}/pubsub.yml")
            docker_copy.append("COPY pubsub.yml /app")
            project.create_file(f"{project_name}/pubsub.yml",pubsub_config)

            publisher = Template("templates/pubsub/publisher.py")
            project.create_file(f"{project_name}/src/publisher.py",publisher)

            imports.append("from src.publisher import Publisher")
            inits.append("publisher = Publisher()")

            #TODO ist not deeded by every modul e.g. jobs
            subscriber = Template("templates/pubsub/subscriber.py")
            project.create_file(f"{project_name}/src/subscriber.py",subscriber)

            imports.append("from src.subscriber import Subscriber")
            inits.append("subscriber = Subscriber()")

    for interface in query_wrapper.get_out_references(service,MBA.has):
        #TODO function with specifing type MBA.Interface
        interface_name = query_wrapper.get_single_object_property(interface,MBA.name)
        input_messages = []
        output_messages = []
        for input_message in query_wrapper.get_out_references(interface,MBA.input): 
            input_msg_name = query_wrapper.get_single_object_property(input_message,MBA.name)
            input_messages.append(lower_camel_case(input_msg_name))
            #TODO create pojo
            pojoImplementation = PojoImplementation(upper_camel_case(input_msg_name)) 
            for property in query_wrapper.get_out_references(input_message,MBA.has):
                property_name = query_wrapper.get_single_object_property(property,MBA.name)
                property_type = query_wrapper.get_single_object_property(property,MBA.datatype)
                pojoImplementation.add_property(property_name,property_type) 

            ## Create Library
            pojo_py = Template("templates/api/pojo.py")
            pojo_py.replace("#{pojo}",pojoImplementation.code())
            project.create_file(f"{project_name}/src/{lower_camel_case(input_msg_name)}.py",pojo_py)
            imports.append(f"from src.{lower_camel_case(input_msg_name)} import {upper_camel_case(input_msg_name)}")

        for output_message in query_wrapper.get_out_references(interface,MBA.output): 
            output_msg_name = query_wrapper.get_single_object_property(output_message,MBA.name)
            output_messages.append(f"{upper_camel_case(output_msg_name)}()")
            #TODO create pojo as method
            pojoImplementation = PojoImplementation(upper_camel_case(output_msg_name)) 
            for property in query_wrapper.get_out_references(output_message,MBA.has):
                property_name = query_wrapper.get_single_object_property(property,MBA.name)
                property_type = query_wrapper.get_single_object_property(property,MBA.datatype)
                pojoImplementation.add_property(property_name,property_type) 

            ## Create Library
            pojo_py = Template("templates/api/pojo.py")
            pojo_py.replace("#{pojo}",pojoImplementation.code())
            project.create_file(f"{project_name}/src/{lower_camel_case(output_msg_name)}.py",pojo_py)
            imports.append(f"from src.{lower_camel_case(output_msg_name)} import {upper_camel_case(output_msg_name)}")

        implementation.add_api(interface_name,input_messages,output_messages)

    #Implementation  python script
    program = Template(f"templates/{template_path}/{program_name}")
    program.replace("#{imports}","\n".join(imports))
    program.replace("#{init}","\n".join(inits))
    program.replace("#{implementation}",implementation.code())

    project.create_file(f"{project_name}/{program_name}",program)    
    docker_copy.append(f"COPY {program_name} /app")

    ## requirements.txt
    requirements = Template(f"templates/{template_path}/requirements.txt")
    for dependency in sorted(dependencies):
        requirements.append(dependency)
    project.create_file(f"{project_name}/requirements.txt",requirements)
    docker_copy.append("COPY requirements.txt /app")

    ## README.md
    readme = Template(f"templates/{template_path}/README.md")
    project.create_file(f"{project_name}/README.md",readme)

    # Dockerfile 
    dockerfile = Template(f"templates/{template_path}/Dockerfile")
    dockerfile.replace("#{COPY_TO_APP}","\n".join(docker_copy))
    project.create_file(f"{project_name}/Dockerfile",dockerfile)


## Example Implementation
service_cache = set()
def create_service(project: Project, service ,query_wrapper):

    # cache
    if service in service_cache: return
    service_cache.add(service)
    
    
    uses = query_wrapper.get_out_references(service,MBA.use)
    name = query_wrapper.get_single_object_property(service,MBA.name)
    pattern = query_wrapper.get_object_properties(service,MBA.pattern)

    for use in uses:
        create_service(project,use,query_wrapper)

    print("create service",name,pattern)


    project_name = name # Todo add pattern oder pattern as subdirectory 
    project.create_subdirectory(project_name)

    #create service
    if "job" in pattern:
        
        ### TODO: fork git-repository -> template "python-job"
        create_python_app(service,project,project_name,"job","main.py",NoImplementation(),query_wrapper)
        return

    if "api" in pattern: #TODO same as "job" ?
        
        ### TODO: fork git-repository -> template "rest-api"
        create_python_app(service,project,project_name,"api","server.py",ApisImplementation(),query_wrapper)
        return

    if "repository" in pattern:

        ## Config
        ## Todo encrypt passwords
        password = get_random_string(len(project_name),20)
        host = "localhost"

        ## Config from Database
        for use in uses:
            use_name = query_wrapper.get_single_object_property(use,MBA.name)
            use_pattern = query_wrapper.get_object_properties(use,MBA.pattern)
            use_project_name = use_name

            if "database" in use_pattern:
                # create config
                database_config = Template(f"{project.root}/{use_project_name}/database.yml")
                project.create_file(f"{project_name}/database.yml",database_config)

                #Todo is this needed
                root_config = yaml.safe_load(database_config.data)
                print(root_config)
                host = root_config["host"]
                

        ## README.md
        readme = Template("templates/repository/README.md")
        project.create_file(f"{project_name}/README.md",readme)


       
        config = Template("templates/repository/repository.yml")
        config.replace("{HOST}",host)
        config.replace("{USER}",project_name+"-user")
        config.replace("{PASSWORD}",password)
        config.replace("{DATABASE}",(project_name+"-database").replace("-","_"))
        project.create_file(f"{project_name}/repository.yml",config)

        ## Init Scripte
        create_database = Template("templates/repository/create_database.py")
        project.create_file(f"{project_name}/create_database.py",create_database)

        create_tables = Template("templates/repository/create_tables.py")
        project.create_file(f"{project_name}/create_tables.py",create_tables)


        repositoryImplementation = RepositoryImplementation(upper_camel_case(name)) 
        #create table and repository lib
        for message in query_wrapper.get_out_references(service,MBA.data):
            msg_name = query_wrapper.get_single_object_property(message,MBA.name)
            table = list()
            parameters = list()
            types = list()
            for property in query_wrapper.get_out_references(message,MBA.has):
                property_name = query_wrapper.get_single_object_property(property,MBA.name)
                property_type = query_wrapper.get_single_object_property(property,MBA.datatype)
                parameters.append(property_name)
                types.append(sql_type(property_type))

                table.append(f"{property_name} {sql_type(property_type)}")
                print(msg_name,property_name,property_type)


            repositoryImplementation.add_table(msg_name,parameters,types)

            #Create Table SQL
            create_table = Template("templates/repository/create_table.sql")
            create_table.replace("{NAME}",msg_name)
            create_table.replace("{DESCRIPTION}",",".join(table))
            project.create_file(f"{project_name}/create_table_{msg_name}.sql",create_table)

        ## Create Library
        repository_py = Template("templates/repository/repository.py")
        repository_py.replace("#repository",repositoryImplementation.code())
        project.create_file(f"{project_name}/{lower_camel_case(name)}.py",repository_py)

        
        ## sql scripte + lib + Config
        ## sql scripte + service (rest) + config
        ## sql scripte + service (grcp) +  lib + config
        ## rasta ?
        return
        
    if "job-controller" in pattern:
        ## fork git-repository -> template "job-controller"
        create_python_app(service,project,project_name,"job-controller","controller.py",NoImplementation(),query_wrapper)
        return

    if "job-scheduler" in pattern:
        ## fork git-repository -> template "job-scheduler"
        create_python_app(service,project,project_name,"job-scheduler","scheduler.py",NoImplementation(),query_wrapper)
        return

    if "ui" in pattern:
        ## fork git-repository -> template "static html"
        index = Template("templates/ui/index.html")

        add_forms = ""
        for use in uses:
            use_pattern = query_wrapper.get_object_properties(use,MBA.pattern)

            if "api" in use_pattern:
                for interface in query_wrapper.get_out_references(use,MBA.has):
                    #TODO function with specifing type MBA.Interface
                    interface_name = query_wrapper.get_single_object_property(interface,MBA.name)

                    #TODO only a workaround
                    config = {}
                    config["id"] = interface_name
                    config["action"] = "http://localhost:8881/api/"+interface_name #TODO copy api config
                    config["inputs"] = []
                    for input_message in query_wrapper.get_out_references(interface,MBA.input): 
                        for property in query_wrapper.get_out_references(input_message,MBA.has):
                            property_name = query_wrapper.get_single_object_property(property,MBA.name)
                            config["inputs"].append(property_name)
                    add_forms += "add_form({0});\n".format(json.dumps(config))
                 
        index.replace("/*implementation*/",add_forms)
        project.create_file(f"{project_name}/index.html",index)
        return
    

    if "database" in  pattern:

        #TODO create passwords and store encrypted and replace in files 
        # ENC[AES256_GCM,data:CwE4O1s=,iv:2k=,aad:o=,tag:w==]

        password = get_random_string(47111234,20)

        ## README.md
        readme = Template("templates/database/README.md")
        project.create_file(f"{project_name}/README.md",readme)

        ## Config
        config = Template("templates/database/database.yml")
        config.replace("{PASSWORD}",password)
        project.create_file(f"{project_name}/database.yml",config)
        #env file
        env_file = Template("templates/database/credentials.env")
        env_file.replace("{PASSWORD}",password)
        project.create_file(f"{project_name}/credentials.env",env_file)

        ## Docker compose file
        docker_compose = Template("templates/database/docker-compose.yml")
        docker_compose.replace("{CONTAINER_NAME}",f"{project.prefix}-{project_name}")
        docker_compose.replace("{MYSQL_VOLUME}",f"{project.prefix}-{project_name}-data")

        project.create_file(f"{project_name}/docker-compose.yml",docker_compose)

        return

    if "pubsub-broker" in  pattern:
        ## README.md
        readme = Template("templates/pubsub/README.md")
        project.create_file(f"{project_name}/README.md",readme)

        ## Config
        config = Template("templates/pubsub/pubsub.yml")
        project.create_file(f"{project_name}/pubsub.yml",config)
        
        ## Docker compose file
        docker_compose = Template("templates/pubsub/docker-compose.yml")
        docker_compose.replace("{CONTAINER_NAME}",f"{project.prefix}-{project_name}")
        project.create_file(f"{project_name}/docker-compose.yml",docker_compose)
        return

    if "extern" in  pattern:
        ## Schnittstellenvereinbarung / Beschreibung
        return

    if "intern" in  pattern:
        ## Docker-compose
        return


    print("cannot handle pattern",pattern,"=>",name)
    #'pubsub' => Lib + Config






def implementation(graph : Graph,path : str):
    
    query_wrapper = SparQLWrapper(graph)


    project = Project(path,"frittenburger")
    # Create Config
        
    # Add Implementations or ImplementationTask  to Services
    for service in query_wrapper.get_instances_of_type(MBA.Service):
       create_service(project,service,query_wrapper)

    # Add Hardware

    # Add Deployment