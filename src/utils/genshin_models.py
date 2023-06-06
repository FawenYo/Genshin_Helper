from dataclasses import dataclass


class Account:
    def __init__(self, cookies: str) -> None:
        self.cookies: str = cookies

        self.account_id: str = ""
        self.uuid: str = ""
        self.cookie_token: str = ""
        self.ltoken: str = ""
        self.ltuid: str = ""

        # Parse Cookies
        self.parse_cookies()

    def parse_cookies(self) -> None:
        """Parse Information from cookies' string"""
        cookies: list[str] = self.cookies.split("; ")
        for each in cookies:
            is_required: bool = False
            required_info: list[str] = [
                "_MHYUUID",
                "account_id",
                "cookie_token",
                "ltoken",
                "ltuid",
            ]
            for each_info in required_info:
                if each_info in each:
                    is_required = True
                    break
            if is_required:
                key, value = each.split("=")

                match key:
                    case "_MHYUUID":
                        self.uuid = value
                    case "account_id":
                        self.account_id = value
                    case "cookie_token":
                        self.cookie_token = value
                    case "ltoken":
                        self.ltoken = value
                    case "ltuid":
                        self.ltuid = value


@dataclass
class DailyReward:
    icon: str
    name: str
    amount: int
