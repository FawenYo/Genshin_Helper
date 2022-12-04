import logging

from tqdm import tqdm

from genshin.helper import Award, Helper
from genshin.models import Account
from src.local_config import cookies

iter = 0

progress = tqdm(cookies, desc=f"剩餘{len(cookies)}組帳號")
for cookie in progress:
    account = Account(cookies=cookie)

    helper = Helper(account=account)
    result = helper.run()

    # Failed to login
    if result["retcode"] != 0:
        logging.error(f"登入失敗，請重新綁定帳號！")

    # Failed to sign
    elif not result["data"]["is_sign"]:
        logging.error(f"簽到失敗！ 請通知作者！")

    # Successfully signed
    else:
        total_sign_day = result["data"]["total_sign_day"]
        award: Award = helper.awards[total_sign_day]

        logging.info(f"抽獎成功！\n獲得獎勵：{award.name} * {award.count}")
    iter += 1
    progress.set_description(f"剩餘{len(cookies) - iter}組帳號")
