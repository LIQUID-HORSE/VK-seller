import os
import time
import vk_api
from config_all import tokens
from funcs import former_post, send_post, captcha_handler


def post_multiple():
    inp = input('''Куда публикуем?
    1. Тестовый
    2. СтонСипи
    3. Адидас/кроссы
    4. Викенд
    5. Кархартт
    :''')

    for filename in os.listdir("group_id's"):
        if filename.startswith(inp):
            with open(f"group_id's/{filename}", "r") as f:
                groups = [line.strip() for line in f.readlines()]

    used_files = set()
    i = 0
    inp = int(input('''С кого публикуем?
    1. Варвар
    2. Авеню
    3. Погиб
    4. Вся братва
    :'''))
    while True:
        if inp == 4:
            token = tokens[i % len(tokens)]
        else:
            token = tokens[inp - 1]
        i += 1

        vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
        vk = vk_session.get_api()
        upload = vk_api.VkUpload(vk_session)
        directory = "photo"
        post_text = ''
        attachments = []

        for filename in os.listdir(directory):
            if filename not in used_files:
                ret = former_post(directory, upload, filename)
                post_text = ret[0]
                attachments = ret[1]
                used_files.add(filename)
                break

        if post_text:
            count = 0
            for group_id in groups:
                try:
                    count += 1
                    time.sleep(1)
                    vk.wall.post(
                        owner_id=group_id,
                        from_group=0,
                        message=post_text,
                        attachments=','.join(attachments),
                        signed=1,
                        captcha_handler=captcha_handler
                    )
                    if count % 10 == 0:
                        print(f"Задержка 5 секунд после публикации в паблике {group_id}")
                        time.sleep(5)
                except vk_api.exceptions.ApiError:
                    print(f"Ошибка! Стена закрыта или схлопотали банчик )0)): {group_id}")
                    time.sleep(10)
            time.sleep(5)
        else:
            break


if __name__ == '__main__':
    post_multiple()
