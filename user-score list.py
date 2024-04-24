import pymysql

def generate_interaction_list(user_id):
    connection = pymysql.connect(
        host='your_host',
        user='your_username',
        password='your_password',
        database='your_database',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT fid FROM collect WHERE user_id = %s", (user_id,))
            collect_records = cursor.fetchall()

            cursor.execute("SELECT id FROM orders WHERE user_id = %s", (user_id,))
            purchase_records = cursor.fetchall()

    finally:
        connection.close()

    total_number_of_products = 4  # 假设有4个商品

    interaction_list = [0] * total_number_of_products

    for record in collect_records:
        fid = record['fid']
        if fid <= total_number_of_products:
            interaction_list[fid - 1] = 1  # 收藏的互动分数是1

    for record in purchase_records:
        order_id = record['id']
        if order_id <= total_number_of_products:
            # 如果之前已经收藏过，则互动分数为2，否则为1
            if interaction_list[order_id - 1] == 1:
                interaction_list[order_id - 1] = 2
            else:
                interaction_list[order_id - 1] = 1  # 购买的互动分数是1

    return interaction_list

def generate_all_users_interaction_list():
    connection = pymysql.connect(
        host='your_host',
        user='your_username',
        password='your_password',
        database='your_database',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT user_id FROM collect")
            user_ids = [record['user_id'] for record in cursor.fetchall()]

    finally:
        connection.close()

    all_users_interaction_list = []

    for user_id in user_ids:
        user_interaction_list = generate_interaction_list(user_id)
        all_users_interaction_list.append(user_interaction_list)

    return all_users_interaction_list

# 示例调用
all_users_interaction_list = generate_all_users_interaction_list()
for idx, user_interaction_list in enumerate(all_users_interaction_list, start=1):
    print(f"User {idx}: {user_interaction_list}")
