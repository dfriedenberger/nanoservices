from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

import uvicorn
import json
import uuid



from src.mediaRepository import MediaRepository
from src.publisher import Publisher
from src.subscriber import Subscriber
from src.youtubeUrl import YoutubeUrl
from src.mediaIdResponse import MediaIdResponse
from src.opensubtitlesId import OpensubtitlesId
from src.mediaIdResponse import MediaIdResponse
from src.vocabularyListRequest import VocabularyListRequest
from src.vocabularyListResponse import VocabularyListResponse
from src.vocabularyRequest import VocabularyRequest
from src.vocabularyResponse import VocabularyResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mediaRepository = MediaRepository()
publisher = Publisher()
subscriber = Subscriber()


# Interfaces

@app.get("/health")
def health():
    return {"Status": "UP"}



@app.post("/api/add_youtube_url")
async def add_youtube_url(request: Request):
    req = await request.json()

    media_id = str(uuid.uuid4())
    
    media = {
        'id' : media_id , 
        'title': '' ,
        'config' : {
            "source" : "youtube",
            "url" : req['url']
        }
    }

    mediaRepository.create_media(media)

    publisher.publish("/db/media/create",{ "id" : media_id })
    

    res = MediaIdResponse()
    res.media_id = media_id
    return res
    
@app.post("/api/add_opensubtitles_id")
async def add_opensubtitles_id(request: Request):
    req = await request.json()
    print(req)
    return MediaIdResponse()
    
@app.post("/api/list")
async def list(request: Request):
    req = await request.json()
    print(req)
    return VocabularyListResponse()
    
@app.post("/api/export")
async def export(request: Request):
    req = await request.json()
    print(req)
    return VocabularyResponse()
    



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8881)
