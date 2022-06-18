

def create_unique_id(o):
    s = str(o).split('#')[-1]
    return s.replace("/","_").replace("-","_").replace(":","_")

class PumlModel:

    def __init__(self,title):
        self.puml = []
        self.puml.append("@startuml")
        self.puml.append("!include c4/C4.puml")
        self.puml.append("!include c4/C4_Component.puml")
        self.puml.append("!include nano/nanoservices.puml")
        self.puml.append(f"title {title}")
        self.puml.append("LAYOUT_LEFT_RIGHT")

        self.cache = set()

    def create_node(self,node,name,type):
        id = create_unique_id(node)
        if id in self.cache: #already created
            return

        T = "Unknown"
        if type in ["Process","Message"]:
            T = type

        puml_obj = f'{T}({id}, "{name}","{type}")'

        self.puml.append(puml_obj)
        self.cache.add(id)

    def create_relation(self,node1,node2):
        id1 = create_unique_id(node1)
        id2 = create_unique_id(node2)
        puml_rel = f'Rel_D({id1}, {id2}," ")'
        self.puml.append(puml_rel)

    def finish(self):
        self.puml.append("@enduml")
        return self.puml

def write_puml_file(puml,filename):
    textfile = open(filename, "w")
    for element in puml:
        textfile.write(element + "\n")
    textfile.close()


