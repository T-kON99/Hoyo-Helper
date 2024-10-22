import requests
import utils as utils
import json
import os
from datetime import datetime
import logging

DISCORD_WEBHOOK = None
HOYO_TOKENS = None
# Setup for production/local dev
try:
    DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
    HOYO_TOKENS = json.loads(os.environ["HOYO_TOKENS"])
except KeyError:
    try:
        import secret

        DISCORD_WEBHOOK = secret.DISCORD_WEBHOOK
        HOYO_TOKENS = secret.HOYO_TOKENS
    except ModuleNotFoundError:
        logging.fatal("env DISCORD_WEBHOOK / HOYO_TOKENS not configured properly")
        exit(1)
    except KeyError:
        pass


apiConf = {
    "gs": {
        "url": "https://sg-hk4e-api.hoyolab.com/event/sol/sign?lang=en-us&act_id=e202102251931481",
        "header_dict": {},
    },
    "hsr": {
        "url": "https://sg-public-api.hoyolab.com/event/luna/os/sign?lang=en-us&act_id=e202303301540311",
        # TODO: add hkrpg once needed based on https://github.com/canaria3406/hoyolab-auto-sign/issues/52
        "header_dict": {},
    },
    "hi3": {
        "url": "https://sg-public-api.hoyolab.com/event/mani/sign?lang=en-us&act_id=e202110291205111",
        "header_dict": {},
    },
    "zzz": {
        "url": "https://sg-act-nap-api.hoyolab.com/event/luna/zzz/os/sign?lang=en-us&act_id=e202406031448091",
        "header_dict": {"x-rpc-signgame": "zzz"},
    },
}

discordConf = {
    "gs": {
        "long_name": "Genshin Impact",
        "icon_url": "https://pbs.twimg.com/media/FDKGiHZVkAADAvD?format=jpg&name=medium",
    },
    "hsr": {
        "long_name": "Honkai Star Rail",
        "icon_url": "https://cdn2.steamgriddb.com/file/sgdb-cdn/icon/7e896649d0a9e3d1c3936eff8b945405.png",
    },
    "hi3": {
        "long_name": "Honkai Impact 3rd",
        "icon_url": "https://cdn2.steamgriddb.com/file/sgdb-cdn/icon_thumb/8e017d9b51e7b9284cd0da58fae39b33.png",
    },
    "zzz": {
        "long_name": "Zenless Zone Zero",
        "icon_url": "https://yt3.googleusercontent.com/bhTyZchnZVHuXYHyvBbSv02rThHjV5pBk1G6Hi0wV_5F1RdXDEf3r7PdQoyl3s0KO0hDiiPc=s900-c-k-c0x00ffffff-no-rj",
    },
}

errColor = 0xED4E4E
succColor = 0x54ED4E


def get_token(ltoken: str, ltuid: str, enableV2: bool):
    if enableV2:
        return f"ltoken_v2={ltoken}; ltuid_v2={ltuid};"
    return f"ltoken={ltoken}; ltuid={ltuid};"


def is_v2_token(token: dict):
    return token.get("enable_v2", False)


def get_discord_uid(token: dict):
    return token.get("discord_uid", None)


def get_headers(token: str):
    return {
        "Cookie": token,
    }


def get_merged_dict(d1: dict, d2: dict) -> dict:
    newDict = {}
    for k, v in d1.items():
        newDict[k] = v
    for k, v in d2.items():
        newDict[k] = v
    return newDict


def auto_signin_from_token_dict(token: dict) -> dict:
    out = {}
    for game in token["games"]:
        try:
            headers = get_headers(
                get_token(token["ltoken"], token["ltuid"], is_v2_token(token))
            )
            conf = apiConf[game]
            headers = get_merged_dict(headers, conf["header_dict"])
            resp = requests.post(conf["url"], headers=headers)
            if resp.status_code != 200:
                out[game] = (
                    "",
                    Exception(f"resp status code is not 200, resp {resp.status_code}"),
                )
                logging.error(resp.text)
                continue
            out[game] = (json.loads(resp.text)["message"], None)
        except Exception as err:
            out[game] = ("", err)
    return out


if __name__ == "__main__":
    logging.basicConfig(filename="runtime.log", encoding="utf-8", level=logging.INFO)
    for token in HOYO_TOKENS:
        r = auto_signin_from_token_dict(token)
        for game, resp in r.items():
            msg, err = resp
            color = succColor
            fields = [{"name": "Check-in Status", "value": f"**{msg}**"}]
            if err is not None:
                logging.error(f"error when attempting to sign in, err {err}")
                color = errColor
                fields.append({"name": "Error", "value": f"**{err}**"})
            logging.info(msg)
            discordEmbedAuthor = "HoyoHelper V2" if is_v2_token(token) else "HoyoHelper"
            discordUID = get_discord_uid(token)
            discordDescription = (
                f"*Helping <@!{discordUID}> check-ins~*"
                if discordUID is not None
                else f"*Helping check-ins~*"
            )
            discordEmbed = {
                "title": f"{discordConf[game]['long_name']} Auto Check-in",
                "description": discordDescription,
                "author": {
                    "name": discordEmbedAuthor,
                    "url": "https://img-os-static.mihoyo.com/avatar/avatar1.png",
                    "icon_url": "https://img-os-static.mihoyo.com/avatar/avatar1.png",
                },
                "url": f"https://www.hoyolab.com/accountCenter/postList?id={token['ltuid']}",
                "fields": [
                    {"name": "Check-in Status", "value": f"**{msg}**"},
                    {"name": "Error", "value": f"**{err}**"},
                ],
                "footer": {
                    "text": f"HoyoHelper {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
                "color": color,
                "image": {"url": discordConf[game]["icon_url"]},
            }
            logging.info(
                utils.to_discwebhook(
                    None,
                    DISCORD_WEBHOOK,
                    discordEmbed,
                )
            )
