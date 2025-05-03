from fastapi.responses import JSONResponse
from http import HTTPStatus

def get_lightningaddress(username: str):
    if username.lower() != "aviv":
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"error": "Username not found"})

    return JSONResponse(
        content={
            "callback": "https://livingroomofsatoshi.com/api/v1/lnurl/payreq/9427284d-4fd4-48e3-850a-3bf10c9a9748",
            "maxSendable": 100000000000,
            "minSendable": 1000,
            "metadata": '[["text/plain","Pay to AvivB"],["text/identifier","aviv@paysats.online"]]',
            "commentAllowed": 255,
            "tag": "payRequest",
            "allowsNostr": True,
            "nostrPubkey": "ddb575d7a5d2dbdaec4db767298b029e5d114d9a5ef7d0ba5103e79566c71ca8",
        }
    )