

import time
import httpx
import secrets
import string
import base64
import hashlib
import threading
import webbrowser
from urllib.parse import urlparse, parse_qs, urlencode
from http.server import HTTPServer, BaseHTTPRequestHandler

from logs import logger
from initconfig import CONF
from funcs import DotDict, get_dotdict, set_dotdict

# ====== 配置参数 ======
# HMCL 内置的 Microsoft OAuth App ID
CLIENT_ID = "6a3728d6-27a3-4180-99bb-479895b8f88e"
SCOPE = "XboxLive.signin offline_access"

# HMCL 使用 login.live.com 端点，且回调白名单为 localhost:29111~29115/auth-response
AUTH_ENDPOINT = "https://login.live.com/oauth20_authorize.srf"
TOKEN_ENDPOINT = "https://login.live.com/oauth20_token.srf"

# Xbox Live 认证链 (对应 HMCL MicrosoftService.authenticateViaLiveAccessToken)
XBOX_LIVE_AUTH = "https://user.auth.xboxlive.com/user/authenticate"
XSTS_AUTH = "https://xsts.auth.xboxlive.com/xsts/authorize"
XBOX_LOGIN = "https://api.minecraftservices.com/authentication/login_with_xbox"
MC_PROFILE = "https://api.minecraftservices.com/minecraft/profile"

# XSTS 返回的错误码 (对应 HMCL XboxAuthorizationException)
XERR_MESSAGES = {
    2148916227: "该账号已被 Xbox Live 封禁",
    2148916233: "该账号没有 Xbox Live 账号，请先在 Xbox 创建",
    2148916235: "当前国家/地区不支持 Xbox Live",
    2148916238: "该账号为未成年人，需先加入 Microsoft 家庭组",
}

SERVER_PORT = 29111
# 主机名必须是 localhost，不能用 127.0.0.1，否则与注册的回调地址不匹配
REDIRECT_URI = f"http://localhost:{SERVER_PORT}/auth-response"

# =====================

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """本地HTTP服务处理器 - 仅处理一次回调"""
    auth_code = None
    state = None

    def do_GET(self):
        # 1. 解析URL中的参数
        query = parse_qs(urlparse(self.path).query)
        code = query.get("code", [""])[0]
        state = query.get("state", [""])[0]

        # 2. 验证state防CSRF
        # 注意：这里可能会有 Pylance 波浪线报错，加 # type: ignore 忽略即可
        if state != self.server.expected_state: 
            self.send_error(400, "Invalid state parameter")
            return

        # 3. 保存授权码并标记服务可关闭
        self.__class__.auth_code = code
        self.__class__.state = state
        
        # 【修正点】必须通过 self.server 访问事件对象
        self.server.server_ready.set()  

        # 4. 返回用户友好页面
        # 必须声明 charset=utf-8，否则浏览器按默认编码解析会导致中文乱码
        body = """
            <html><head><meta charset="utf-8"></head><body style="text-align: center; padding: 50px;">
                <h1>✅ 登录成功</h1>
                <p>Microsoft账号已授权，可安全关闭此窗口</p>
                <script>window.close()</script>
            </body></html>
        """.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args): 
        return # 禁用日志

def start_local_server(state):
    """启动本地HTTP服务等待回调"""
    # 端口需与 REDIRECT_URI 一致 (HMCL 白名单为 29111~29115)
    server = HTTPServer(("127.0.0.1", SERVER_PORT), OAuthCallbackHandler)
    server.expected_state = state
    server.timeout = 120
    
    # 绑定事件对象
    server.server_ready = threading.Event()

    server_thread = threading.Thread(target=server.serve_forever, args=(0.1,))
    server_thread.daemon = True
    server_thread.start()

    return server, server_thread

def generate_pkce_codes():
    """生成PKCE必需的code_verifier和code_challenge"""
    # 1. 生成43-128字符的随机字符串 (推荐43)
    code_verifier = ''.join(secrets.choice(string.ascii_letters + string.digits) 
                           for _ in range(43))
    
    # 2. 计算SHA-256哈希
    hashed = hashlib.sha256(code_verifier.encode()).digest()
    
    # 3. Base64 URL安全编码 (移除=, /, +)
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')
    
    return code_verifier, code_challenge

def authenticate_with_xbox(client, ms_access_token):
    """微软令牌 -> Xbox Live 令牌 (对应 HMCL 的第一步 user/auth.xboxlive.com)"""
    payload = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={ms_access_token}",
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT",
    }
    resp = client.post(XBOX_LIVE_AUTH, json=payload, headers={"Accept": "application/json"})
    resp.raise_for_status()
    data = resp.json()
    uhs = data["DisplayClaims"]["xui"][0]["uhs"]
    return uhs, data["Token"]


def authorize_with_xsts(client, uhs, xbox_token):
    """Xbox Live 令牌 -> XSTS 令牌 (对应 HMCL 的第二步 xsts/authorize)"""
    payload = {
        "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]},
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT",
    }
    resp = client.post(XSTS_AUTH, json=payload, headers={"Accept": "application/json"})
    if resp.status_code == 401:
        data = resp.json()
        xerr = data.get("XErr")
        raise RuntimeError(XERR_MESSAGES.get(xerr, f"Xbox 授权失败: XErr={xerr}"))
    resp.raise_for_status()
    data = resp.json()
    return uhs, data["Token"]


