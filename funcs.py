import os
import time
import pandas as pd
import vk_api


def captcha_handler(captcha):
    key = input(f"Введите код капчи {captcha.get_url()}: ").strip()
    return captcha.try_again(key)


def former_post(directory: str, upload, folder_name: str):
    post_text = "post_text"
    prod_text = "prod_text"
    name = "name"
    price = "price"
    post_images = []

    folder_path = os.path.join(directory, folder_name)
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.endswith('post.txt'):
            with open(item_path, "r", encoding='utf-8') as file:
                post_text = file.read()
        elif item.lower().endswith(('.jpeg', '.jpg', '.png', '.heic')):
            post_images.append(item_path)
            print("Найдено изображение:", item_path)
        elif item.endswith('.csv'):
            info = pd.read_csv(item_path, sep=',')
            name = info['name'][0]
            price = info['price'][0]
        elif os.path.isfile(item_path) and item.endswith('prod.txt'):
            with open(item_path, "r", encoding='utf-8') as file:
                prod_text = file.read()

    attachments = []
    print("Изображения для загрузки:", post_images)

    if post_images:
        photos = upload.photo_wall(post_images)
        for photo in photos:
            attachments.append(f"photo{photo['owner_id']}_{photo['id']}")

    print('\n')
    return [post_text, attachments, name, price, prod_text]


def former_market(directory: str, upload, folder_name: str, group: str):
    post_images = []
    prod_text = "prod_text"
    name = "name"
    price = "price"
    folder_path = os.path.join(directory, folder_name)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.endswith('prod.txt'):
            with open(item_path, "r", encoding='utf-8') as file:
                prod_text = file.read()
        elif item.lower().endswith(('.jpeg', '.jpg', '.png')):
            post_images.append(item_path)
            print("Найдено изображение:", item_path)
        elif item.endswith('.csv'):
            info = pd.read_csv(item_path, sep=',')
            name = info['name'][0]
            price = info['price'][0]

    photos = upload.photo_market(post_images, int(group[1:]))
    attachments = []
    photo_ids = []
    for photo in photos:
        photo_id_str = f"market{photo['owner_id']}_{photo['id']}"
        attachments.append(photo_id_str)
        photo_ids.append(photo['id'])

    return [prod_text, photo_ids, name, price]


def send_post(vk, wall: str, post_text: str, attachments: list):
    try:
        time.sleep(1)
        vk.wall.post(
            owner_id=wall,
            from_group=0,
            message=post_text,
            attachments=','.join(attachments),
            signed=1,
            captcha_handler=captcha_handler
        )
    except vk_api.exceptions.ApiError:
        print(f"Ошибка! Возможно стена закрыта {wall}")
        time.sleep(10)


def send_market(vk, group: str, prod_text: str, attachments: list, name: str, price: str):
    try:
        time.sleep(1)
        if len(attachments) > 5:
            attachments = attachments[:4]
        vk.market.add(
            owner_id=group,
            name=name,
            price=price,
            category_id=10000,
            description=prod_text,
            main_photo_id=attachments[0],
            photo_ids=attachments[1:]
        )
    except vk_api.exceptions.ApiError:
        print(f"Ошибка при публикации товара для группы {group}")
        time.sleep(10)
