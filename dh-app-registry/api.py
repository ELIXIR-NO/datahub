import os
import uvicorn
from pydantic import BaseModel, Field

from fastapi import FastAPI

PORT = int(os.getenv('PORT', '8000'))
PROXY_ROOT_PATH = os.getenv('PROXY_ROOT_PATH', '')

# Create the FastAPI application instance
app = FastAPI(
    title="Datahub - Apps Registry",
    description="A managed way of orchestrating the different apps (front ends, apis etc . . ) in ENDH ",
    version="1.0.0",
    root_path=PROXY_ROOT_PATH
)


@app.get("/")
def read_root():
    return {"message": "Welcome to ENDH app registry"}


@app.get("/front-ends")
def read_frontends():
    return [
        {"name": "ENDH App1",
         "uri": "http://localhost/app1-web",
         "dev_port": 4201,
         "view_role": "",
         "logo": "https://elixir.no//assets/logos/elixir-no-dark.svg"
         },
        {"name": "Account",
         "uri": "http://localhost:8080/realms/datahub/account",
         "dev_port": 8080,
         "view_role": "",
         "logo": "https://elixir.no//assets/logos/elixir-no-dark.svg"
         },
    ]


@app.get("/apis")
def read_apis():
    return [
        {"name": "ENDH App Registry",
         "uri": "http://localhost/dh-app-registry",
         "specification": "http://localhost/dh-app-registry/docs",
         "dev_port": 8001
         }
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
