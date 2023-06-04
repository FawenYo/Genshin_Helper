from tqdm import tqdm

from src.local_config import cookies
from src.utils.genshin_models import Account, Award
from src.utils.helper import Helper
from src.utils.logging_util import get_logger

logger = get_logger()

iter = 0

progress = tqdm(cookies, desc=f"剩餘{len(cookies)}組帳號")
for cookie in progress:
    account = Account(cookies=cookie)

    helper = Helper(account=account)
    result = helper.run()

    # Failed to login
    if result["retcode"] != 0:
        logger.error(f"登入失敗，請重新綁定帳號！")

    # Failed to sign
    elif not result["data"]["is_sign"]:
        logger.error(f"簽到失敗！ 請通知作者！")

    # Successfully signed
    else:
        total_sign_day = result["data"]["total_sign_day"]
        award: Award = helper.awards[total_sign_day]

        logger.info(f"抽獎成功！\n獲得獎勵：{award.name} * {award.count}")
    iter += 1
    progress.set_description(f"剩餘{len(cookies) - iter}組帳號")
