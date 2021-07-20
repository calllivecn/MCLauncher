#!/usr/bin/env python3
# coding=utf-8
# date 2021-07-19 23:23:10
# author calllivecn <c-all@qq.com>


import re
import json
import time
import getpass
import webbrowser
from pathlib import Path
from urllib import (
    request,
    parse,
)

from pprint import pprint

def req(url, param=None, method="GET", content="application/json"):

    headers = {
        #"Content-Type": "application/x-www-form-urlencoded;charset=utf-8;",
        "Content-Type": content,
    }

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


# 
find_code = re.compile("https\://login\.live\.com/oauth20_desktop\.srf\?code=(.*?)&lc=(.*?)")

# Minecraft ID
CLIENT_ID="00000000402b5328"

# 用户登录 缓存
USERCACHE_FILE = Path("cache.json")

# 保存 cachefile
def save_cachefile(j):
    data = {
        "timestamp": int(time.time()),
        "expires_in": j["expires_in"],
        "access_token": j["access_token"],
        "refresh_token": j["refresh_token"],
    }

    with open(USERCACHE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Microsoft auth
def microsoft_auth():
    # client_id为minecraft在azure的服务名，response_type为返回结果类型，scope为验证服务的类型，redirect_uri为返回的重定向链接。
    URL="https://login.live.com/oauth20_authorize.srf"

    param={
        "client_id": CLIENT_ID,
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
            print(code)
            break
        else:
            print("不是成功登录后的浏览器URL，请重新输入。")
    
    return code

# Authorization Code -> Toke
def get_access_token(code):
    URL_token="https://login.live.com/oauth20_token.srf"

    param={
        "client_id": CLIENT_ID,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
        "scope": "service::user.auth.xboxlive.com::MBI_SSL"
    }

    j = req(URL_token, param, "POST", "application/x-www-form-urlencoded;charset=utf-8;")
    save_cachefile(j)
    return j

# refresh accesstoken
def refresh(refresh_token):
    URL_token="https://login.live.com/oauth20_token.srf"

    param={
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
        "scope": "service::user.auth.xboxlive.com::MBI_SSL"
    }

    j = req(URL_token, param, "POST", "application/x-www-form-urlencoded;charset=utf-8;")

    save_cachefile(j)
    
    return j


# usercache.json 过期没有
def isexpires(filename):

    if filename.exists() and filename.is_file():
        with open(filename) as f:
            usercache = json.load(f)
    else:
        return None

    # code 没过期
    if usercache["timestamp"] + usercache["expires_in"] > (int(time.time() - 600)):
        return usercache
    else:
        return None


def auth():

    # 有token, 且没过期
    usercache = isexpires(USERCACHE_FILE)
    if usercache:
        j = refresh(usercache["refresh_token"])
    else:
        code = microsoft_auth()
        j = get_access_token(code)

    print("j --> ")
    pprint(j)

    URL_xbox="https://user.auth.xboxlive.com/user/authenticate"

    param = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": j["access_token"]
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }

    xbox = req(URL_xbox, param, "POST", "application/json")

    print("xbox --> ")
    pprint(xbox)

    xbox_token = xbox["Token"]
    xbox_uhs = xbox["DisplayClaims"]["xui"][0]["uhs"]

    # XSTS
    URL_xsts="https://xsts.auth.xboxlive.com/xsts/authorize"

    param = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [xbox_token],
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT",
    }

    xsts = req(URL_xsts, param, "POST", "application/json")

    print("xsts -->")
    print(xsts)

    xsts_token = xsts["Token"]
    xsts_uhs = xsts["DisplayClaims"]["xui"][0]["uhs"]

    url_mc_profile="https://api.minecraftservices.com/minecraft/profile"

    # get MC access_token
    URL_mc="https://api.minecraftservices.com/authentication/login_with_xbox"

    param = {
        "identityToken": "XBL3.0 x=" + xsts_uhs + ";" + xsts_token,
    }

    mc_j = req(url_mc_profile, param, "GET", "application/json")

    print("mc_j --> ")
    pprint(mc_j)

    return mc_j

# test
code="M.R3_BAY.aff26ae3-db72-292c-c331-a960b961863e"
j = auth()

print(f"返回的json: {j}")
