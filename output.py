from datetime import datetime


async def print_info(data, query):
    res = []
    for post in data:
        clean_query = query.replace(' ', '')
        res.append(f"Время: {datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S')}   "
                   f"Автор: https://vk.com/id{post['from_id']}    "
                   f"Ссылка на комментарий: https://vk.com/wall{post['owner_id']}?q={clean_query}&w=wall{post['owner_id']}_{post['id']}_r{post['id']}    "
                   f""
                   f"---------------------------------------------------------------------------------------------------")


    return res


