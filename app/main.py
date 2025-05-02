from fastapi import FastAPI, Request

# from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from http import HTTPStatus
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

class DB:
    class DoesnotExists(Exception):
        pass

    def __init__(self, data):
        self.__db_data = data

    def query_user(self, user):
        u = self.__db_data.get("users", {}).get(user)
        if u is None:
            raise self.DoesnotExists()
        return u

server_db_dict = {
    "users":{}
}

def none_to_na(obj):
    return "N/A" if obj is None else obj

def apply_none_to_na(data):
    if isinstance(data, dict):
        return {k: apply_none_to_na(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [apply_none_to_na(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(apply_none_to_na(item) for item in data)
    else:
        return none_to_na(data)

# Add record to DB
server_db_dict["users"]["aviv"] = {
        "contact": {
            "nickname":"aviv",
            "x": "@Aviv__BarEl",
            "email": "aviv@paysats.online",
            "nostr": "npub1mk6ht4a96tda4mzdkanjnzcznew3znv6tmmapwj3q0ne2ek8rj5q8vpf5q",
        },
        "bitcoin": {
            "address": "bc1qft4764g468c09rzv6huzjnzcfelzrva9mcjk75",
            "xpub": None,
            "lightning_address": "aviv@paysats.online",
            "silent_payments": None,
        },
    }

g_server_db = DB(apply_none_to_na(server_db_dict))


@app.get("/.well-known/lnurlp/{username}")
async def get_lnurlp(username: str):
    if username.lower() != "aviv":
        return JSONResponse(status_code=404, content={"error": "Username not found"})

    return JSONResponse(
        content={
            "callback": "https://livingroomofsatoshi.com/api/v1/lnurl/payreq/9427284d-4fd4-48e3-850a-3bf10c9a9748",
            "maxSendable": 100000000000,
            "minSendable": 1000,
            "metadata": '[["text/plain","Pay to AvivB"],["text/identifier","aviv@paysats.online"]]',
            "commentAllowed": 255,
            "tag": "payRequest",
            "allowsNostr": True,
            "nostrPubkey": "be1d89794bf92de5dd64c1e60f6a2c70c140abac9932418fee30c5c637fe9479",
        }
    )


@app.get("/.well-known/paysats/{username}")
async def get_paysats(username: str):
    try:
        return JSONResponse(content=g_server_db.query_user(user=username))
    except DB.DoesnotExists:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"error": f"{username} not found"})
    
@app.get("/u/{username}", response_class=HTMLResponse)
async def show_payment_options(request: Request, username: str):
    user = g_server_db.query_user(username)
    if not user:
        return HTMLResponse(status_code=HTTPStatus.NOT_FOUND, content="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})    


@app.get("/.well-known/nostr.json")
async def get_nip_05():
    # Here you can add your own logic to build the response
    return JSONResponse(
        content={
            "names": {
                "aviv": "ddb575d7a5d2dbdaec4db767298b029e5d114d9a5ef7d0ba5103e79566c71ca8"
            }
        }
    )

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
     return templates.TemplateResponse("index.html", {"request": request, "title": "paysats.online (Coming soon)"})