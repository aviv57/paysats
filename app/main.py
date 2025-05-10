import os
import logging

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

BASE_URL = os.environ.get("BASE_URL", "https://paysats.online")

g_server_db = DB(utils.apply_none_to_na(server_db_dict))

"""
Lightning address protocol for "aviv"
"""
@app.get("/.well-known/lnurlp/{username}")
async def get_lnurlp(username: str):
    return get_lightningaddress(username)

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
        return JSONResponse(content=g_server_db.query_user(user=username))
    except DB.DoesnotExists:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"error": f"{username} not found"})

@app.get("/u/{username}", response_class=HTMLResponse)
async def show_payment_options(request: Request, username: str):
    user = g_server_db.query_user(username)
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
    server = "paysats.online"
    user = q
    if utils.is_valid_email(q):
        user, server = q.split("@")
        user, server = user.lower(), server.lower()
    if server == "paysats.online":
        try:
            user_dict = g_server_db.query_user(user)
        except DB.DoesnotExists:
            return templates.TemplateResponse("404.html", {"request": request})
        return RedirectResponse(url=f"/u/{user}", status_code=302)
    return JSONResponse(status_code=400,
        content={"reason": "Only paysats.online is supported for now"}
    )