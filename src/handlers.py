import os
import asyncio
import logging
import requests
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

import keyboard as kb
from output import print_info
from data.orm import upd_token, get_token

router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



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


@router.message(F.text == 'Отправить')
async def get_group_id_and_domain(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    domains = read_domains_from_file()
    if not domains:
        await message.answer("Нет доменов для обработки")
        return

    data_g = await state.get_data()
    processed_domains = []

    try:
        await upd_token(session)
        access_token = await get_token(session)

        for domain in domains:
            try:
                response = requests.get(
                    "https://api.vk.com/method/groups.getById",
                    params={
                        "access_token": access_token,
                        "v": data_g['v'],
                        "group_id": domain,
                    }
                )

                if 'response' not in response.json():
                    continue

                dom = response.json()['response']['groups'][0]['screen_name']
                processed_domains.append(dom)
            except Exception as e:
                logger.error(f"Ошибка обработки домена {domain}: {e}")

        if not processed_domains:
            await message.answer("Не удалось обработать домены")
            return

        await state.update_data(domains=processed_domains)
        await message.answer(f'Будут обработаны: {", ".join(processed_domains)}')
        await state.set_state(RequestPars.count)
        await message.answer("Введите количество комментариев")

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


@router.message(RequestPars.count)
async def get_count(message: Message, state: FSMContext):
    await state.update_data(count=int(message.text))
    await state.set_state(RequestPars.offset)
    await message.answer("Введите смещение (Что бы не потерять данные, напишите 0)")


@router.message(RequestPars.offset)
async def get_offset_and_pars(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(offset=int(message.text))
    data_req = await state.get_data()
    domains = data_req.get('domains', [])

    try:
        await upd_token(session)
        access_token = await get_token(session)

        if not domains:
            await message.answer("Нет доменов для обработки")
            return

        await message.answer(f"⏳ Обработка {len(domains)} групп...")
        total_posts = 0

        for domain in domains:
            try:
                offset = data_req['offset']
                count = data_req['count']
                batch_size = 99

                while offset < count:
                    current_count = min(batch_size, count - offset)

                    response = requests.get(
                        'https://api.vk.com/method/wall.search',
                        params={
                            'access_token': access_token,
                            'v': data_req['v'],
                            'query': data_req['query'],
                            'domain': domain,
                            'count': current_count,
                            'offset': offset,
                        }
                    )

                    if 'response' not in response.json():
                        break

                    data = response.json()['response']['items']
                    offset += len(data)

                    # Обработка и вывод результатов
                    gi = await print_info(data=data)
                    for i in range(0, len(gi), 10):
                        await message.answer('\n'.join(gi[i:i + 10]))
                        await asyncio.sleep(1)

                    await asyncio.sleep(0.3)

                total_posts += offset - data_req['offset']
                await message.answer(f"✅ {domain}: {offset - data_req['offset']} постов")

            except Exception as e:
                logger.error(f"Ошибка обработки {domain}: {e}")
                await message.answer(f"Ошибка в {domain}")

        await message.answer(f"🏁 Всего постов: {total_posts}")
        await state.clear()

    except Exception as e:
        await message.answer(f"Критическая ошибка: {str(e)}")