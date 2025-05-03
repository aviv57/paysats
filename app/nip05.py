from fastapi.responses import JSONResponse

def get_nip_05():
    # Here you can add your own logic to build the response
    return JSONResponse(
        content={
            "names": {
                "aviv": "ddb575d7a5d2dbdaec4db767298b029e5d114d9a5ef7d0ba5103e79566c71ca8"
            }
        }
    )
