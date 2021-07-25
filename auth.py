#!/usr/bin/env python3
# coding=utf-8
# date 2021-07-19 23:23:10
# author calllivecn <c-all@qq.com>


__all__ = (
    "auth",
)

import re
import sys
import json
import time
import webbrowser
from pathlib import Path
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from urllib import (
    request,
    parse,
)
from pprint import (
    pprint,
    pformat,
)

from logs import logger
from initconfig import (
    CONF,
)
from funcs import (
    DotDict,
)

"""
MC 认证过程文档：https://wiki.vg/ZH:Microsoft_Authentication_Scheme
"""

def utc2local(utc_dtm):
    local_tm = datetime.fromtimestamp(0)
    utc_tm = datetime.utcfromtimestamp(0)
    offset = local_tm - utc_tm
    return utc_dtm + offset

def local2utc(local_dtm):
    return datetime.utcfromtimestamp(local_dtm.timestamp())

def req(url, param=None, method="GET", header={}, content="application/json"):

    headers = {
        #"Content-Type": "application/x-www-form-urlencoded;charset=utf-8;",
        "Content-Type": content,
    }

    if header is not {}:
        headers.update(header)

    if param is None:
        data = None
    else:
        if content == "application/json":
            data=json.dumps(param).encode("utf-8")
        elif content == "application/x-www-form-urlencoded;charset=utf-8;":
            data = parse.urlencode(param).encode("utf-8")
        else:
            print("没定义的请求方式")
            data = None

    r = request.Request(url, data=data, headers=headers, method=method)

    j = request.urlopen(r).read()

    # 调试时，使用
    with open("post.json", "wb") as f:
        f.write(j)

    result = json.loads(j)

    return result


find_code = re.compile("https\://login\.live\.com/oauth20_desktop\.srf\?code=(.*?)&lc=(.*?)")

class AuthorizedError(Exception):
    pass

