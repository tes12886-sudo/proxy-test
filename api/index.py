import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import blackboxprotobuf
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx
from upstash_redis.asyncio import Redis
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

# Inisialisasi Upstash Redis
redis_client = Redis(
    url="https://harmless-muskrat-144397.upstash.io",
    token="gQAAAAAAAjQNAAIgcDI2ZGU0M2ZmNTNiMjQ0NTJlOTAwNjRlZDAyMzY4ODZhOA",
)

MAIN_KEY = b"Yg&tc%DEuh6%Zc^8"
MAIN_IV = b"6oyZDr22E3ychjM%"
BASE_TARGET_URL = "https://loginbp.ggpolarbear.com"

# Data versi
VER_DATA = {
    "code": 0,
    "is_server_open": True,
    "is_firewall_open": False,
    "cdn_url": "https://dl.cdn.freefiremobile.com/live/ABHotUpdates/",
    "backup_cdn_url": "https://dl.cdn.freefiremobile.com/live/ABHotUpdates/",
    "abhotupdate_cdn_url": "https://dl-core.cdn.freefiremobile.com/live/ABHotUpdates/",
    "img_cdn_url": "https://dl.cdn.freefiremobile.com/common/",
    "login_download_optionalpack": "optionalclothres:shaders|optionalpetres:optionalpetres_commonab_shader|optionallobbyres:",
    "need_track_hotupdate": True,
    "abhotupdate_check": "cache_res;assetindexer;SH-Gpp",
    "latest_release_version": "OB54",
    "min_hint_size": 1,
    "space_required_in_GB": 1.48,
    "should_check_ab_load": False,
    "force_refresh_restype": "optionalavatarres",
    "remote_version": "1.130.22",
    "server_url": "https://bahlil.embege-enak-loh.my.id/",
    "is_review_server": False,
    "use_login_optional_download": True,
    "use_background_download": False,
    "use_background_download_lobby": False,
    "country_code": "SG",
    "client_ip": "23.236.119.226",
    "gdpr_version": 0,
    "billboard_cdn_url": "https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi101.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi102.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi103.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi104.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi105.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi106.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi107.ff_extend",
    "billboard_msg": "",
    "web_url": "",
    "billboard_bg_url": "https://dl.cdn.freefiremobile.com/common/OB23/version/Patch_Bg.png",
    "max_store": "",
    "max_web": "",
    "max_video": "",
    "patchnote_url": "https://dl.dir.freefiremobile.com/common/web_event/aswqooiwd/zClWsKYO.html?lang=en",
    "multi_region": "",
    "need_check_ip_list": [],
    "network_log_server": "https://sgnetwork.ggblueshark.com/",
    "web_log_server": "https://networkselftest.ff.garena.com/api/",
    "login_failed_count": 2,
    "test_url": "",
    "core_url": "csoversea.castle.freefiremobile.com",
    "core_ip_list": ["0.0.0.0", "50.109.27.134", "129.226.2.163", "129.226.1.13", "129.226.1.16"],
    "appstore_url": "http://play.google.com/store/apps/details?id=com.dts.freefireth",
    "backup_appstore_url": "",
    "garena_login": False,
    "garena_hint": False,
    "gop_url": "",
    "gamevar": "var_name,comment,var_type,var_value,var_region,var_platform\nvar_name,comment,var_type,var_value,var_region,var_platform\nEnableVariableFFVoiceIDC,EnableVariableFFVoiceIDC,bool,False,,\nEnableYieldMutexDuringAsyncLoad,EnableYieldMutexDuringAsyncLoad,bool,False,,\nNinthProgressLoadingDuration,NinthProgressLoadingDuration,float,0,,\nEnableUGCScrollViewCulling,EnableUGCScrollViewCulling,bool,False,,\nEnableUGCScrollViewCulling,EnableUGCScrollViewCulling,bool,False,,\nReservedInt01,ReservedInt01,int,5,,\nNinthLevelPortalRadius,NinthLevelPortalRadius,float,20,,\nEnable2018ABstreamed,Enable2018ABstreamed,bool,False,,ios\nEnableAsyncCullResultsRelease,EnableAsyncCullResultsRelease,bool,False,,ios\nReservedInt02,ReservedInt02,int,30,,\nEnableUGCHalfwayJoin,EnableUGCHalfwayJoin,bool,False,,\nLadderMatchSplashRegionOn,LadderMatchSplashRegionOn,string,PK;EUROPE;TH;SG;TW;BR,,\nSensitivityMaxSetting,SensitivityMaxSetting,float,8.5,,\nSensitivity1PMaxSetting,Sensitivity1PMaxSetting,float,8.5,,\nX1ScopeMaxSetting,X1ScopeMaxSetting,float,8.5,,\nX2ScopeMaxSetting,X2ScopeMaxSetting,float,8.5,,\nX4ScopeMaxSetting,X4ScopeMaxSetting,float,8.5,,\nX8ScopeMaxSetting,X8ScopeMaxSetting,float,8.5,,\nFreeLookMaxSetting,FreeLookMaxSetting,float,8.5,,\nPlayerOutlineWidthSpecial,PlayerOutlineWidthSpecial,float,8.5,,\n",
    "remote_option_version": "optionallocres:50|optionalavatarres:791|optionalclothres:1228|optionalfootballres:27|optionalfullscreencgres:319|optionalhuntinggroundres:246|optionalinfection:125|optionalingameres:503|optionallobbyres:640|optionallonewolfres:86|optionallonewolfstrikeoutres:59|optionalludores:42|optionalmap1res:385|optionalmap2res:156|optionalmap4res:139|optionalmaphippores:118|optionalmapres:357|optionalnewblast:163|optionalpetres:910|optionalrushb:108|optionalrushingpetsres:84|optionalsnowduelres:65|optionalsocialres:223|optionaltrainingres:297|optionalugcres:844|optionalvoiceres:344|optionalwerewolves:153|optionalwerunres:92|optionalmapponyres:204|optionalugcoldparadiseres:34|optionalmultiregionres:29",
    "remote_option_version_astc": "optionallocres:50|optionalavatarres:753|optionalclothres:1228|optionalfootballres:29|optionalfullscreencgres:306|optionalhuntinggroundres:216|optionalinfection:124|optionalingameres:461|optionallobbyres:640|optionallonewolfres:206|optionallonewolfstrikeoutres:155|optionalludores:175|optionalmap1res:385|optionalmap2res:192|optionalmap4res:175|optionalmaphippores:120|optionalmapres:391|optionalnewblast:162|optionalpetres:910|optionalrushb:241|optionalrushingpetsres:217|optionalsnowduelres:65|optionalsocialres:215|optionaltrainingres:267|optionalugcres:786|optionalvoiceres:379|optionalwerewolves:286|optionalwerunres:81|optionalmapponyres:204|optionalugcoldparadiseres:33|optionalmultiregionres:27",
    "ggp_url": "gin.freefiremobile.com",
}


