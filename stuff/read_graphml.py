import xml.etree.ElementTree as ET




def read_graphml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    namespace = "http://graphml.graphdrawing.org/xmlns"

    for e in root:
        
        if e.tag.endswith("graph"):
            for el in e:
                if el.tag.endswith("node"):
                    #parse node
                    id = el.attrib["id"]
                    print("node",id)
                    #is subgraph
                if el.tag.endswith("edge"):
                    print("edge",el.attrib["id"],el.attrib["source"],"->",el.attrib["target"])



read_graphml("vokabelnlernen.graphml")