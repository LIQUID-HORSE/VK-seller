import vk_api
from config_brand_avenue import token


def get_group_id(screen_name):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    screen_name = screen_name.replace('https://vk.com/public', '')
    group = vk.utils.resolveScreenName(screen_name=screen_name)
    if group['type'] == 'group':
        return group['object_id']
    return None


def main():
    input_file = "group_id's/simple_links.txt"
    with open(input_file, "r") as groups_file:
        groups = [line.strip() for line in groups_file.readlines()]

    for group in groups:
        group_id = get_group_id(group)
        if group_id:
            print('-' + str(group_id))
        else:
            print(f"Не удалось определить id для {group}")


if __name__ == '__main__':
    main()
