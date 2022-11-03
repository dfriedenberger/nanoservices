import zlib
import base64

from plantuml import PlantUML

text = """
@startuml
Bob -> Alice : hello
@enduml
"""

p = PlantUML(url="http://localhost:8080/png/")

print(p.get_url(text))