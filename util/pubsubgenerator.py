from .generator import Variable, Function



class PythonPubSubGenerator:

    def __init__(self):
        self.imports = ['from pubsub import pub']
        self.functions = []
        self.listeners = ["","# Register listeners"]
        self.main = ["","# Register listeners"]

    def add_class(self,variable):
        import_str = f"from .{variable.path} import {variable.type}"
        if import_str not in self.imports:
            self.imports.append(import_str)


    def add_function(self,function,input,output):
        
        import_str = f"from .{function.name} import {function.name}"
        if import_str not in self.imports:
            self.imports.append(import_str)

        if not input:
            self.main.append("")
            self.main.append(f"{output.name} = {function.name}()")
            self.main.append(f"pub.sendMessage('{output.name}', arg={output.name})")
            return

        self.functions.append("")
        self.functions.append(f"def listener_{function.name}(arg : {input.type}) -> {output.type}:")
        self.functions.append(f"    print('receive',arg)")
        self.functions.append(f"    {output.name} = {function.name}(arg)")
        self.functions.append(f"    pub.sendMessage('{output.name}', arg={output.name})")
        

        self.listeners.append(f"pub.subscribe(listener_{function.name}, '{input.name}')")

    def lines(self):
        return self.imports + self.functions + self.listeners + self.main