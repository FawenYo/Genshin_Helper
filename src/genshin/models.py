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
        cookies = self.cookies.split("; ")
        for each in cookies:
            is_required = False
            required_info = [
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

                if key == "_MHYUUID":
                    self.uuid = value
                elif key == "account_id":
                    self.account_id = value
                elif key == "cookie_token":
                    self.cookie_token = value
                elif key == "ltoken":
                    self.ltoken = value
                elif key == "ltuid":
                    self.ltuid = value
