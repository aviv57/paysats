from fastapi.responses import JSONResponse, RedirectResponse
from http import HTTPStatus

def get_lightningaddress(username: str, lnurlp_map: dict, user: dict) -> JSONResponse:
    if username in lnurlp_map:
        return JSONResponse(content=lnurlp_map[username])
    
    address = user.get("bitcoin", {}).get("lightning_address", "")
    if address != "":
        try:
            remote_domain = address.split("@")[1]
            redirect_url = f"https://{remote_domain}/.well-known/lnurlp/{username}"
            return RedirectResponse(url=redirect_url, status_code=HTTPStatus.TEMPORARY_REDIRECT)
        except IndexError:
            pass  # Malformed address, fall through to erro    

    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={
            "error": f"Lightning address for {username} not found",
            "message": "Please check the username or contact support.",
        },
    )