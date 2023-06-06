from datetime import datetime
from typing import Sequence

import genshin
import requests

from src import config
from src.utils.genshin_models import Account, DailyReward
from src.utils.logging_util import get_logger

logger = get_logger()


class GenshinHelper:
    def __init__(self, cookies: str, lang: str = "zh-tw") -> None:
        account = Account(cookies=cookies)

        self.awards: dict[int, DailyReward] = {}
        self.account_id: str = account.account_id
        self.uuid: str = account.uuid
        self.cookie_token: str = account.cookie_token
        self.ltoken: str = account.ltoken
        self.ltuid: str = account.ltuid

        client_cookies = {"ltuid": account.ltuid, "ltoken": account.ltoken}
        self.client = genshin.Client(
            client_cookies, lang=lang, game=genshin.Game.GENSHIN
        )

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
            "User-Agent": config.USER_AGENT,
        }
        response = requests.get(url=url, headers=headers, params=payload).json()
        for index, each in enumerate(response["data"]["awards"]):
            day = index + 1
            amount = each["cnt"]
            icon = each["icon"]
            name = each["name"]
            self.awards[day] = DailyReward(icon=icon, name=name, amount=amount)

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
            "User-Agent": config.USER_AGENT,
        }
        response = requests.post(
            url="https://hk4e-api-os.mihoyo.com/event/sol/sign?lang=zh-tw",
            headers=headers,
            params=payload,
        ).json()
        logger.debug(f"Sign in result: {response}")

        return self.account_status()

    async def claim_daily_reward(self) -> DailyReward:
        """Claim Daily Reward

        Raises:
            Exception: Errors encountered while claiming daily reward
        """
        try:
            result: genshin.models.DailyReward = await self.client.claim_daily_reward()
            reward: DailyReward = DailyReward(
                icon=result.icon, name=result.name, amount=result.amount
            )
        # Already claimed
        except genshin.AlreadyClaimed:
            logger.warning("Daily reward already claimed")
            # Get all rewards
            monthly_rewards: Sequence[
                genshin.models.DailyReward
            ] = await self.client.get_monthly_rewards()
            # Get today date
            today: datetime = datetime.now()
            # Get today reward
            result: genshin.models.DailyReward = monthly_rewards[today.day - 1]
            reward: DailyReward = DailyReward(
                icon=result.icon, name=result.name, amount=result.amount
            )
        except Exception as e:
            raise e
        return reward

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
            "User-Agent": config.USER_AGENT,
        }
        payload = {"act_id": act_id, "lang": lang}
        response = requests.get(
            url=f"https://hk4e-api-os.mihoyo.com/event/sol/info?lang=zh-tw&act_id={act_id}",
            headers=headers,
            params=payload,
        ).json()
        logger.debug(f"Account status: {response}")
        return response
