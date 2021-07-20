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

def post(url, data=None, content="application/json"):

    headers = {
        #"Content-Type": "application/x-www-form-urlencoded;charset=utf-8;",
        "Content-Type": content,
    }

    r = request.Request(url, data=data, headers=headers, method="POST")

    j = request.urlopen(r).read()

    with open("post.html", "wb") as f:
        f.write(j)

    print("data j:", j)

    result = json.loads(j)

    return result


find_code = re.compile("https\://login\.live\.com/oauth20_desktop\.srf\?code=(.*?)&lc=(.*?)")

URL="https://login.live.com/oauth20_authorize.srf"

# Minecraft ID
client_id="00000000402b5328"


# Microsoft auth
def microsoft_auth():

    # client_id为minecraft在azure的服务名，response_type为返回结果类型，scope为验证服务的类型，redirect_uri为返回的重定向链接。
    # client_id="client_id=00000000402b5328&"
    # leftover="response_type=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf"

    usercache_file = Path("usercaches.json")
    if usercache_file.is_file():

        with open(usercache_file) as f:
            usercache = json.load(f)
        
        # code 过期
        if usercache["timestamp"] + usercache["expires_in"] < (int(time.time() - 600)):

            # 之后成功了用优化
            param={
                "client_id": client_id,
                "response_type": "code",
                "grant_type": "authorization_code",
                "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
                "scope": "service::user.auth.xboxlive.com::MBI_SSL"
            }

            data = parse.urlencode(param)

            webbrowser.open_new(URL + "?" + data)

            #login_url = getpass.getpass("成功登录后的浏览器URL: ")
            login_url = input("成功登录后的浏览器URL: ")

            re_code =  find_code.match(login_url)

            if re_code:
                code = re_code.group(1)
                print(code)
            else:
                print("不对")
    

            # Authorization Code -> Toke
            URL_token="https://login.live.com/oauth20_token.srf"

            param={
                "client_id": client_id,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
                "scope": "service::user.auth.xboxlive.com::MBI_SSL"
            }

            data = parse.urlencode(param)
            j = post(URL_token, data.encode("utf-8"), "application/x-www-form-urlencoded;charset=utf-8;")
            print("j --> ")
            pprint(j)

        else:
            # Xbox Live验证
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

            data = json.dumps(param)

            xbox = post(URL_xbox, data.encode("utf-8"), "application/json")

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

    data = json.dumps(param)
    xsts = post(URL_xsts, data.encode("utf-8"), "application/json")

    print("xsts -->")
    print(xsts)

    xsts_token = xsts["Token"]
    xsts_uhs = xsts["DisplayClaims"]["xui"][0]["uhs"]

    # get MC access_token
    url_mc_profile="https://api.minecraftservices.com/minecraft/profile"
    URL_mc="https://api.minecraftservices.com/authentication/login_with_xbox"

    param = {
        "identityToken": "XBL3.0 x=" + xsts_uhs + ";" + xsts_token,
    }

    data = json.dumps(param)
    r = request.Request(url_mc_profile, data=data.encode("utf-8"), headers={"Content-Type": "application/json"}, method="GET")

    mc_j = json.loads(request.urlopen(r).read(), ensure_ascii=False, indent=4)
    print("mc_j --> ")
    pprint(mc_j)

    return mc_j

# test
code="M.R3_BAY.aff26ae3-db72-292c-c331-a960b961863e"
j = microsoft_auth()

print(f"返回的json: {j}")
