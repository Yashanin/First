# Лабораторная работа №6
# Задание
# Реализуйте следующее Web приложение на фреймворке Flask
# 1) создайте базу данных на движке SQLite при помощи Python, состоящей из одной таблицы
# и заполните ее вашими данными (не менее 10 строк),
# Таблицу можете выбрать любой тематики, например какие подарки необходимо купить
# родным / коллегам на Новый Год. Указать ФИО, название подарка, стоимость и статус
# (куплен / не куплен)
# Проверьте наличие данных в вашей таблице написав SQL запрос через Python
# SELECT * FROM ваша_таблица
# 2) возьмите файл базы данных созданной в задании 1) и выведите содержимое таблицы в
# HTML форме, используя Flask фреймворк и вызов GET запроса через браузер
# Пример вывода таблицы
# ФИО Подарок Стоимость Статус
# Иван Иванович Санки 2000 куплен
# Ирина Сергеевна Цветы 3000 не куплен
# … … … …
from pprint import pprint
import sqlite3
import pandas as pd
from flask import Flask

print('''\t   Домашнее задание №6
    SQLite, Flask \n''')

dict_routers = {
    'Имя': ['Маршрутизатор ME5210S', 'Маршрутизатор ESR-1511', 'Маршрутизатор ESR-21-H',
            'Маршрутизатор ESR-20-H', 'Маршрутизатор ESR-1511-H', 'Маршрутизатор ME5100',
            'Маршрутизатор ME5000', 'Маршрутизатор ESR-31', 'Маршрутизатор ESR-15VF',
            'Маршрутизатор ESR-30', 'Маршрутизатор ESR-15', 'Маршрутизатор ESR-3300',
            'Маршрутизатор ESR-3200L', 'Маршрутизатор ESR-30-H', 'Маршрутизатор ESR-3200-H',
            'Маршрутизатор cisco', 'Коммутатор huawei', 'Экран juniper'],
    'Name': ['MPLS router ME5210S', 'Service router ESR-1511', 'Service router ESR-21-H',
             'Service router ESR-20-H', 'Service router ESR-1511-H', 'router',
             'ME5000 router', 'Service router ESR-31', 'ESR-15VF service routers',
             'Service router ESR-30', 'ESR-15 service router', 'Service router ESR-3300',
             'Router ESR-3200L', 'Service router ESR-30-H', 'Service router ESR-3200-H',
             'Router cisco', 'Switch huawei', 'Firewall juniper'],
    'Единица': ['Штука', 'Штука', 'Штука', 'Штука', 'Штука',
               'Штука', 'Штука', 'Штука', 'Штука', 'Штука',
               'Штука', 'Штука', 'Штука', 'Штука', 'Штука',
                'Штука', 'Штука', 'Штука'],
    'vendor': ['eltex', 'eltex', 'eltex', 'eltex', 'eltex', 'eltex', 'eltex', 'eltex', 'eltex', 'eltex', 'eltex',
               'eltex', 'eltex', 'eltex', 'eltex','cisco', 'huawei', 'juniper'],
    'Предприятие': ['"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"',
                    '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"',
                    '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"',
                    '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"',
                    '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"', '"ООО "ПРЕДПРИЯТИЕ "ЭЛТЕКС"',
                    'Cisco', 'Huawei', 'Juniper'],
    'ИНН': [5410108110, 5410108110, 5410108110, 5410108110, 5410108110, 5410108110, 5410108110, 5410108110,
            5410108110, 5410108110, 5410108110, 5410108110, 5410108110, 5410108110, 5410108110,0,0,0],
    'Сайт': ['https://eltex-co.ru/', 'https://eltex-co.ru/', 'https://eltex-co.ru/', 'https://eltex-co.ru/',
             'https://eltex-co.ru/', 'eltex-co.ru', 'https://eltex-co.ru/', 'https://eltex-co.ru/',
             'https://eltex-co.ru/', 'https://eltex-co.ru/', 'https://eltex-co.ru/', 'https://eltex-co.ru/',
             'https://eltex-co.ru/', 'https://eltex-co.ru/', 'https://eltex-co.ru/', 'cisco.com', 'huawei.com',
             'juniper.net'],
    'Уровень локализации': [10, 15, 15, 20, 30, 61, 35, 69, 58, 81, 90, 10, 11, 42, 71,0,0,0],
    'Аналоги': ['Cisco 7609; Cisco 713; Huawei NE8000 M6; Cisco NCS-5501-SE',
                'Huawei USG6610E; Huawei USG6630E; Cisco ASR 902',
                'Cisco ASA 5550; Huawei  USG6350',
                'Cisco ASA 5515-X; Huawei AR2220E',
                'Huawei USG6610E; Huawei USG6630E; Cisco ASR902',
                'NA',
                'Juniper MX-960; Cisco ASR-9010',
                'Huawei AR6140-16G4XG',
                'Huawei AR651; Huawei AR169CVW; ZYXEL ZyWALL ATP500',
                'Cisco ISR 4461',
                'P-LINK TL-R600VPN; Cisco RV130 VPN Router; ZYXEL yWALL ATP100',
                'Mikrotik Cloud Core Router CCR2216-1G-12XS-2XQ',
                'Fortine FortiGate 1800F; FortiGate 1100E; FortiGate 900G',
                'Cisco ISR 4461',
                'MikroTik CCR2216-1G-12XS-2XQ',
                'Eltex',
                'Eltex',
                'Solar'],
    'Запись': ['ТКО-168/24', 'ТКО-720/22', 'ТКО-728/22', 'ТКО-727/22', 'ТКО-719/22', 'ТКО-196/19',
               'ТКО-195/19', 'ТКО-48/24', 'ТКО-104/24', 'ТКО-887/23', 'ТКО-902/23', 'ТКО-157/24',
               'ТКО-160/24', 'ТКО-102/24', 'ТКО-103/24', 'отсутствует', 'отсутствует', 'отсутствует'],
    'Дата': ['07.10.2024', '07.10.2024', '06.06.2024', '06.06.2024', '07.10.2024', '06.04.2023', '06.06.2024',
             '04.03.2024', '19.03.2024', '14.01.2024', '06.06.2024', '07.08.2024', '07.08.2024', '19.03.2024',
             '19.03.2024','отсутствует', 'отсутствует', 'отсутствует'],
    'Документ': [4623, 4623, 2545, 2545, 4623, 1251, 2545, 881, 1121, 65, 2545, 3578, 3578, 1121, 1121, 0,0,0]
}

