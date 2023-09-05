import requests
import utils as utils
import json
from datetime import datetime
import secret as secret
import logging

url = {
    "gs": "https://sg-hk4e-api.hoyolab.com/event/sol/sign?lang=en-us&act_id=e202102251931481",
    "hsr": "https://sg-public-api.hoyolab.com/event/luna/os/sign?lang=en-us&act_id=e202303301540311",
    "hi3": "https://sg-public-api.hoyolab.com/event/mani/sign?lang=en-us&act_id=e202110291205111",
}


cfg = {
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
}

errColor = 0xED4E4E
succColor = 0x54ED4E


def get_token(ltoken: str, ltuid: str):
    return f"ltoken={ltoken}; ltuid={ltuid};"


def get_headers(token: str):
    return {
        "Cookie": token,
    }


def auto_signin_from_token_dict(token: dict) -> dict:
    out = {}
    for game in token["games"]:
        try:
            headers = get_headers(get_token(token["ltoken"], token["ltuid"]))
            resp = requests.post(url[game], headers=headers)
            if resp.status_code != 200:
                out[game] = (
                    "",
                    Exception(f"resp status code is not 200, resp {resp.status_code}"),
                )
                continue
            out[game] = (json.loads(resp.text)["message"], None)
        except Exception as err:
            out[game] = ("", err)
    return out


if __name__ == "__main__":
    logging.basicConfig(filename="runtime.log", encoding="utf-8", level=logging.INFO)
    for token in secret.HOYO_TOKENS:
        r = auto_signin_from_token_dict(token)
        for game, resp in r.items():
            msg, err = resp
            color = errColor
            if err is None:
                color = succColor
            discord_embed = {
                "title": f"{cfg[game]['long_name']} Auto Check-in",
                "description": f"*Helping check-ins~*",
                "author": {
                    "name": "HoyoHelper",
                    "url": "https://img-os-static.mihoyo.com/avatar/avatar1.png",
                    "icon_url": "https://img-os-static.mihoyo.com/avatar/avatar1.png",
                },
                "url": f"https://www.hoyolab.com/accountCenter/postList?id={token['ltuid']}",
                "fields": [
                    {"name": "Check-in Status", "value": f"**{msg}**"},
                ],
                "footer": {
                    "text": f"HoyoHelper {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
                "color": color,
                "image": {"url": cfg[game]["icon_url"]},
            }
            logging.info(
                utils.to_discwebhook(
                    None,
                    secret.DISCORD_WEBHOOK,
                    discord_embed,
                )
            )
