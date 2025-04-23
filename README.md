# Парсер комментариев и постов ВКонтакте

Парсер для сбора новых комментариев и постов из ВКонтакте через API с последующей отправкой в Telegram-бота.

## 📌 Основная функциональность

1. **Парсинг сообществ ВК** с возможностью:
   - Уникализации запросов (добавление символов `@*':!?`)
   - Фильтрации данных

2. **Отправка результатов в Telegram-бота** с детализацией:
   - 🔗 Ссылка на комментарий
   - ⏳ Время написания
   - 👤 Ссылка на автора комментария

## 🔑 Получение access_token

### Шаг 1: Создание приложения в VK-ID
1. Перейдите в [VK Developers](https://vk.com/dev)
2. Создайте новое веб-приложение

![Создание приложения](https://github.com/user-attachments/assets/6e4dcd53-4360-4c65-9b6b-7b72cc233ffb)  
*Рис. 1.1 - Создание приложения*

![Настройки приложения](https://github.com/user-attachments/assets/01521bbe-4a8c-455a-979e-7e821d466813)  
*Рис. 1.2 - ID приложения*

### Шаг 2: Настройка авторизации
Обязательно включите настройки авторизации:

![Настройки авторизации](https://github.com/user-attachments/assets/7850a3d5-73f7-4f40-b373-25742397c811)

### Шаг 3: Получение кода авторизации
Отправьте GET-запрос в браузере (замените параметры на свои):
https://id.vk.com/authorize?
response_type=code&
client_id=ВАШ_APP_ID&
scope=vkid.personal_info&
redirect_uri=https://oauth.vk.com/blank.html&
state=XXXRaXXXxxsssssssXXXsdaXXXXssXXXXXXXXXXXXXndomZZZ&
code_challenge=СГЕНЕРИРОВАННЫЙ_КОД&
code_challenge_method=S256


Где:
- `client_id` - ID вашего приложения (из Рис. 1.2)
- `code_challenge` - сгенерируйте на [PKCE Generator](https://tonyxu-io.github.io/pkce-generator/)

### Шаг 4: Получение токена через Postman
Используйте полученный код для запроса токена:

![Запрос токена](https://github.com/user-attachments/assets/82531c49-8cd9-4ada-9831-f18d0631cf22)


### Шаг 5: Заполнение статических данных в папке с кодом (Для автоматического обновления токена)
Возьмите полученные данные из postman 

![image](https://github.com/user-attachments/assets/3901eba8-4812-4a69-90ec-a1f83da6baa3)


## 🤖 Работа бота

### Примеры работы:

![Пример 1](https://github.com/user-attachments/assets/2ba74486-4dc9-42b6-b39c-b678e3697fb4)

![Пример 2](https://github.com/user-attachments/assets/9e4d3235-6916-40ce-961c-2c18a42799d8)

![Пример 3](https://github.com/user-attachments/assets/80af5ee1-9ee6-459f-bf89-447850af0c86)
