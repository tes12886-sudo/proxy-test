import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import blackboxprotobuf
from fastapi import FastAPI, Request, Response

app = FastAPI()

MAIN_KEY = b"Yg&tc%DEuh6%Zc^8"
MAIN_IV = b"6oyZDr22E3ychjM%"

def aes_decrypt(data: bytes) -> bytes:
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    decrypted = cipher.decrypt(data)
    return unpad(decrypted, AES.block_size)

def make_octet_response(text: str, status_code: int = 400) -> Response:
    return Response(
        content=text.encode("utf-8"),
        status_code=status_code,
        media_type="application/octet-stream"
    )

@app.post("/MajorLogin")
@app.post("/majorlogin")
@app.post("/api/MajorLogin")
@app.post("/api/majorlogin")
async def handle_major_login(request: Request):
    body = await request.body()
    if not body:
        return make_octet_response("Request body is empty\n", status_code=400)

    try:
        # Deteksi apakah body berupa hex string atau raw bytes
        try:
            ciphertext = bytes.fromhex(body.decode("utf-8", errors="ignore").strip())
        except Exception:
            ciphertext = body

        if len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
            return make_octet_response("Invalid ciphertext length for AES-CBC\n", status_code=400)

        # Dekripsi AES-CBC
        decrypted = aes_decrypt(ciphertext)

        # Parsing Protobuf
        decoded, _ = blackboxprotobuf.protobuf_to_json(decrypted)
        
        if isinstance(decoded, str):
            fields = json.loads(decoded)
        elif isinstance(decoded, dict):
            fields = decoded
        else:
            fields = {}

        open_id_val = fields.get("22")
        access_token_val = fields.get("29")

        open_id = str(open_id_val) if open_id_val is not None else None
        access_token = str(access_token_val) if access_token_val is not None else None

        # Jika salah satu field tidak ditemukan
        if not open_id or not access_token:
            msg = (
                f"[FF0000]Open ID: [FFF000]{open_id or 'N/A'}\n"
                f"[FF0000]Access Token: [FFF000]{access_token or 'N/A'}\n"
                f"[FFFFFF]Status: [FF0000]FAILED\n"
            )
            return make_octet_response(msg, status_code=400)

        # Jika data lengkap (status code tetap 400)
        msg = (
            f"[FF0000]OPEN ID: [00FF00]{open_id}\n"
            f"[FF0000]ACCESS TOKEN: [FFF000]{access_token}\n"
            f"[FFFFFF]Status: [00FF00]OK\n"
        )
        return make_octet_response(msg, status_code=400)

    except Exception as e:
        err_msg = f"[FF0000]Error: [FFFFFF]{str(e)}\n"
        return make_octet_response(err_msg, status_code=400)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def catch_all(path: str):
    return make_octet_response("Not Found\n", status_code=400)
