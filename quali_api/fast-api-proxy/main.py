import json
import uvicorn as uvicorn

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dataclasses import dataclass
from quali_api import QualiAPIHandler

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@dataclass
class CloudshellConfig:
    server: str
    domain: str
    port: str


def _get_config():
    with open("config.json") as f:
        data = json.load(f)
    return CloudshellConfig(server=data["CS_SERVER"],
                            domain=data["CS_DOMAIN"],
                            port=data["QUALI_API_PORT"])


config = _get_config()
quali_api = QualiAPIHandler(host=config.server, port=config.port)


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_name = form_data.username
    password = form_data.password
    if not user_name and password:
        raise HTTPException(status_code=400,
                            detail="Must provide user and password")
    response = quali_api.login(user_name=user_name, password=password, domain=config.domain)
    if not response.ok:
        raise HTTPException(status_code=response.status_code,
                            detail=response.reason)
    token = quali_api.get_token_from_login(response)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/suites")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return quali_api.get_available_suites(token)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
