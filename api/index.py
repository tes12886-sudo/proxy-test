import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import blackboxprotobuf
from mitmproxy import http

MAIN_KEY = b"Yg&tc%DEuh6%Zc^8"
MAIN_IV = b"6oyZDr22E3ychjM%"

def aes_decrypt(data: bytes) -> bytes:
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    decrypted = cipher.decrypt(data)
    return unpad(decrypted, AES.block_size)

class LoginInterceptor:
    def request(self, flow: http.HTTPFlow) -> None:
        # Cek apakah endpoint cocok
        path = flow.request.path.lower()
        if not path.startswith("/majorlogin"):
            return

        body = flow.request.content
        if not body:
            flow.response = http.Response.make(
                400,
                b"Request body is empty\n",
                {"Content-Type": "text/plain"}
            )
            return

        try:
            # Cek apakah body berupa hex string atau raw bytes
            try:
                ciphertext = bytes.fromhex(body.decode("utf-8").strip())
            except Exception:
                ciphertext = body

            # Validasi panjang blok AES (harus kelipatan 16 byte)
            if len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
                flow.response = http.Response.make(
                    400,
                    b"Invalid ciphertext length for AES-CBC\n",
                    {"Content-Type": "text/plain"}
                )
                return

            decrypted = aes_decrypt(ciphertext)
            decoded, _ = blackboxprotobuf.protobuf_to_json(decrypted)
            fields = json.loads(decoded)

            open_id = fields.get("22")
            access_token = fields.get("29")

            # Cek open_id
            if not open_id:
                flow.response = http.Response.make(
                    400,
                    b"[FF0000]Open ID tidak ditemukan!\n",
                    {"Content-Type": "text/plain"}
                )
                return

            # Cek access_token
            if not access_token:
                msg = (
                    f"[FF0000]Open ID: [FFF000]{open_id}\n"
                    f"[FF0000]Access Token tidak ditemukan!\n"
                    f"[FFFFFF]Status: [FF0000]FAILED\n"
                )
                flow.response = http.Response.make(
                    400,
                    msg.encode("utf-8"),
                    {"Content-Type": "text/plain"}
                )
                return

            # Sukses
            msg = (
                f"[FF0000]OPEN ID: [00FF00]{open_id}\n"
                f"[FF0000]ACCESS TOKEN: [FFF000]{access_token}\n"
                f"[FFFFFF]Status: [00FF00]OK\n"
            )
            flow.response = http.Response.make(
                200,
                msg.encode("utf-8"),
                {"Content-Type": "text/plain"}
            )

        except Exception as e:
            error_data = json.dumps({"status": "error", "message": str(e)})
            flow.response = http.Response.make(
                400,
                error_data.encode("utf-8"),
                {"Content-Type": "application/json"}
            )

addons = [
    LoginInterceptor()
]
