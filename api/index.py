import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import blackboxprotobuf
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI()

MAIN_KEY = b"Yg&tc%DEuh6%Zc^8"
MAIN_IV = b"6oyZDr22E3ychjM%"

VER_DATA = {
  "code": 0,
  "is_server_open": true,
  "is_firewall_open": false,
  "cdn_url": "https://dl.cdn.freefiremobile.com/advance/ABHotUpdates/",
  "backup_cdn_url": "https://dl.cdn.freefiremobile.com/advance/ABHotUpdates/",
  "abhotupdate_cdn_url": "https://api.24hrs-central.site/api/ff/14a13cf4/hotpatchs/",
  "img_cdn_url": "https://dl.cdn.freefiremobile.com/common/",
  "login_download_optionalpack": "",
  "need_track_hotupdate": false,
  "abhotupdate_check": "cache_res;assetindexer;SH-Gpp",
  "latest_release_version": "OB55",
  "min_hint_size": 1,
  "space_required_in_GB": 1.48,
  "should_check_ab_load": false,
  "force_refresh_restype": "optionalavatarres",
  "remote_version": "68.55.0",
  "server_url": "https://login.advance.freefiremobile.com/",
  "is_review_server": false,
  "use_login_optional_download": false,
  "use_background_download": false,
  "use_background_download_lobby": false,
  "country_code": "BR",
  "client_ip": "34.228.217.254",
  "gdpr_version": 1,
  "billboard_cdn_url": "https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/idolzjifnmi101.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/idolzjifnmi102.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/idolzjifnmi103.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/idolzjifnmi104.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/idolzjifnmi105.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/idolzjifnmi106.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/idolzjifnmi107.ff_extend",
  "billboard_msg": "",
  "web_url": "",
  "billboard_bg_url": "https://dl.cdn.freefiremobile.com/common/OB23/version/Patch_Bg.png",
  "max_store": "",
  "max_web": "",
  "max_video": "",
  "patchnote_url": "https://dl.dir.freefiremobile.com/common/web_event/aswqooiwd/eCYh86t5.html?lang=ind",
  "multi_region": "BD;IN;PK;VN;US;BR;EUROPE",
  "need_check_ip_list": [
    "202.81.108.9"
  ],
  "network_log_server": "https://api.24hrs-central.site",
  "web_log_server": "https://api.24hrs-central.site",
  "login_failed_count": 2,
  "test_url": "",
  "core_url": "api.24hrs-central.site",
  "core_ip_list": [
    "0.0.0.0",
    "50.109.254.254"
  ],
  "appstore_url": "http://play.google.com/store/apps/details?id=com.dts.freefireth",
  "backup_appstore_url": "",
  "garena_login": true,
  "garena_hint": true,
  "gop_url": "",
  "gamevar": "var_name,comment,var_type,var_value\nvar_name,comment,\"var_type float, int, bool\",var_value\nFFAntihackDisabledRegions,关闭MTP的地区,string,\"IND,BD,NA\"\nFFAntihackDisabledClientVariant,FFAntihackDisabledClientVariant,string,\"ClientUsingVersion_MAX_HPE,ClientUsingVersion_FFI,ClientUsingVersion_NORMAL,ClientUsingVersion_MAX|IND,ClientUsingVersion_MAX|BD,ClientUsingVersion_NORMAL|BD\"\nEnableMtpLiteDataRegion,mtp轻特征开关,string,\"BR,EUROPE,ID,ME,US,RU,SAC,SG,TH,TW,VN,PK,ZA\"\nFFAntihackEmulatorCheckDisbaledClientVariant,FFAntihackEmulatorCheckDisbaledClientVariant,string,\"ClientUsingVersion_FFI,ClientUsingVersion_MAX,ClientUsingVersion_NORMAL\"\nForceTutorial_ChangeHudABTest,fps流程中打开hud 选择界面的概率,float,-1\n",
  "remote_option_version": "optionallocres:50|optionalavatarres:791|optionalclothres:1228|optionalfootballres:27|optionalfullscreencgres:319|optionalhuntinggroundres:246|optionalinfection:125|optionalingameres:503|optionallobbyres:640|optionallonewolfres:86|optionallonewolfstrikeoutres:59|optionalludores:42|optionalmap1res:385|optionalmap2res:156|optionalmap4res:139|optionalmaphippores:118|optionalmapres:357|optionalnewblast:163|optionalpetres:910|optionalrushb:108|optionalrushingpetsres:84|optionalsnowduelres:65|optionalsocialres:223|optionaltrainingres:297|optionalugcres:844|optionalvoiceres:344|optionalwerewolves:153|optionalwerunres:92|optionalmapponyres:204|optionalugcoldparadiseres:34|optionalmultiregionres:29",
  "remote_option_version_astc": "optionallocres:50|optionalavatarres:753|optionalclothres:1228|optionalfootballres:29|optionalfullscreencgres:306|optionalhuntinggroundres:216|optionalinfection:124|optionalingameres:461|optionallobbyres:640|optionallonewolfres:206|optionallonewolfstrikeoutres:155|optionalludores:175|optionalmap1res:385|optionalmap2res:192|optionalmap4res:175|optionalmaphippores:120|optionalmapres:391|optionalnewblast:162|optionalpetres:910|optionalrushb:241|optionalrushingpetsres:217|optionalsnowduelres:65|optionalsocialres:215|optionaltrainingres:267|optionalugcres:786|optionalvoiceres:379|optionalwerewolves:286|optionalwerunres:81|optionalmapponyres:204|optionalugcoldparadiseres:33|optionalmultiregionres:27",
  "ggp_url": "api.24hrs-central.site",
  "show_high_framerate_UI": true
}

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

# Handler khusus MajorLogin
@app.post("/MajorLogin")
@app.post("/majorlogin")
@app.post("/api/MajorLogin")
@app.post("/api/majorlogin")
async def handle_major_login(request: Request):
    body = await request.body()
    if not body:
        return make_octet_response("Request body is empty\n", status_code=400)

    try:
        try:
            ciphertext = bytes.fromhex(body.decode("utf-8", errors="ignore").strip())
        except Exception:
            ciphertext = body

        if len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
            return make_octet_response("Invalid ciphertext length for AES-CBC\n", status_code=400)

        decrypted = aes_decrypt(ciphertext)
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

        if not open_id or not access_token:
            msg = (
                f"[FF0000]Open ID: [FFF000]{open_id or 'N/A'}\n"
                f"[FF0000]Access Token: [FFF000]{access_token or 'N/A'}\n"
                f"[FFFFFF]Status: [FF0000]FAILED\n"
            )
            return make_octet_response(msg, status_code=400)

        msg = (
            f"[FF0000]OPEN ID: [00FF00]{open_id}\n"
            f"[FF0000]ACCESS TOKEN: [FFF000]{access_token}\n"
            f"[FFFFFF]Status: [00FF00]OK\n"
        )
        return make_octet_response(msg, status_code=400)

    except Exception as e:
        err_msg = f"[FF0000]Error: [FFFFFF]{str(e)}\n"
        return make_octet_response(err_msg, status_code=400)

# Semua path lainnya (root, ver.php, dll.) akan merespons JSON VER_DATA
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def catch_all(path: str):
    return JSONResponse(content=VER_DATA, status_code=200)

@app.get("/")
@app.post("/")
async def root():
    return JSONResponse(content=VER_DATA, status_code=200)