def get_minecraft_token(ms_access_token):
    """微软令牌 -> XBL3.0 令牌 -> Minecraft 令牌，并返回 (令牌信息, 账户资料)"""
    with httpx.Client() as client:
        uhs, xbox_token = authenticate_with_xbox(client, ms_access_token)
        uhs, xsts_token = authorize_with_xsts(client, uhs, xbox_token)

        resp = client.post(
            XBOX_LOGIN,
            json={"identityToken": f"XBL3.0 x={uhs};{xsts_token}"},
            headers={"Accept": "application/json"},
        )
        resp.raise_for_status()
        mc_token = resp.json()

        profile_resp = client.get(
            MC_PROFILE,
            headers={"Authorization": f"Bearer {mc_token['access_token']}"},
        )
        profile_resp.raise_for_status()
        return mc_token, profile_resp.json()

def refresh_microsoft_token(refresh_token):
    """用 refresh_token 刷新微软令牌 (scope 含 offline_access)"""
    data = {
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "scope": SCOPE,
    }
    with httpx.Client() as client:
        resp = client.post(
            TOKEN_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        return resp.json()


def interactive_login():
    """交互式完成授权码流程，返回 (微软令牌, MC令牌, profile)"""
    state = secrets.token_urlsafe(16)  # CSRF令牌
    code_verifier, code_challenge = generate_pkce_codes()

    server, _ = start_local_server(state)
    logger.info(f"本地服务已启动: {REDIRECT_URI}")

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"{AUTH_ENDPOINT}?{urlencode(params)}"
    logger.info(f"请访问授权URL (已自动打开浏览器): {auth_url}")
    webbrowser.open(auth_url)

    logger.info("等待用户授权... (120秒超时)")
    try:
        if not server.server_ready.wait(timeout=120):
            raise TimeoutError("用户未在120秒内完成授权")

        code = OAuthCallbackHandler.auth_code
        if not code:
            raise RuntimeError("未获取到授权码")

        data = {
            "client_id": CLIENT_ID,
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
            "code_verifier": code_verifier,
        }
        with httpx.Client() as client:
            resp = client.post(
                TOKEN_ENDPOINT,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            resp.raise_for_status()
            tokens = resp.json()
    finally:
        server.shutdown()

    mc_token, profile = get_minecraft_token(tokens["access_token"])
    return tokens, mc_token, profile


class MicrosoftAuthorized:
    """使用：
    1. account = MicrosoftAuthorized(username)
    2. username, uuid, accesstoken = account.user()

    缓存到 CONF/<username>.json，优先用 refresh_token 免重复浏览器登录。
    """

    def __init__(self, username=None):
        self.username = username
        self.user_conf = CONF / (username + ".json") if username else None
        self.usercache = self._load_cache()

        mc_access_token = self.usercache.get("mc_access_token")
        mc_expires_at = self.usercache.get("mc_expires_at", 0)

        # 1. MC token 未过期，直接使用
        if mc_access_token and time.time() < mc_expires_at - 1800:
            logger.debug("MC access_token 未过期，直接使用。")
            return

        # 2. 用 refresh_token 静默刷新
        refresh_token = self.usercache.get("ms_refresh_token")
        if refresh_token:
            try:
                logger.debug("使用 ms refresh_token 刷新令牌。")
                tokens = refresh_microsoft_token(refresh_token)
                self._save_login(tokens)
                return
            except Exception as e:
                logger.warning(f"刷新令牌失败，转为重新登录: {e}")

        # 3. 交互式登录
        logger.info("需要 Microsoft 账号登录。")
        tokens, mc_token, profile = interactive_login()
        self._save_login(tokens, mc_token, profile)

    def _save_login(self, tokens, mc_token=None, profile=None):
        if mc_token is None or profile is None:
            mc_token, profile = get_minecraft_token(tokens["access_token"])

        self.username = profile["name"]
        self.user_conf = CONF / (self.username + ".json")

        cache = DotDict()
        cache["username"] = profile["name"]
        cache["uuid"] = profile["id"]
        cache["mc_access_token"] = mc_token["access_token"]
        cache["mc_expires_at"] = int(time.time()) + int(mc_token.get("expires_in", 86400))
        cache["ms_refresh_token"] = tokens.get("refresh_token")
        self.usercache = cache

        set_dotdict(cache, self.user_conf)

    def _load_cache(self):
        if self.user_conf is not None and self.user_conf.exists() and self.user_conf.is_file():
            try:
                return get_dotdict(self.user_conf)
            except Exception as e:
                logger.warning(f"读取账号缓存失败: {e}")
        return DotDict()

    def user(self) -> tuple[str, str, str]:
        return self.usercache.username, self.usercache.uuid, self.usercache.mc_access_token


if __name__ == "__main__":
    try:
        _, mc_token, profile = interactive_login()
        print("\n🎮 Minecraft账户信息:")
        print(f"  - 用户名: {profile['name']}")
        print(f"  - 账户ID: {profile['id']}")
        print(f"  - 游戏许可证: ✅ 已购买")
    except Exception as e:
        print(f"\n❌ 流程失败: {str(e)}")
        exit(1)