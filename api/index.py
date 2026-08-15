import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
import blackboxprotobuf

# Inisialisasi 'app' yang dicari oleh Vercel
app = FastAPI()

MAIN_KEY = b"Yg&tc%DEuh6%Zc^8"
MAIN_IV = b"6oyZDr22E3ychjM%"

def aes_decrypt(data: bytes) -> bytes:
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    decrypted = cipher.decrypt(data)
    return unpad(decrypted, AES.block_size)

@app.post("/MajorLogin")
@app.post("/majorlogin")
@app.post("/api/MajorLogin")
@app.post("/api/majorlogin")
async def handle_major_login(request: Request):
    body = await request.body()
    if not body:
        return PlainTextResponse("Request body is empty\n", status_code=400)

    try:
        # Cek apakah body berupa hex string atau raw bytes
        try:
            ciphertext = bytes.fromhex(body.decode("utf-8").strip())
        except Exception:
            ciphertext = body

        # Validasi panjang ciphertext (harus kelipatan 16 byte untuk AES)
        if len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
            return PlainTextResponse("Invalid ciphertext length for AES-CBC\n", status_code=400)

        decrypted = aes_decrypt(ciphertext)
        decoded, _ = blackboxprotobuf.protobuf_to_json(decrypted)
        fields = json.loads(decoded)

        open_id = fields.get("22")
        access_token = fields.get("29")

        # Cek open_id
        if not open_id:
            return PlainTextResponse("[FF0000]Open ID tidak ditemukan!\n", status_code=400)

        # Cek access_token
        if not access_token:
            msg = (
                f"[FF0000]Open ID: [FFF000]{open_id}\n"
                f"[FF0000]Access Token tidak ditemukan!\n"
                f"[FFFFFF]Status: [FF0000]FAILED\n"
            )
            return PlainTextResponse(msg, status_code=400)

        # Response sukses
        msg = (
            f"[FF0000]OPEN ID: [00FF00]{open_id}\n"
            f"[FF0000]ACCESS TOKEN: [FFF000]{access_token}\n"
            f"[FFFFFF]Status: [00FF00]OK\n"
        )
        return PlainTextResponse(msg, status_code=200)

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=400)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def catch_all(path: str):
    return PlainTextResponse("Not Found", status_code=404)