def aes_decrypt(data: bytes) -> bytes:
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    decrypted = cipher.decrypt(data)
    return unpad(decrypted, AES.block_size)


def make_octet_response(text: str, status_code: int = 400) -> Response:
    return Response(
        content=text.encode("utf-8"),
        status_code=status_code,
        media_type="application/octet-stream",
    )


# Handler khusus MajorLogin (Sniffing Request & Response Token + Forward)
@app.post("/MajorLogin")
@app.post("/majorlogin")
@app.post("/api/MajorLogin")
@app.post("/api/majorlogin")
async def handle_major_login(request: Request):
    body = await request.body()
    if not body:
        return make_octet_response("Request body is empty\n", status_code=400)

    open_id = None
    access_token = None

    # 1. Dekripsi & Ekstrak OpenID & Access Token dari Request
    try:
        try:
            req_ciphertext = bytes.fromhex(body.decode("utf-8", errors="ignore").strip())
        except Exception:
            req_ciphertext = body

        if len(req_ciphertext) > 0 and len(req_ciphertext) % 16 == 0:
            req_decrypted = aes_decrypt(req_ciphertext)
            req_decoded, _ = blackboxprotobuf.protobuf_to_json(req_decrypted)
        else:
            req_decoded, _ = blackboxprotobuf.protobuf_to_json(body)

        if isinstance(req_decoded, str):
            req_fields = json.loads(req_decoded)
        elif isinstance(req_decoded, dict):
            req_fields = req_decoded
        else:
            req_fields = {}

        if "22" in req_fields:
            open_id = str(req_fields["22"])
        if "29" in req_fields:
            access_token = str(req_fields["29"])

    except Exception as e:
        print(f"[Warn] Gagal parse request body: {e}")

    # 2. Forward request original ke upstream target
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            target_res = await client.post(
                f"{BASE_TARGET_URL}/MajorLogin",
                content=body,
                headers=headers,
            )

            res_content = target_res.content
            account_id = None

            # 3. Dekripsi & Ekstrak Account ID dari Respon Server
            try:
                try:
                    res_ciphertext = bytes.fromhex(res_content.decode("utf-8", errors="ignore").strip())
                except Exception:
                    res_ciphertext = res_content

                # Coba dekripsi AES jika data berukuran kelipatan block size 16
                if len(res_ciphertext) > 0 and len(res_ciphertext) % 16 == 0:
                    try:
                        res_decrypted = aes_decrypt(res_ciphertext)
                        res_decoded, _ = blackboxprotobuf.protobuf_to_json(res_decrypted)
                    except Exception:
                        res_decoded, _ = blackboxprotobuf.protobuf_to_json(res_content)
                else:
                    res_decoded, _ = blackboxprotobuf.protobuf_to_json(res_content)

                if isinstance(res_decoded, str):
                    res_fields = json.loads(res_decoded)
                elif isinstance(res_decoded, dict):
                    res_fields = res_decoded
                else:
                    res_fields = {}

                # Field 1 = account_id (UInt64)
                if "1" in res_fields:
                    account_id = str(res_fields["1"])

            except Exception as e:
                print(f"[Warn] Gagal parse response account_id: {e}")

            # 4. Simpan paket data lengkap ke Upstash Redis
            if open_id or account_id:
                session_key = f"session:{account_id or open_id}"
                session_payload = {
                    "open_id": open_id,
                    "access_token": access_token,
                    "account_id": account_id,
                }
                
                await redis_client.set(
                    session_key,
                    json.dumps(session_payload),
                    ex=86400,
                )
                print(f"[Redis] Berhasil simpan session -> {session_payload}")

            # 5. Kembalikan respons asli server ke client
            return Response(
                content=target_res.content,
                status_code=target_res.status_code,
                headers=dict(target_res.headers),
            )

        except Exception as e:
            return make_octet_response(
                f"Error: [FFFFFF]{str(e)}\n",
                status_code=502,
            )


