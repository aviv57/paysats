from fastapi import FastAPI, Response
#from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import asyncio

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

@app.get("/.well-known/lnurlp/{username}")
async def get_lnurlp(username: str):
    if username.lower() != "aviv":
        return JSONResponse(
            status_code=404,
            content={"error": "Username not found"}
        )
    
    return JSONResponse(content={
        "callback": "https://livingroomofsatoshi.com/api/v1/lnurl/payreq/9427284d-4fd4-48e3-850a-3bf10c9a9748",
        "maxSendable": 100000000000,
        "minSendable": 1000,
        "metadata": "[[\"text/plain\",\"Pay to AvivB\"],[\"text/identifier\",\"aviv@paysats.online\"]]",
        "commentAllowed": 255,
        "tag": "payRequest",
        "allowsNostr": True,
        "nostrPubkey": "be1d89794bf92de5dd64c1e60f6a2c70c140abac9932418fee30c5c637fe9479"
        }
)

# @app.get("/.well-known/paysats/{username}")
# async def get_paysats(username: str):
#     # Here you can add your own logic to build the response
#     return JSONResponse(content={
#         "username": username,
#         "message": f"This is paysats info for {username}"
#     })

@app.get("/.well-known/nostr.json")
async def get_nip_05():
    # Here you can add your own logic to build the response
    return JSONResponse(content=
    {
        "names":
        {
            "aviv": "ddb575d7a5d2dbdaec4db767298b029e5d114d9a5ef7d0ba5103e79566c71ca8"
        }
    }
    )

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Coming Soon</title>
        <style>
            body {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #667eea, #764ba2);
                color: white;
                text-align: center;
            }
            h1 {
                font-size: 3em;
            }
            p {
                font-size: 1.5em;
                margin-top: 0.5em;
            }
        </style>
    </head>
    <body>
        <h1>🚀 Coming Soon 🚀</h1>
        <p>We're working hard to launch something amazing.<br>Stay tuned!</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

