from __future__ import annotations



class Message:

    def __init__(self,name : str):
        self.name = name
    
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

    def set_pattern(self,pattern : str) -> Service:
        self.patterns.append(pattern)
        return self


    def add_interface(self,interface : Interface):
        self.interfaces.append(interface)

    def add_use(self,service : Service):
        self.uses.append(service)

    def add_trigger(self,service : Service):
        self.triggers.append(service)

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


