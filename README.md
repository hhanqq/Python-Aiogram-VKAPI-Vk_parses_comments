
Парсер новых комментариев, постов ВКонтакте через запросы.

Задача:
1) Парсить базу сообществ вк 
2) Во время парса, нужно уникализировать запрос добавлением символа "@"*':!?
3) Результат парса отправлять в тг бота
4) В результате указывать: 
- ссылка на комментарий
- время написания
- ссылка на автора комментария




Для получения access_token нужно создать web-приложения в VK-ID


![image](https://github.com/user-attachments/assets/c6e10867-3f4e-4aa4-8d07-a5bfe3886920)

Рисунок 1.1

Далее


![image](https://github.com/user-attachments/assets/01521bbe-4a8c-455a-979e-7e821d466813)


Рисунок 1.2

Обязательная настройка авторизации


![image](https://github.com/user-attachments/assets/7850a3d5-73f7-4f40-b373-25742397c811)


Далее нужно отправить POST зарпрос по ссылке (Просто вставляете в браузер, далее из URL вытаскиваете данные и вставляете в POSTMAN):
https://id.vk.com/authorize?
response_type=code&
client_id=53455195& // АЙДИ ВАШЕГО ПРИЛОЖЕНИЯ ИЗ РИСУНКА 1.2
scope=vkid.personal_info&
redirect_uri=https://oauth.vk.com/blank.html&
state=XXXRaXXXxxsssssssXXXsdaXXXXssXXXXXXXXXXXXXndomZZZ& // рандомная строка для сравнения с ответом (можно оставить так же)
code_challenge=cLjsp8BxW2YA5NJC5QJAPfdmyG6kMQdkb-ZkYkXT4vw& // для генерации использовать - https://tonyxu-io.github.io/pkce-generator/
code_challenge_method=S256

Следующий шаг с POSTMAN
![image](https://github.com/user-attachments/assets/4810d638-e1b3-435e-ad1b-0ac11a798c3b)

Ура! Вы получили access_token для использования бота.
Далее по истечению часа нужно его обновить, просто создаете такой запрос и вставляете в него refresh_token
![image](https://github.com/user-attachments/assets/ce5587f7-f707-46e3-8b96-0ed6645e3750)




Работа бота

![image](https://github.com/user-attachments/assets/2ba74486-4dc9-42b6-b39c-b678e3697fb4)



![image](https://github.com/user-attachments/assets/9e4d3235-6916-40ce-961c-2c18a42799d8)



![image](https://github.com/user-attachments/assets/80af5ee1-9ee6-459f-bf89-447850af0c86)


