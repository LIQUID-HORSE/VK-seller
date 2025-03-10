import time
import vk_api
from config_boris import token


def captcha_handler(captcha):
    key = input(f"Введите код капчи {captcha.get_url()}: ").strip()
    return captcha.try_again(key)


def main():
    vk_session = vk_api.VkApi(token=token)
    try:
        vk = vk_session.get_api()
    except vk_api.AuthError as error_msg:
        print("Ошибка авторизации:", error_msg)
        return

    with open("group_id's/followers.txt", "r") as file:
        groups = [line.strip() for line in file.readlines()]

    for group_id in groups:
        try:
            response = vk.groups.join(group_id=group_id[1:], captcha_handler=captcha_handler)
            print(f"Подписка выполнена: {response} для группы {group_id}")
            time.sleep(5)
        except vk_api.exceptions.ApiError:
            print(f"Уже подписан или ошибка в группе {group_id}")
            time.sleep(5)
        except vk_api.exceptions.Captcha:
            print("Капча не обработана")
            time.sleep(20)


if __name__ == '__main__':
    main()
