from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import FileResponse

import uvicorn

from plantuml import PlantUML

from src.modelRepository import ModelRepository
from src.textModel import TextModel
from src.updateStatus import UpdateStatus
from src.textModelId import TextModelId
from src.textModel import TextModel
from src.textModelConfig import TextModelConfig
from src.textModelUrl import TextModelUrl

from nanoservices.yaml2rdf import create_rdf_graph_from_yaml
from nanoservices.rdf2puml import rdf2pumlServices
from nanoservices.enrichment import enrichment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

modelRepository = ModelRepository()


# Interfaces

@app.get("/health")
def health():
    return {"Status": "UP"}



@app.post("/api/update-model")
async def updateModel(request: Request):
    req = await request.json()


    model_id = req['model_id']

    #Model
    status = UpdateStatus()
    status.id = model_id
    status.status = "Unknown"

    model = {
        "id" : model_id,
        "format" : "yaml",
        "model" : req['model'] 
    }
    m = modelRepository.exists_model(model_id)
    if m:
        modelRepository.update_model(model)
        status.status = "updated"
    else:
        modelRepository.create_model(model)
        status.status = "created"

    


    return status

@app.post("/api/read-model")
async def readModel(request: Request):
    req = await request.json()
    model_id = req['model_id']

    textModel = TextModel()
    m = modelRepository.exists_model(model_id)
    if m:
        model = modelRepository.read_model(model_id)
        textModel.id = model['id']
        textModel.model = model['model']
        return textModel
    
    return {}

@app.post("/api/read-puml-model")
async def readPumlModel(request: Request):
    req = await request.json()
    model_id = req['model_id']
    model_type = req['model_type']
    
    textModelUrl = TextModelUrl()
    m = modelRepository.exists_model(model_id)
    if m:
        model = modelRepository.read_model(model_id)
    
        yaml = model['model']

        # Recrate model
        try:
            graph = create_rdf_graph_from_yaml(yaml)
        except Exception as err:
            return { "error": f"create_rdf_graph_from_yaml: {err}, {type(err)}"}

        if model_type != 'cim':
            ## enrichment (impl, deployments)
            enrichment(graph)

        puml = rdf2pumlServices(graph)
        txt = '\n'.join(puml.puml)
       
        p = PlantUML(url="http://localhost:8080/png/")

        textModelUrl.url = p.get_url(txt)
        return textModelUrl
    
    return {}


@app.post("/api/implement-model")
async def implementModel(request: Request):
    req = await request.json()
    model_id = req['model_id']

    # read model

    # enrichment

    # calculate tasks

    # create Branch from 'main' and MergeRequest in git repository
    ## do tasks 
    
   
if __name__ == '__main__':
 
    uvicorn.run(app, host="0.0.0.0", port=8881)
