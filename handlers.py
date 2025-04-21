import os
import asyncio
import requests
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import keyboard as kb
from output import print_info

router = Router()


class RequestPars(StatesGroup):
    access_token = State()
    v = State()  # Версия API VK
    query = State()  # Запрос
    domain = State()  # Группа VK
    count = State()  # Кол-во постов в пачке
    offset = State()  # Смещение


def read_domains_from_file():
    domains = []
    file_path = os.path.join(os.path.dirname(__file__), 'domains.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            domains = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return domains


@router.message(CommandStart())
async def send_hello_msg(message: Message):
    await message.reply('Привет!', reply_markup=kb.main)


@router.message(F.text == "Ввести данные 📝")
async def get_information(message: Message, state: FSMContext):
    await state.set_state(RequestPars.access_token)
    await message.answer("Введите ваш access token")


@router.message(RequestPars.access_token)
async def get_access_token(message: Message, state: FSMContext):
    await state.update_data(access_token=message.text)
    await state.set_state(RequestPars.v)
    await message.answer(
        "Введите актуальную версию API ВК. Её можно узнать по ссылке: https://dev.vk.com/ru/reference/versions"
    )


@router.message(RequestPars.v)
async def get_v(message: Message, state: FSMContext):
    await state.update_data(v=float(message.text))
    await state.set_state(RequestPars.query)
    await message.answer("Введите ваш запрос для поиска")


@router.message(RequestPars.query)
async def get_query(message: Message, state: FSMContext):
    await state.update_data(query=message.text)
    await state.set_state(RequestPars.domain)

    domains = read_domains_from_file()
    await message.answer(
        f'Найдены домены в файле: {", ".join(domains)}\n'
        'Нажмите "Отправить" для использования доменов из файла',
        reply_markup=kb.send
    )



@router.message(F.text=='Отправить')
async def get_group_id_and_domain(message: Message, state: FSMContext):
    domains = read_domains_from_file()


    if not domains:
        await message.answer("Не указано ни одного домена для обработки")
        return

    data_g = await state.get_data()
    processed_domains = []

    for domain in domains:
        try:
            response = requests.get(
                "https://api.vk.com/method/groups.getById",
                params={
                    "access_token": data_g['access_token'],
                    "v": data_g['v'],
                    "group_id": domain,
                }
            )

            if 'response' not in response.json():
                await message.answer(f"Ошибка при получении данных группы {domain}")
                continue

            dom = response.json()['response']['groups'][0]['screen_name']
            processed_domains.append(dom)

        except Exception as e:
            await message.answer(f"Ошибка обработки домена {domain}: {str(e)}")

    if not processed_domains:
        await message.answer("Не удалось обработать ни один домен")
        return

    await state.update_data(domains=processed_domains)
    await message.answer(f'🔍 Будут обработаны группы: {", ".join(processed_domains)}')
    await state.set_state(RequestPars.count)
    await message.answer("Введите кол-во комментариев для каждой группы")


@router.message(RequestPars.count)
async def get_count(message: Message, state: FSMContext):
    await state.update_data(count=int(message.text))
    await state.set_state(RequestPars.offset)
    await message.answer("Введите смещение (Что бы не потерять данные, напишите 0)")


@router.message(RequestPars.offset)
async def get_offset_and_pars(message: Message, state: FSMContext):
    await state.update_data(offset=int(message.text))
    data_req = await state.get_data()
    domains = data_req.get('domains', [])

    if not domains:
        await message.answer("Нет доменов для обработки")
        return

    await message.answer(f"⏳ Начинаю обработку {len(domains)} групп...")

    total_posts = 0
    offset = int(data_req['offset'])
    count = int(data_req['count'])
    pachka = 99  # Максимальное количество постов за один запрос

    for domain in domains:
        try:
            await message.answer(f"🔍 Обрабатываю группу: {domain}")
            all_posts = []
            current_offset = offset

            while current_offset < count:
                current_count = min(pachka, count - current_offset)

                response = requests.get(
                    'https://api.vk.com/method/wall.search',
                    params={
                        'access_token': str(data_req['access_token']),
                        'v': float(data_req['v']),
                        'query': str(data_req['query']),
                        'domain': domain,
                        'count': current_count,
                        'offset': current_offset,
                    }
                )

                if 'response' not in response.json():
                    await message.answer(f"Ошибка при запросе для группы {domain}")
                    break

                data = response.json()['response']['items']
                all_posts.extend(data)
                current_offset += len(data)

                # Отправка результатов пачками
                gi = await print_info(data=data)
                for i in range(0, len(gi), 10):
                    batch = gi[i:i + 10]
                    await message.answer('\n'.join(batch))
                    await asyncio.sleep(1)

                await asyncio.sleep(0.3)

            total_posts += len(all_posts)
            await message.answer(f"✅ Группа {domain} обработана. Найдено постов: {len(all_posts)}")

        except Exception as e:
            await message.answer(f"Ошибка при обработке группы {domain}: {str(e)}")

    await message.answer(f"🏁 Все группы обработаны. Всего найдено постов: {total_posts}")
    await state.clear()