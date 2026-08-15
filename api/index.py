from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from Crypto.Cipher import AES
import blackboxprotobuf
import json

app = FastAPI()

MAIN_KEY = b"Yg&tc%DEuh6%Zc^8"
MAIN_IV = b"6oyZDr22E3ychjM%"

def unpad(data: bytes) -> bytes:
    n = data[-1]
    if n < 1 or n > AES.block_size:
        raise ValueError("Invalid PKCS#7 padding")
    return data[:-n]

def aes_decrypt(data: bytes) -> bytes:
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    return unpad(cipher.decrypt(data))

@app.post("/MajorLogin")
@app.post("/majorlogin")
async def majorlogin(request: Request):
    body = await request.body()

    try:
        # Cek hex atau raw bytes
        try:
            ciphertext = bytes.fromhex(body.decode().strip())
        except:
            ciphertext = body

        decrypted = aes_decrypt(ciphertext)
        decoded, typedef = blackboxprotobuf.protobuf_to_json(decrypted)
        fields = json.loads(decoded)

        open_id = fields.get("22", "[NOT FOUND]")
        access_token = fields.get("29", "[NOT FOUND]")

        # Kalau mau tampilan warna, pake text biasa aja. JSON ga support warna [FF0000]
        text_response = (
            f"ACCES TOKEN: {access_token}\n"
            f"OPEN ID: {open_id}\n"
            f"STATUS: OK\n"
        )
        return Response(content=text_response, media_type="text/plain", status_code=200)

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=400)

@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
)
async def not_found(path: str):
    return HTMLResponse("<html><body><h1>404 Not Found</h1></body></html>", status_code=404)
