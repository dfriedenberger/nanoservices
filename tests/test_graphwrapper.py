
from nanoservices.graphwrapper import create_ref
from nanoservices.namespace import MBA

def test_create_ref():

    rdf_input_msg = create_ref(MBA.Message,"test")

    assert str(rdf_input_msg) == "https://frittenburger.de/2022/05/NanoServices#Message_test"