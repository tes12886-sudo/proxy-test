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
    "server_url": "https://loginbp.ggpolarbear.com/",
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
    "gamevar": "var_name,comment,var_type,var_value,var_region,var_platform\n"
                "SensitivityMaxSetting,Sensi Umum,float,5000,,\n"
                "Sensitivity1PMaxSetting,Sensi 1P,float,5000,,\n"
                "X1ScopeMaxSetting,Sensi RedDot,float,5000,,\n"
                "X2ScopeMaxSetting,Sensi Scope2x,float,5000,,\n"
                "X4ScopeMaxSetting,Sensi Scope4x,float,5000,,\n"
                "X8ScopeMaxSetting,Sensi AWM,float,5000,,\n"
                "FreeLookMaxSetting,Sensi FreeLook,float,5000,,\n"
                "EnableVariableFFVoiceIDC,EnableVariableFFVoiceIDC,bool,false,,\n"
                "EnableYieldMutexDuringAsyncLoad,EnableYieldMutexDuringAsyncLoad,bool,false,,\n"
                "NinthProgressLoadingDuration,NinthProgressLoadingDuration,float,0,,\n"
                "EnableUGCScrollViewCulling,EnableUGCScrollViewCulling,bool,false,,\n"
                "EnableUGCScrollViewCulling,EnableUGCScrollViewCulling,bool,false,,\n"
                "ReservedInt01,ReservedInt01,int,5,,\n"
                "NinthLevelPortalRadius,NinthLevelPortalRadius,float,20,,\n"
                "Enable2018ABstreamed,Enable2018ABstreamed,bool,false,,ios\n"
                "EnableAsyncCullResultsRelease,EnableAsyncCullResultsRelease,bool,false,,ios\n"
                "ReservedInt02,ReservedInt02,int,30,,\n"
                "EnableUGCHalfwayJoin,EnableUGCHalfwayJoin,bool,false,,\n"
                "LadderMatchSplashRegionOn,LadderMatchSplashRegionOn,string,PK;EUROPE;TH;SG;TW;BR,,\n",
    "remote_option_version": "optionallocres:50|optionalavatarres:791|optionalclothres:1228|optionalfootballres:27|optionalfullscreencgres:319|optionalhuntinggroundres:246|optionalinfection:125|optionalingameres:503|optionallobbyres:640|optionallonewolfres:86|optionallonewolfstrikeoutres:59|optionalludores:42|optionalmap1res:385|optionalmap2res:156|optionalmap4res:139|optionalmaphippores:118|optionalmapres:357|optionalnewblast:163|optionalpetres:910|optionalrushb:108|optionalrushingpetsres:84|optionalsnowduelres:65|optionalsocialres:223|optionaltrainingres:297|optionalugcres:844|optionalvoiceres:344|optionalwerewolves:153|optionalwerunres:92|optionalmapponyres:204|optionalugcoldparadiseres:34|optionalmultiregionres:29",
    "remote_option_version_astc": "optionallocres:50|optionalavatarres:753|optionalclothres:1228|optionalfootballres:29|optionalfullscreencgres:306|optionalhuntinggroundres:216|optionalinfection:124|optionalingameres:461|optionallobbyres:640|optionallonewolfres:206|optionallonewolfstrikeoutres:155|optionalludores:175|optionalmap1res:385|optionalmap2res:192|optionalmap4res:175|optionalmaphippores:120|optionalmapres:391|optionalnewblast:162|optionalpetres:910|optionalrushb:241|optionalrushingpetsres:217|optionalsnowduelres:65|optionalsocialres:215|optionaltrainingres:267|optionalugcres:786|optionalvoiceres:379|optionalwerewolves:286|optionalwerunres:81|optionalmapponyres:204|optionalugcoldparadiseres:33|optionalmultiregionres:27",
    "ggp_url": "gin.freefiremobile.com"
}

# Semua path lainnya (root, ver.php, dll.) akan merespons JSON VER_DATA
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def catch_all(path: str):
    return JSONResponse(content=VER_DATA, status_code=200)

@app.get("/")
@app.post("/")
async def root():
    return JSONResponse(content=VER_DATA, status_code=200)
