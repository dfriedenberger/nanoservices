from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

import uvicorn
import json



#{imports}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#{init}


# Interfaces

@app.get("/health")
def health():
    return {"Status": "UP"}


#{implementation}



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8881)
