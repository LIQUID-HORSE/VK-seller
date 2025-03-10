import os
import vk_api
from config_all import tokens, walls
from funcs import former_post, send_post, captcha_handler


def post_to_wall(token, wall):
    vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    directory = "photo"

    for filename in os.listdir(directory):
        ret = former_post(directory, upload, filename)
        post_text = ret[4]
        attachments = ret[1]
        send_post(vk, wall, post_text, attachments)


def main():
    quantity = len(tokens)
    for i in range(quantity):
        token = tokens[i]
        wall = walls[i]
        post_to_wall(token, wall)


if __name__ == '__main__':
    main()
