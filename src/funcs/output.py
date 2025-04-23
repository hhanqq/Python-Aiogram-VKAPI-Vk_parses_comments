from datetime import datetime
from typing import List


async def print_info(data):
    res: List[str] = []
    for post in data:
        try:
            time_str = datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S')
            author_link = f"https://vk.com/id{post['from_id']}"

            if post.get('post_type') == 'reply':
                # Это комментарий
                post_link = f"https://vk.com/wall{post['owner_id']}_{post['post_id']}?reply={post['id']}"
            else:
                # Это обычный пост
                post_link = f"https://vk.com/wall{post['owner_id']}_{post['id']}"

            res.append(
                f"Время: {time_str}   "
                f"Автор: {author_link}    "
                f"Ссылка: {post_link}\n"
                f"---------------------------------------------------------------------------------------------------"
            )
        except KeyError as e:
            error_msg = f"Ошибка обработки поста: отсутствует ключ {str(e)}"
            res.append(error_msg)
            print(f"{error_msg}. Полный пост: {post}")

    return res