routers =pd.DataFrame(dict_routers)
conn = sqlite3.connect("routers.db")
routers.to_sql('router', conn, index= False, if_exists= 'replace')
cur = conn.cursor()
cur.execute('SELECT * FROM router')
row_data = cur.fetchall()
conn.close()
pprint(row_data)

app = Flask(__name__)
@app.route('/')
def hello_world():
    #TODO добавить ссылки на странички vendor
    return '''<h1> Hello, World! </h1>
            <br> Перейдите на страниуцу производителя: eltex, cisco, juniper, huawei</br>
            <br<a href = http://localhost:5000/eltex > http://localhost:5000/eltex </a></br>
            <br<a href = http://localhost:5000/cisco > http://localhost:5000/cisco </a></br>
            <br<a href = http://localhost:5000/juniper > http://localhost:5000/juniper </a></br>
            <br<a href = http://localhost:5000/huawei > http://localhost:5000/huawei </a></br>
            '''
@app.route('/<vendor>')
def router_equip(vendor):
    try:
        connect = sqlite3.connect('routers.db')
        cursor = connect.cursor()
        cursor.execute('''
        SELECT *
        FROM router
        WHERE vendor = ?
        ''', (vendor,))
        desc = cursor.description
        head = [desc[i][0] for i in range(len(desc))]
        data = pd.DataFrame(cursor.fetchall(),columns=[head])
        return data.to_html()
    except Exception as error:
        print("Ошибка при работе", error)
    finally:
        if connect:
            connect.close()
            print("Соединение с SQLite закрыто")
if __name__ == '__main__':
  app.run(debug=True)
