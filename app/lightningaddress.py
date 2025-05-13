from fastapi.responses import JSONResponse
from http import HTTPStatus

def get_lightningaddress(username: str, lnurlp_map: dict) -> JSONResponse:
    if username in lnurlp_map:
        return JSONResponse(content=lnurlp_map[username])

    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={
            "error": f"Lightning address for {username} not found",
            "message": "Please check the username or contact support.",
        },
    )