# Handler Tangkap Semua Request (Catch-All)
@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
)
async def catch_all(request: Request, path: str):
    # Cek apakah path mengandung 'ver.php'
    if "ver.php" in path.lower() or path.lower().endswith("ver.php"):
        # Salin dict agar data default tidak termodifikasi permanen
        response_data = VER_DATA.copy()
        
        # Ambil query parameter ?version=...
        client_version = request.query_params.get("version")
        
        if client_version:
            # Ambil digit mayor pertama sebelum titik (contoh: "1" dari "1.109.1" atau "2" dari "2.109.1")
            major_prefix = client_version.split(".")[0]
            
            # Ganti prefix remote_version (130.22 tetap dipertahankan)
            response_data["remote_version"] = f"{major_prefix}.130.22"
            
        return JSONResponse(content=response_data, status_code=200)

    # Forward semua path lainnya ke target URL
    target_url = f"{BASE_TARGET_URL}/{path}"
    if request.url.query:
        target_url += f"?{request.url.query}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)

    body = await request.body()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            target_res = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body if body else None,
            )
            return Response(
                content=target_res.content,
                status_code=target_res.status_code,
                headers=dict(target_res.headers),
            )
        except Exception as e:
            return make_octet_response(
                f"Proxy Error: [FFFFFF]{str(e)}\n",
                status_code=502,
            )


# Handler Root Path
@app.api_route("/", methods=["GET", "POST"])
async def root(request: Request):
    # Jika root langsung diakses tanpa ver.php, tetap forward ke base target
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)

    body = await request.body()
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            target_res = await client.request(
                method=request.method,
                url=BASE_TARGET_URL,
                headers=headers,
                content=body if body else None,
            )
            return Response(
                content=target_res.content,
                status_code=target_res.status_code,
                headers=dict(target_res.headers),
            )
        except Exception as e:
            return make_octet_response(
                f"Proxy Error: [FFFFFF]{str(e)}\n",
                status_code=502,
            )
