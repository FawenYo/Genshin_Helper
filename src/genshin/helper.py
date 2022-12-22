from typing import Dict

import requests

from config import USER_AGENT
from genshin.models import Account


class Award:
    def __init__(self, name: str, count: int, icon: str) -> None:
        self.name: str = name
        self.count: int = count
        self.icon: str = icon


class Helper:
    def __init__(self, account: Account) -> None:
        self.awards: Dict[Award] = {}
        self.account_id: str = account.account_id
        self.uuid: str = account.uuid
        self.cookie_token: str = account.cookie_token
        self.ltoken: str = account.ltoken
        self.ltuid: str = account.ltuid

    def get_month_award(
        self, act_id: str = "e202102251931481", lang: str = "zh-tw"
    ) -> None:
        """Get Month Award

        Args:
            act_id (str, optional): Action ID. Defaults to "e202102251931481".
            lang (str, optional): Language. Defaults to "zh-tw".
        """
        url = "https://hk4e-api-os.mihoyo.com/event/sol/home?lang=zh-tw&act_id=e202102251931481"
        payload = {"act_id": act_id, "lang": lang}
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": f"_MHYUUID={self.uuid}; mi18nLang={lang}",
            "Referer": "https://webstatic-sea.mihoyo.com/",
            "User-Agent": USER_AGENT,
        }
        response = requests.get(url=url, headers=headers, params=payload).json()
        for index, each in enumerate(response["data"]["awards"]):
            day = index + 1
            count = each["cnt"]
            icon = each["icon"]
            name = each["name"]
            self.awards[day] = Award(name=name, count=count, icon=icon)

    def run(self, lang: str = "zh-tw"):
        """Sign in to Hoyolab

        Args:
            lang (str, optional): Language. Defaults to "zh-tw".
        """
        self.get_month_award()

        payload = {"act_id": "e202102251931481"}
        headers = {
            "Accept-Encoding": "application/json, text/plain, */*",
            "Cookie": f"mi18nLang={lang}; _MHYUUID={self.uuid}; account_id={self.account_id}; cookie_token={self.cookie_token}; ltoken={self.ltoken}; ltuid={self.ltuid}",
            "Referer": "https://webstatic-sea.mihoyo.com/",
            "User-Agent": USER_AGENT,
        }
        response = requests.post(
            url="https://hk4e-api-os.mihoyo.com/event/sol/sign?lang=zh-tw",
            headers=headers,
            params=payload,
        ).json()

        return self.account_status()

    def account_status(self, act_id: str = "e202102251931481", lang: str = "zh-tw"):
        """Account Sign in status

        Args:
            act_id (str, optional): Action ID. Defaults to "e202102251931481".
            lang (str, optional): Language. Defaults to "zh-tw".
        """
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": f"mi18nLang={lang}; _MHYUUID={self.uuid}; account_id={self.account_id}; cookie_token={self.cookie_token}; ltoken={self.ltoken}; ltuid={self.ltuid}",
            "Referer": "https://webstatic-sea.mihoyo.com/",
            "User-Agent": USER_AGENT,
        }
        payload = {"act_id": act_id, "lang": lang}
        response = requests.get(
            url=f"https://hk4e-api-os.mihoyo.com/event/sol/info?lang=zh-tw&act_id={act_id}",
            headers=headers,
            params=payload,
        )
        return response.json()
