import vk
import requests
import json
import time
from flask import Flask as fl

app = fl(__name__)

@app.route('/')

def refresh_lp(vkapi):
    # Запрашиваем параметры подключения
    return vkapi.messages.getLongPollServer()
def main():
    session = vk.Session( '64539d85290a5d7f2bd416abe68d12e626efbf1eb275c51643b02751130c917190a717638ed758c9ba1fa')
    vk = vk.API(session, v='5.38')

    lp = refresh_lp(vkapi)

    ts = lp['ts']

    while True:
        # Шаблон строки запроса
        req = 'https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=2'
        # Заполненная строка запроса с параметрами подключения
        req = req.format(server=lp['server'], key=lp['key'], ts=ts)
        # print(ts)
        # Выполнение запроса
        get = requests.get(req)

        # Загрузка ответа в виде объекта
        try:
            response = json.loads(get.text)
        except:
            time.sleep(1)
            continue

        if not response:
            time.sleep(1)
            continue

        if response.get('failed') and response['failed'] == 2:
            lp = refresh_lp(vkapi)
            time.sleep(1)
            continue

        ts = response['ts']

        if not response.get('updates'):
            lp = refresh_lp(vkapi)
            time.sleep(1)
            continue

        # Обработка всех обновлений
        for update in response['updates']:
            # Селектор типа события
            msgid = update [0]
            if msgid == 4: # Отправлено новое сообщение
                messageid = update[1]
                flags = update[2]
                peer_id = update[3]
                timestamp = update[4]
                text = update[5]
                # надо проверить флаг
                if (flags & 2) == 0:
                    # Сообщение отправлено не самим ботом (флаг 2 установлен)
                    # Добавлено новое сообщение
                    try:
                        print ('Добавлено новое сообщение: {flags} {text}'.format(flags=flags,text=text))
                        mes = 'HEllo'
                        # Отправка ответа
                    except:
                        mes = 'Не используйте смайлики и другие специальные символы'
                    try:
                        vkapi.messages.send (user_id = peer_id, message=mes)
                    except:
                        continue

        # Задержка на одну секунду
        time.sleep(1)
if __name__ == '__main__':
    main()
