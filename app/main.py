import os
import logging
import json
import requests

logger = logging.getLogger()

if not os.path.exists(".env"):
    logger.warning("No .env file found, using default values")

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from http import HTTPStatus
from fastapi.staticfiles import StaticFiles

from app.db import DB, server_db_dict
from app import nip05
from app import utils
from app.lightningaddress import get_lightningaddress

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

BASE_URL = os.environ.get("BASE_URL", "https://paysats.online").rstrip("/")
CURRENT_SERVER = BASE_URL.rsplit("://", 1)[1].split("/")[0]

class Globals:
    pass
Globals.server_db = DB(utils.apply_none_to_na(server_db_dict))
Globals.loaded_lnurlp_map = None

"""
Lightning address protocol for "aviv"
"""
@app.get("/.well-known/lnurlp/{username}")
async def get_lnurlp(username: str):
    lnurlp_map = {}
    if Globals.loaded_lnurlp_map is None:
        lnurlp_map_path = "app/lnurlp_map.json"
        if os.path.exists(lnurlp_map_path):
            with open(lnurlp_map_path, "r") as f:
                lnurlp_map = json.load(f)
            Globals.loaded_lnurlp_map = lnurlp_map
            logger.info("lnurlp_map.json loaded successfully")
        else:
            logger.warning("lnurlp_map.json not found, using empty map")
            Globals.loaded_lnurlp_map = {}

    user = Globals.server_db.query_user(user=username)
    return get_lightningaddress(username, Globals.loaded_lnurlp_map, user)

"""
NIP-05 protocol for "aviv"
"""
@app.get("/.well-known/nostr.json")
async def get_nip_05():
    # Here you can add your own logic to build the response
    return nip05.get_nip_05()


@app.get("/.well-known/paysats/{username}")
async def get_paysats(username: str):
    try:
        return JSONResponse(content=Globals.server_db.query_user(user=username))
    except DB.DoesnotExists:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"error": f"{username} not found"})

@app.get("/u/{username}", response_class=HTMLResponse)
async def show_payment_options(request: Request, username: str):
    user = Globals.server_db.query_user(username)
    if not user:
        return HTMLResponse(status_code=HTTPStatus.NOT_FOUND, content="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user, "qr_image": utils.generate_qr_base64(f"{BASE_URL}/u/{username}")})

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
     return templates.TemplateResponse("index.html", {"request": request})
 
@app.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
     return templates.TemplateResponse("faq.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    q = request.query_params.get("q")
    server = CURRENT_SERVER
    user = q
    if utils.is_valid_email(q):
        user, server = q.split("@")
        user, server = user.lower(), server.lower()
    if server == CURRENT_SERVER:
        try:
            user_dict = Globals.server_db.query_user(user)
        except DB.DoesnotExists:
            return templates.TemplateResponse("404.html", {"request": request})
        return RedirectResponse(url=f"/u/{user}", status_code=302)
    return RedirectResponse(url=f"/resolve/{user}@{server}", status_code=302)    
    
@app.get("/resolve/{address}", response_class=HTMLResponse)
async def resolve_paysats_address(request: Request, address: str):
    if not utils.is_valid_email(address):
        return JSONResponse(status_code=400, content={"error": "Invalid address"})
    user, server = address.split("@")
    user, server = user.lower(), server.lower()
    if server == CURRENT_SERVER:
        return RedirectResponse(url=f"/u/{user}", status_code=302)
    paysats_res = requests.get(f"https://{server}/.well-known/paysats/{user}")
    if paysats_res.status_code == HTTPStatus.NOT_FOUND:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"error": f"{user}@{server} not found"})
    if paysats_res.status_code != HTTPStatus.OK:
        return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={"error": f"Error fetching {user}@{server}"})
    return templates.TemplateResponse("user.html",
                                      {
                                       "request": request,
                                       "user": paysats_res.json(),
                                       "qr_image": utils.generate_qr_base64(f"{BASE_URL}/resolve/{user}@{server}"),
                                      })