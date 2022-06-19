from .generator import Variable, Function

class Dependencies:

    def __init__(self):
        self.conditions = dict()

    def add(self,condition,function,output):
        if condition not in self.conditions:
            self.conditions[condition] = []
        self.conditions[condition].append((function,output))

    def lines(self):
        lines = []
        fulfilled  = [""]
        ix = 0
        while ix < len(fulfilled):
            next = fulfilled[ix]
            if next in self.conditions:
                for function, output in self.conditions[next]:
                    lines.extend(function)
                    if output not in fulfilled: #TODO notwendig?
                        fulfilled.append(output)
            ix += 1
        return lines


class PythonPlainGenerator:

    def __init__(self,modul):
        self.modul = modul
        self.imports = []
        self.dependencies = Dependencies()

    def add_class(self,variable):
        import_str = f"from {self.modul}.{variable.type.lower()} import {variable.type}"
        if import_str not in self.imports:
            self.imports.append(import_str)


    def add_function(self,function,input,output):
        
        import_str = f"from {self.modul}.{function.name} import {function.name}"
        if import_str not in self.imports:
            self.imports.append(import_str)
        
        
        lines = [""]
        if not input:
            lines.append(f"{output.name} : {output.type} = {function.name}()")
            self.dependencies.add("",lines,f"'{output.name}'")

            return

        lines.append(f"print('{input.name}',{input.name})")
        lines.append(f"{output.name}  : {output.type}  = {function.name}({input.name})")
        self.dependencies.add(f"'{input.name}'",lines,f"'{output.name}'")


    def lines(self):
        return self.imports + self.dependencies.lines()