class MicrosoftAuthorized:
    """
    使用讲法：
    1. account = microsoftAuthorized(username)
    2. uesrnaem, uuid, accesstoken = account.user()
    """

    # Minecraft ID
    CLIENT_ID="00000000402b5328"

    def __init__(self, username=None):

        self.username = username
        self.usercache = DotDict()

        if self.username != None:
            self.user_conf = CONF / (self.username + ".json")
            # 有token(xbox), 且没过期
            self.is_xbox_expires()

        if self.usercache:
            xsts = self.get_xsts_token(self.usercache.xbox_token)
        else:
            code = self.microsoft_account_login()

            jdata = self.get_access_token(code)
            logger.debug("access_token ↓")
            logger.debug(pformat(jdata))

            # get xbox token
            xbox = self.get_xbox_token(jdata["access_token"])

            # XSTS
            xsts = self.get_xsts_token(xbox["Token"])


        xsts_token = xsts["Token"]
        xsts_uhs = xsts["DisplayClaims"]["xui"][0]["uhs"]


        # MC accesstoken expires 8小时
        if self.is_mc_expires():

            logger.debug("MC accesstoken 过期，重新请求。")

            # mc access token
            mc_j = self.get_mc_token(xsts_token, xsts_uhs)

            # check microsoft acounnts 是否拥有MC, 否则退出。
            if not self.check_mc(mc_j["access_token"]):
                msg = "你的微软账号没有MC"
                logger.error(msg)
                raise AuthorizedError(msg)
        
            # 添加 MC 启动的 access_token
            profile = self.get_mc_profile(mc_j["access_token"])

            # MC username
            self.username = profile["name"]

            self.usercache.username = profile["name"]
            self.usercache.uuid = profile["id"]
            self.usercache.mc_access_token = mc_j["access_token"]
            self.usercache.mc_timestamp = int(time.time())

            # 落盘
            self.save()

        # MC accesstoken 没过期。直接使用
        else:
            logger.debug("MC accesstoken 没过期直接使用。")
    
    def user(self):
        return self.usercache.username, self.usercache.uuid, self.usercache.mc_access_token

    # Microsoft auth
    def microsoft_account_login(self):
        # client_id为minecraft在azure的服务名，response_type为返回结果类型，scope为验证服务的类型，redirect_uri为返回的重定向链接。
        URL="https://login.live.com/oauth20_authorize.srf"

        param={
            "client_id": self.CLIENT_ID,
            "response_type": "code",
            "grant_type": "authorization_code",
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "scope": "service::user.auth.xboxlive.com::MBI_SSL"
        }
        data = parse.urlencode(param)
        webbrowser.open_new(URL + "?" + data)

        code = ""
        while code == "":
            #login_url = getpass.getpass("成功登录后的浏览器URL: ")
            login_url = input("成功登录后的浏览器URL: ")
            re_code =  find_code.match(login_url)

            if re_code:
                code = re_code.group(1)
                logger.debug("Microsoft_auth ↓")
                logger.debug(pformat(code))
                break
            else:
                print("不是成功登录后的浏览器URL，请重新输入。")

        return code

    # Authorization Code -> Toke
    def get_access_token(self, code):
        URL_token="https://login.live.com/oauth20_token.srf"

        param={
            "client_id": self.CLIENT_ID,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "scope": "service::user.auth.xboxlive.com::MBI_SSL"
        }

        j = req(URL_token, param, method="POST", content="application/x-www-form-urlencoded;charset=utf-8;")
        return j
    
    # refresh access token, 没必要刷新，xbox token 过期时间 有15天
    def refresh_access_token(self, refresh_token):
        URL_token="https://login.live.com/oauth20_token.srf"

        param={
            "client_id": self.CLIENT_ID,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "scope": "service::user.auth.xboxlive.com::MBI_SSL"
        }

        j = req(URL_token, param, method="POST", content="application/x-www-form-urlencoded;charset=utf-8;")

        return j

    # get xbox token
    def get_xbox_token(self, accesstoken):
        # xbox
        URL_xbox="https://user.auth.xboxlive.com/user/authenticate"

        param = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": accesstoken,
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }

        xbox = req(URL_xbox, param, method="POST")

        logger.debug("xbox ↓")
        logger.debug(pformat(xbox))

        self.usercache.xbox_expires_in = xbox["NotAfter"]
        self.usercache.xbox_token = xbox["Token"]

        return xbox

    # get xsts token
    def get_xsts_token(self, xbox_token):
        URL_xsts="https://xsts.auth.xboxlive.com/xsts/authorize"

        param = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [xbox_token],
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT",
        }

        xsts = req(URL_xsts, param, method="POST")

        logger.debug("xsts ↓")
        logger.debug(pformat(xsts))

        self.usercache.xsts_expires_in = xsts["NotAfter"]
        self.usercache.xsts_refresh_token = xsts["Token"]

        return xsts

    # get MC token
    def get_mc_token(self, xsts_token, xsts_uhs):
        URL_mc="https://api.minecraftservices.com/authentication/login_with_xbox"

        param = {
            "identityToken": "XBL3.0 x=" + xsts_uhs + ";" + xsts_token,
        }

        mc_j = req(URL_mc, param, method="POST")

        logger.debug("get MC token ↓")
        logger.debug(pformat(mc_j))

        self.usercache.mc_token_type = mc_j["token_type"]
        self.usercache.mc_expires_in = mc_j["expires_in"]

        return mc_j

    # check microsoft acounnts 是否拥有MC
    def check_mc(self, access_token):
        url_check_mc="https://api.minecraftservices.com/entitlements/mcstore"

        #header = {"Authorization": "Bearer " + access_token}
        header = {"Authorization": self.usercache.mc_token_type + " " + access_token}

        result = req(url_check_mc, header=header)
        if len(result["items"]) == 0:
            logger.error("你的微软账号里没Minecraft.")
            sys.exit(0)
        else:
            logger.debug("check mc ↓")
            logger.debug(pformat(result))
            return True
    
    # get MC profile
    def get_mc_profile(self, access_token):
        """
        正确返回：
        {
          "id" : "986dec87b7ec47ff89ff033fdb95c4b5", // 账号的真实uuid
          "name" : "HowDoesAuthWork", // 该账号的mc用户名
          "skins" : [ {
            "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
            "state" : "ACTIVE",
            "url" : "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
            "variant" : "CLASSIC",
            "alias" : "STEVE"
          } ],
          "capes" : [ ]
         }    
        错误返回：
        {
        "path" : "/minecraft/profile",
        "errorType" : "NOT_FOUND",
        "error" : "NOT_FOUND",
        "errorMessage" : "The server has not found anything matching the request URI",
        "developerMessage" : "The server has not found anything matching the request URI"
        }
        """
        url_mc_profile="https://api.minecraftservices.com/minecraft/profile"

        header = {"Authorization": "Bearer " + access_token}

        profile = req(url_mc_profile, header=header)

        logger.debug("profile ↓")
        logger.debug(pformat(profile))

        if profile.get("error"):
            msg = "获取Minecarft profile 失败"
            logger.error(msg)
            raise AuthorizedError(msg)
        
        #self.usercache.mc_expires_in = profile["NotAfter"]
        #self.usercache.mc_token = profile["token"]
        
        return profile


    # <username>.json 过期没有
    def is_xbox_expires(self):
        # dotdict = DotDict()
        if self.user_conf.exists() and self.user_conf.is_file():
            with open(self.user_conf) as f:
                self.usercache.load(f)
        else:
            return DotDict()

        # 把拿到 的UTC过期时间 转化为 本地时间
        expires = self.usercache.xbox_expires_in.split(".")[0]
        expires_in = datetime.strptime(expires + "Z", "%Y-%m-%dT%H:%M:%S%z")

        # code 没过期
        #if self.usercache.timestamp + self.usercache.expires_in > (int(time.time() - 600)):
        if datetime.now(timezone.utc) >= (expires_in - timedelta(minutes=600)):
            return self.usercache
        else:
            return DotDict()
    
    def is_mc_expires(self):
        # 没有过期
        logger.debug(f"is mc expres self.usercache.mc_timestamp: {self.usercache.mc_timestamp}")
        if self.usercache.mc_expires_in + self.usercache.mc_timestamp + 1800 < int(time.time()):
            return False
        else:
            return True

    def save(self):
        self.user_conf = CONF / (self.username + ".json")
        with open(self.user_conf, "w") as f:
            self.usercache.dump(f, ensure_ascii=False, indent=4)



# test
if __name__ == "__main__":
    logger.setLevel(2)
    user = MicrosoftAuthorized("calllivecn")
    j = user.user()
    print(f"返回的json: {j}")
