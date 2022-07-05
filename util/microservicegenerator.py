from .generator import Variable, Function


class PythonMicroserviceGenerator:

    def __init__(self):
        self.imports = ['']

    def add_class(self,variable):
        import_str = f"from .{variable.path} import {variable.type}"
        if import_str not in self.imports:
            self.imports.append(import_str)


    def add_function(self,function,input,output):
        
        import_str = f"from .{function.name} import {function.name}"
        if import_str not in self.imports:
            self.imports.append(import_str)

        #TODO generate orchestration which calls the microservices

    def lines(self):
        return self.imports + self.main