from __future__ import annotations



class Message:

    def __init__(self,name : str):
        self.name = name
        self.properties = dict()
        self.type = "object" #default
    
    def set_type(self,type): # list , blob, string, ...
        self.type = type
        
    def add(self,name : str,type : str):
        self.properties[name] = type

class Interface:
    
    def __init__(self,name : str,input : Message,output : Message):
        self.name = name
        self.input = input
        self.output = output


class Service:

    def __init__(self,name : str):
        self.name = name
        self.patterns = list()
        self.interfaces = list()
        self.uses = list()
        self.triggers = list()
        self.data = list()

    def set_pattern(self,pattern : str) -> Service:
        self.patterns.append(pattern)
        return self


    def add_interface(self,interface : Interface):
        self.interfaces.append(interface)

    def add_use(self,service : Service):
        self.uses.append(service)

    def add_trigger(self,service : Service):
        self.triggers.append(service)

    def add_data(self,message : Message):
        self.data.append(message);

class Model:

    def __init__(self):
        self.services = list[Service]()
        self.messages = list[Message]()

class ModelFactory:

    def __init__(self,model: Model):
        self.model = model

    def create_service(self,name : str):
        service = Service(name)
        self.model.services.append(service)
        return service

    def create_message(self,name : str):
        message = Message(name)
        self.model.messages.append(message)
        return message


