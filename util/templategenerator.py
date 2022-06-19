from .generator import Variable, Function


class PythonTemplateGenerator:

    def __init__(self,path):
        self.path = path

    def create_class(self,variable : Variable):
        filename = f"{self.path}/{variable.path}.py"
        with open(filename,"w") as f:

            #we are using protobuf
            #f.write(f"class {variable.type}:\n")
            #f.write("    pass\n")
            f.write(f"from .{variable.path}_pb2 import {variable.type}\n")

    def create_function(self,function : Function, input : Variable, output : Variable):
        filename = f"{self.path}/{function.name}.py"
        with open(filename,"w") as f:
            if input:
                f.write(f"from .{input.path} import {input.type}\n")
            f.write(f"from .{output.path} import {output.type}\n")
            if input:
                f.write(f"def {function.name}({input.name} : {input.type}) ->  {output.type}:\n")
            else:
                f.write(f"def {function.name}() ->  {output.type}:\n")
            f.write(f"    {output.name} = {output.type}()\n")
            f.write(f"    return {output.name}\n")

    def create_unittest(self,function : Function, input : Variable, output : Variable):
        filename = f"{self.path}/test_{function.name}.py"
        with open(filename,"w") as f:

            f.write(f"def test():\n")
            if input:
                f.write(f"    from .{input.path} import {input.type}\n")
            f.write(f"    from .{output.path} import {output.type}\n")
            f.write(f"    from .{function.name} import {function.name}\n")

            if input:
                f.write(f"    {input.name} = {input.type}()\n")
                f.write(f"    {output.name} :  {output.type} = {function.name}({input.name})\n")
            else:
                f.write(f"    {output.name} :  {output.type} = {function.name}()\n")
            f.write(f"    assert {output.name} != None\n")


    def create_file(self,lines : list,filename):
        with open(f"{self.path}/{filename}","w") as f:
            for line in lines:
                f.write(f"{line}\n")


