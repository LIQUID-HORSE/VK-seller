import time
import vk_api
from config_pogib import token


def captcha_handler(captcha):
    key = input(f"Введите код капчи {captcha.get_url()}: ").strip()
    return captcha.try_again(key)


def delete_suggested_posts(vk, group_id: str):
    try:
        proposed_posts = vk.wall.get(group_id=group_id, filter='suggests', owner_id=group_id)
        for post in proposed_posts['items']:
            post_id = post['id']
            vk.wall.delete(owner_id=group_id, post_id=post_id)
            print(f"Предложенная запись с id {post_id} удалена для группы {group_id}")
    except vk_api.exceptions.ApiError:
        print(f"Ошибка! Возможно стена закрыта {group_id}")
        time.sleep(10)
    except vk_api.exceptions.Captcha:
        print("Ошибка обработки капчи")
        time.sleep(15)


def main():
    vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
    vk = vk_session.get_api()

    with open("group_id's/1-group_id.txt", "r") as f:
        groups = [line.strip() for line in f.readlines()]

    for group_id in groups:
        delete_suggested_posts(vk, group_id)


if __name__ == '__main__':
    main()
