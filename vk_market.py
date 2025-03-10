import os
import vk_api
from config_vova import token
from funcs import former_market, send_market, captcha_handler


def post_to_market():
    group = "-219933668"    # test
    vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    directory = "next"

    for filename in os.listdir(directory):
        ret = former_market(directory, upload, filename, group)
        prod_text, attachments, name, price = ret
        send_market(vk, group, prod_text, attachments, name, price)


if __name__ == '__main__':
    post_to_market()
