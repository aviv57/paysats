from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import asyncio

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

@app.get("/.well-known/lnurlp/{username}")
async def get_lnurlp(username: str):
    # Here you can add your own logic to build the response
    return JSONResponse(content={
        "callback": "https://livingroomofsatoshi.com/api/v1/lnurl/payreq/9427284d-4fd4-48e3-850a-3bf10c9a9748",
        "maxSendable": 100000000000,
        "minSendable": 1000,
        "metadata": "[[\"text/plain\",\"Pay to AvivB\"],[\"text/identifier\",\"tacitweight60@walletofsatoshi.com\"]]",
        "commentAllowed": 255,
        "tag": "payRequest",
        "allowsNostr": True,
        "nostrPubkey": "be1d89794bf92de5dd64c1e60f6a2c70c140abac9932418fee30c5c637fe9479"
        }
)

@app.get("/.well-known/paysats/{username}")
async def get_paysats(username: str):
    # Here you can add your own logic to build the response
    return JSONResponse(content={
        "username": username,
        "message": f"This is paysats info for {username}"
    })