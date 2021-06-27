from rich.console import Console
from tqdm import tqdm

from genshin.helper import Award, Helper
from genshin.models import Account
from local_config import cookies

console = Console()
iter = 0

progress = tqdm(cookies, desc=f"剩餘{len(cookies)}組帳號")
for cookie in progress:
    account = Account(cookies=cookie)

    helper = Helper(account=account)
    result = helper.run()

    # Failed to login
    if result["retcode"] != 0:
        console.log(f":x: 登入失敗，請重新綁定帳號！")

    # Failed to sign
    elif not result["data"]["is_sign"]:
        console.log(f":bangbang: 簽到失敗！ 請通知作者！")

    # Successfully signed
    else:
        total_sign_day = result["data"]["total_sign_day"]
        award: Award = helper.awards[total_sign_day]

        console.log(f":white_check_mark: 抽獎成功！\n獲得獎勵：{award.name} * {award.count}")
    iter += 1
    progress.set_description(f"剩餘{len(cookies) - iter}組帳號")
