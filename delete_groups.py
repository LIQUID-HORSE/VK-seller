def remove_deleted_groups():
    delete_file_path = "group_id's/delete.txt"
    group_id_path = "group_id's/group_id_adidas.txt"
    group_links_path = "group_id's/group_links_adidas.txt"

    with open(delete_file_path, 'r') as f:
        delete_ids = f.readlines()

    with open(group_id_path, 'r') as f:
        group_ids = f.readlines()

    print(f"Всего id для удаления: {len(delete_ids)}")
    print(f"Исходное количество group id: {len(group_ids)} -> {group_ids}")

    filtered_ids = [gid for gid in group_ids if gid not in delete_ids]
    print(f"Количество group id после фильтрации: {len(filtered_ids)} -> {filtered_ids}")

    with open(group_links_path, 'w') as f:
        f.writelines(filtered_ids)

    formatted_ids = ['-' + gid[21:].strip() + "\n" for gid in filtered_ids]
    print("Отформатированные group id:", formatted_ids)

    with open(group_id_path, 'w') as f:
        f.writelines(formatted_ids)


if __name__ == '__main__':
    remove_deleted_groups()
