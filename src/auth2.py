

import httpx
import secrets
import string
import base64
import hashlib
import threading
import webbrowser
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

# ====== 配置参数 (实际使用需替换为真实值) ======
CLIENT_ID = "00000000402b5328"  # 微软Minecraft官方客户端ID
SCOPE = "XboxLive.signin offline_access"
# 2. 必须严格匹配官方注册的回调地址 (注意端口 8080 和路径)
REDIRECT_URI = "http://127.0.0.1:8/login-with-microsoft"
AUTH_ENDPOINT = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MINECRAFT_API = "https://api.minecraftservices.com/launcher/login"

# ====== 配置参数 ======
# 替换为允许 localhost 回调的公共 Client ID
CLIENT_ID = "50b95c1f-6199-4339-9688-44856d69b219" 

# 必须与下方服务器监听的地址完全一致
REDIRECT_URI = "http://localhost:8080/callback"
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
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write("""
            <html><body style="text-align: center; padding: 50px;">
                <h1>✅ 登录成功</h1>
                <p>Microsoft账号已授权，可安全关闭此窗口</p>
                <script>window.close()</script>
            </body></html>
        """.encode())

    def log_message(self, format, *args): 
        return # 禁用日志

def start_local_server(state):
    """启动本地HTTP服务等待回调"""
    # 强制绑定 8080 端口以匹配官方 Client ID 的白名单
    server = HTTPServer(("127.0.0.1", 8080), OAuthCallbackHandler)
    server.expected_state = state
    server.timeout = 120
    
    # 绑定事件对象
    server.server_ready = threading.Event()

    server_thread = threading.Thread(target=server.serve_forever, args=(0.1,))
    server_thread.daemon = True
    server_thread.start()
    
    print(f"✅ 本地服务已启动: {REDIRECT_URI}")
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

def get_minecraft_token(access_token):
    """用微软令牌换取Minecraft服务令牌"""
    headers = {"Authorization": f"Bearer {access_token}"}
    with httpx.Client() as client:
        resp = client.get(MINECRAFT_API, headers=headers)
        resp.raise_for_status()
        return resp.json()

def main():
    # ===== 阶段1: 准备PKCE和CSRF防护 =====
    state = secrets.token_urlsafe(16)  # CSRF令牌
    code_verifier, code_challenge = generate_pkce_codes()
    
    # ===== 阶段2: 启动本地HTTP服务 =====
    server, server_thread = start_local_server(state)
    print(f"✅ 本地服务已启动: {REDIRECT_URI}")

    # ===== 阶段3: 构建授权URL并打开浏览器 =====
    auth_url = (
        f"{AUTH_ENDPOINT}?"
        f"client_id={CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={SCOPE.replace(' ', '+')}&"
        f"state={state}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    print(f"🔗 请访问授权URL (已自动打开浏览器):\n{auth_url}")
    webbrowser.open(auth_url)

    # ===== 阶段4: 等待用户授权回调 =====
    print("⏳ 等待用户授权... (120秒超时)")
    if not server.server_ready.wait(timeout=120):
        server.shutdown()
        raise TimeoutError("用户未在120秒内完成授权")

    print(f"🔑 已获取授权码: {OAuthCallbackHandler.auth_code[:10]}... (安全隐藏)")

    # ===== 阶段5: 用授权码换取令牌 =====
    data = {
        "client_id": CLIENT_ID,
        "code": OAuthCallbackHandler.auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    with httpx.Client() as client:
        resp = client.post(TOKEN_ENDPOINT, data=data, headers=headers)
        resp.raise_for_status()
        tokens = resp.json()
    
    print(f"🔐 已获取访问令牌: {tokens['access_token'][:15]}... (有效期 {tokens['expires_in']}秒)")

    # ===== 阶段6: 验证Minecraft许可证 =====
    mc_token = get_minecraft_token(tokens["access_token"])
    print("\n🎮 Minecraft账户信息:")
    print(f"  - 用户名: {mc_token['username']}")
    print(f"  - 账户ID: {mc_token['available_profiles'][0]['id']}")
    print(f"  - 游戏许可证: {'✅ 已购买' if mc_token['available_profiles'] else '❌ 未购买'}")

    # ===== 清理 =====
    server.shutdown()
    print("\n🔒 本地服务已安全关闭")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 流程失败: {str(e)}")
        exit(1)