import vk_api
from config_vova import token


def get_all_items(vk, owner_id: str):
    items = []
    offset = 0
    count = 200

    while True:
        response = vk.market.get(owner_id=owner_id, count=count, offset=offset)
        items.extend(response['items'])
        if offset + count >= response['count']:
            break
        offset += count

    return items


def delete_all_items(vk, owner_id: str):
    items = get_all_items(vk, owner_id)
    for item in items:
        item_id = item['id']
        vk.market.delete(owner_id=owner_id, item_id=item_id)
        print(f"Товар с ID {item_id} удалён")


def main():
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    group = "-219933668"    # test
    delete_all_items(vk, group)


if __name__ == '__main__':
    main()
