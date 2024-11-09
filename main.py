import requests


def gpt(text):
    prompt = {
        "modelUri": "gpt://b1ghnehmnn3n3dvbqi90/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты - бот, отыгрывающий реального юзера. Ты будешь противником игрока, вы играете в традиционною драку яйцами на пасхую. Ты должен отыгрывать реального человека"
            },
            {
                "role": "assistant",
                "text": text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVNz9XUQGq4KhejXKZ-8PLoDVwLZrPGARRazGnK"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json().get('result')
    return result['alternatives'][0]['message']['text']


import telebot
import sqlite3
from random import randint

sqlite = sqlite3.connect('DataBase/EggsFightDB.sqlite', check_same_thread=False)
EggsFight = telebot.TeleBot('7133968318:AAFU9zjj133ywnVFeKdnUq0RFE127qMVd2I')
CommandList = {
    'create_room': 'Создать комнату',
    'quest_room': 'Ищет подходящую команту',
    'leave_room': 'Покинуть комнату',
    'rules': 'Правила игры',
    'start_fight': 'Начать игру (Только для создателя комнаты)'
}
RulesList = {
    '1': 'В чатах не материться',
    '2': 'Первый удар за присоединившимся. Второй за создателем комнаты'
}
PickRoomFlag = False
Rooms = []


@EggsFight.message_handler(commands=['start'])
def start(msg):
    cur = sqlite.cursor()
    res = f'SELECT * FROM Players WHERE PersID = {msg.from_user.id}'
    pers = cur.execute(res).fetchall()
    sqlite.commit()
    cur.close()
    if len(pers) == 0:
        cur = sqlite.cursor()
        res = f'INSERT INTO Players VALUES("{msg.from_user.first_name}", {msg.from_user.id})'
        cur.execute(res)
        sqlite.commit()
        cur.close()
        EggsFight.send_message(msg.chat.id, f'Урааа!!! Ты добавлен(-на) в базу! Нажми сюда --> /help (Пердупреждение!!! Не заходите в две комнаты сразу, и не создавайте комнату, если вступили в другую!!!)',
                               parse_mode='html')
    else:
        EggsFight.send_message(msg.chat.id, f'Урааа!!! Ты уже в базе! Нажми сюда --> /help (Пердупреждение!!! Не заходите в две комнаты сразу, и не создавайте комнату, если вступили в другую!!!)',
                               parse_mode='html')


@EggsFight.message_handler(commands=['help'])
def help(msg):
    for command in CommandList:
        EggsFight.send_message(msg.chat.id, f'/{command}: {CommandList[command]}', parse_mode='html')


@EggsFight.message_handler(commands=['rules'])
def rules(msg):
    for Rules in RulesList:
        EggsFight.send_message(msg.chat.id, f'{Rules}) {RulesList[Rules]}', parse_mode='html')


@EggsFight.message_handler(commands=['create_room'])
def create_room(msg):
    cur = sqlite.cursor()
    res = f'SELECT * FROM Players WHERE PersID = {msg.from_user.id}'
    pers = cur.execute(res).fetchall()
    sqlite.commit()
    cur.close()
    if len(pers) == 0:
        cur = sqlite.cursor()
        res = f'INSERT INTO Players VALUES("{msg.from_user.first_name}", {msg.from_user.id})'
        cur.execute(res)
        sqlite.commit()
        cur.close()
        EggsFight.send_message(msg.chat.id,
                               f'Урааа!!! Ты добавлен(-на) в базу! Нажми сюда --> /help (Пердупреждение!!! Не заходите в две комнаты сразу, и не создавайте комнату, если вступили в другую!!!)',
                               parse_mode='html')
    EggsFight.send_message(msg.chat.id, 'Создаем...', parse_mode='html')
    cur = sqlite.cursor()
    res = f'SELECT * FROM Rooms WHERE RoomCreater = "{msg.from_user.id}"'
    ProverkaRooms = cur.execute(res).fetchall()
    sqlite.commit()
    if len(ProverkaRooms) == 0:
        res = f'SELECT * FROM Rooms'
        RoomsList = cur.execute(res).fetchall()
        sqlite.commit()
        RoomsList = sorted(RoomsList)
        res = f'INSERT INTO Rooms VALUES({RoomsList[-1][0] + 1}, "{msg.from_user.id}", "")'
        cur.execute(res)
        sqlite.commit()
        cur.close()
        EggsFight.send_message(msg.chat.id, 'Успешно!', parse_mode='html')
    else:
        EggsFight.send_message(msg.chat.id, 'Вы уже в комнате!', parse_mode='html')


@EggsFight.message_handler(commands=['leave_room'])
def leave_room(msg):
    cur = sqlite.cursor()
    res = f'SELECT * FROM Players WHERE PersID = {msg.from_user.id}'
    pers = cur.execute(res).fetchall()
    sqlite.commit()
    cur.close()
    if len(pers) == 0:
        cur = sqlite.cursor()
        res = f'INSERT INTO Players VALUES("{msg.from_user.first_name}", {msg.from_user.id})'
        cur.execute(res)
        sqlite.commit()
        cur.close()
        EggsFight.send_message(msg.chat.id,
                               f'Урааа!!! Ты добавлен(-на) в базу! Нажми сюда --> /help (Пердупреждение!!! Не заходите в две комнаты сразу, и не создавайте комнату, если вступили в другую!!!)',
                               parse_mode='html')
    cur = sqlite.cursor()
    res = f'DELETE FROM Rooms WHERE RoomCreater = "{msg.from_user.id}"'
    cur.execute(res).fetchall()
    sqlite.commit()
    res = f'UPDATE Rooms SET RoomJoiner = "" WHERE RoomJoiner = "{msg.from_user.id}"'
    cur.execute(res).fetchall()
    sqlite.commit()
    cur.close()
    EggsFight.send_message(msg.chat.id, 'Успешно!', parse_mode='html')


@EggsFight.message_handler(commands=['quest_room'])
def quest_room(msg):
    cur = sqlite.cursor()
    res = f'SELECT * FROM Players WHERE PersID = {msg.from_user.id}'
    pers = cur.execute(res).fetchall()
    sqlite.commit()
    cur.close()
    if len(pers) == 0:
        cur = sqlite.cursor()
        res = f'INSERT INTO Players VALUES("{msg.from_user.first_name}", {msg.from_user.id})'
        cur.execute(res)
        sqlite.commit()
        cur.close()
        EggsFight.send_message(msg.chat.id,
                               f'Урааа!!! Ты добавлен(-на) в базу! Нажми сюда --> /help (Пердупреждение!!! Не заходите в две комнаты сразу, и не создавайте комнату, если вступили в другую!!!)',
                               parse_mode='html')
    global PickRoomFlag, Rooms
    EggsFight.send_message(msg.chat.id, 'Ищу...', parse_mode='html')
    cur = sqlite.cursor()
    res = f'SELECT * FROM Rooms'
    RoomsList = cur.execute(res).fetchall()
    sqlite.commit()
    cur.close()
    for Room in RoomsList:
        Rooms.append(Room)
        cur = sqlite.cursor()
        res = f'SELECT Name FROM Players WHERE PersID = {int(Room[1])}'
        Creater = cur.execute(res).fetchall()
        sqlite.commit()
        cur.close()
        EggsFight.send_message(msg.chat.id, f'Комната номер {Room[0]}.\nСоздатель: {Creater[0][0]}', parse_mode='html')
    cur = sqlite.cursor()
    res = f'SELECT * FROM Rooms WHERE RoomCreater = "{msg.from_user.id}" OR RoomJoiner = "{msg.from_user.id}"'
    ProverkaRooms = cur.execute(res).fetchall()
    sqlite.commit()
    if len(ProverkaRooms) == 0:
        EggsFight.send_message(msg.chat.id, 'Выберите комнату ', parse_mode='html')
        PickRoomFlag = True
    else:
        EggsFight.send_message(msg.chat.id, 'Вы уже в комнате!', parse_mode='html')


@EggsFight.message_handler(commands=['start_fight'])
def start_fight(msg):
    cur = sqlite.cursor()
    res = f'SELECT * FROM Players WHERE PersID = {msg.from_user.id}'
    pers = cur.execute(res).fetchall()
    sqlite.commit()
    cur.close()
    if len(pers) == 0:
        cur = sqlite.cursor()
        res = f'INSERT INTO Players VALUES("{msg.from_user.first_name}", {msg.from_user.id})'
        cur.execute(res)
        sqlite.commit()
        cur.close()
        EggsFight.send_message(msg.chat.id,
                               f'Урааа!!! Ты добавлен(-на) в базу! Нажми сюда --> /help (Пердупреждение!!! Не заходите в две комнаты сразу, и не создавайте комнату, если вступили в другую!!!)',
                               parse_mode='html')
    cur = sqlite.cursor()
    res = f'SELECT * FROM Rooms WHERE RoomCreater = {msg.from_user.id}'
    lst2 = cur.execute(res).fetchall()
    sqlite.commit()
    cur.close()
    Win1 = 0
    Win2 = 0
    if len(lst2) > 0:
        if lst2[0][2] != '':
            one = randint(1, 10)
            EggsFight.send_message(lst2[0][2], f'Вам выпало {one}', parse_mode='html')
            EggsFight.send_message(msg.chat.id, f'Сопернику выпало {one}', parse_mode='html')
            two = randint(1, 10)
            while two == one:
                two = randint(1, 10)
            EggsFight.send_message(lst2[0][2], f'Сопернику выпало {two}', parse_mode='html')
            EggsFight.send_message(msg.chat.id, f'Вам выпало {two}', parse_mode='html')
            if one > two:
                Win1 = 1
                EggsFight.send_message(lst2[0][2], f'Вы выиграли в первом раунде!', parse_mode='html')
                EggsFight.send_message(msg.chat.id, f'Вы проиграли в первом раунде!', parse_mode='html')
            else:
                Win1 = 2
                EggsFight.send_message(lst2[0][2], f'Вы проиграли в первом раунде!', parse_mode='html')
                EggsFight.send_message(msg.chat.id, f'Вы выиграли в первом раунде!', parse_mode='html')
            EggsFight.send_message(lst2[0][2], f'Второй раунд', parse_mode='html')
            EggsFight.send_message(msg.chat.id, f'Второй раунд', parse_mode='html')
            one = randint(1, 10)
            EggsFight.send_message(lst2[0][2], f'Сопернику выпало {one}', parse_mode='html')
            EggsFight.send_message(msg.chat.id, f'Вам выпало {one}', parse_mode='html')
            two = randint(1, 10)
            while two == one:
                two = randint(1, 10)
            EggsFight.send_message(lst2[0][2], f'Вам выпало {two}', parse_mode='html')
            EggsFight.send_message(msg.chat.id, f'Сопернику выпало {two}', parse_mode='html')
            if one > two:
                Win2 = 2
                EggsFight.send_message(lst2[0][2], f'Вы проиграли во втором раунде!', parse_mode='html')
                EggsFight.send_message(msg.chat.id, f'Вы выиграли во втором раунде!', parse_mode='html')
            else:
                Win2 = 1
                EggsFight.send_message(lst2[0][2], f'Вы выиграли во втором раунде!', parse_mode='html')
                EggsFight.send_message(msg.chat.id, f'Вы проиграли в втором раунде!', parse_mode='html')
            if Win1 + Win2 == 4:
                cur = sqlite.cursor()
                res = f'SELECT Name FROM Players WHERE PersID = {msg.from_user.id}'
                Winner = cur.execute(res).fetchall()
                sqlite.commit()
                cur.close()
                EggsFight.send_message(lst2[0][2], f'{Winner[0][0]} выиграл!', parse_mode='html')
                EggsFight.send_message(msg.chat.id, f'{Winner[0][0]} выиграл!', parse_mode='html')
            elif Win1 + Win2 == 2:
                cur = sqlite.cursor()
                res = f'SELECT Name FROM Players WHERE PersID = {lst2[0][2]}'
                Winner = cur.execute(res).fetchall()
                sqlite.commit()
                cur.close()
                EggsFight.send_message(lst2[0][2], f'{Winner[0][0]} выиграл!', parse_mode='html')
                EggsFight.send_message(msg.chat.id, f'{Winner[0][0]} выиграл!', parse_mode='html')
            else:
                EggsFight.send_message(lst2[0][2], f'Ничья!', parse_mode='html')
                EggsFight.send_message(msg.chat.id, f'Ничья!', parse_mode='html')


@EggsFight.message_handler()
def LeftMSG(msg):
    global PickRoomFlag, Rooms
    cur = sqlite.cursor()
    res = f'SELECT * FROM Rooms WHERE RoomCreater = "{msg.from_user.id}" OR RoomJoiner = "{msg.from_user.id}"'
    ProverkaRooms = cur.execute(res).fetchall()
    sqlite.commit()
    if len(ProverkaRooms) != 0:
        if str(msg.from_user.id) != ProverkaRooms[0][2]:
            EggsFight.send_message(ProverkaRooms[0][2], f'{msg.from_user.first_name}: {msg.text}', parse_mode='html')
        else:
            EggsFight.send_message(ProverkaRooms[0][1], f'{msg.from_user.first_name}: {msg.text}', parse_mode='html')
    if PickRoomFlag:
        try:
            cur = sqlite.cursor()
            res = f'SELECT * FROM Rooms WHERE RoomID = {int(msg.text)}'
            Pers = cur.execute(res).fetchall()
            sqlite.commit()
            if Pers[0][2] == '':
                res = f'UPDATE Rooms SET RoomJoiner = {msg.from_user.id} WHERE RoomID = {int(msg.text)}'
                cur.execute(res).fetchall()
                sqlite.commit()
                res = f'SELECT * FROM Rooms'
                lst = cur.execute(res).fetchall()
                sqlite.commit()
                cur.close()
                cur = sqlite.cursor()
                res = f'SELECT * FROM Players WHERE PersID = {msg.from_user.id}'
                lst2 = cur.execute(res).fetchall()
                sqlite.commit()
                cur.close()
                PickRoomFlag = False
                EggsFight.send_message(msg.chat.id, 'Успешно!', parse_mode='html')
                EggsFight.send_message(int(lst[0][1]), f'К вам присоединился игрок {lst2[0][0]}!', parse_mode='html')
            else:
                EggsFight.send_message(msg.chat.id, 'Нет места!', parse_mode='html')
        except ValueError:
            EggsFight.send_message(msg.chat.id, 'Нужно ввести только номер комнаты. Попробуй еще', parse_mode='html')
            PickRoomFlag = True


EggsFight.polling(none_stop=True)
