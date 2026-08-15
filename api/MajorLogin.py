from http.server import BaseHTTPRequestHandler
from Crypto.Cipher import AES
import json
import time

MAIN_KEY = b'Yg&tc%DEuh6%Zc^8'
MAIN_IV  = b'6oyZDr22E3ychjM%'

def pad(data: bytes) -> bytes:
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def aes_cbc_encrypt(data_bytes: bytes) -> bytes:
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    return cipher.encrypt(pad(data_bytes))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Payload response akun tidak ditemukan
        payload = {
            "type": "account_not_found",
            "msg": "account not found",
            "server_time": int(time.time() * 1000)
        }
        
        raw_response = (json.dumps(payload) + "\n").encode('utf-8')
        encrypted_response = aes_cbc_encrypt(raw_response)

        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()
        self.wfile.write(encrypted_response)
        return
