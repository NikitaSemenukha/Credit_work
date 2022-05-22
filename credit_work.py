"""
                                Залікова робота
За посиланням https://registry.edbo.gov.ua/opendata/universities/
розміщено РЕЄСТР СУБ'ЄКТІВ ОСВІТНЬОЇ ДІЯЛЬНОСТІ (ЗАКЛАДИ ВИЩОЇ, ФАХОВОЇ ПЕРЕДВИЩОЇ ТА ПРОФЕСІЙНОЇ (ПРОФЕСІЙНО-ТЕХНІЧНОЇ) ОСВІТИ)
Завдання:
    1.Запитати у користувача код регіону
    2.Отримати ЗВО з вказаного користувачем регіону
    3.Зберегти всі дані у файл universities.csv у форматі csv
    4.Збережіть ті ж дані у файл universities_<код регіону>.csv, наприклад universities_80.csv
    5.Якщо регіон не зі списку доступних, то повідомити про це користувачеві у консолі
    6.Відфільтруйте і збережіть таку інформацію про заклади:
        Назви та ПІП керівників в файл rectors.csv
    7.Ускладніть програму з першого завдання наступним фільтром:
        З формою фінансування Державна
    8.Ускладніть програму з другого завдання можливістю фільтрування за будь-яким з наявних значень поля
"""


import requests
import csv


if __name__ == '__main__':

    _region_key = str(input('Enter region code = '))

    _string_key = ['01', '05', '07']
    _int_key = [12, 14, 18, 21, 23, 26, 32, 35, 44, 46, 48, 51, 53, 56, 59, 61, 63, 65, 68, 71, 73, 74, 80, 85]

    _check_0 = int(_region_key) in _int_key
    _check_1 = _region_key in _string_key

    if _check_0 is False:
        if _check_1 is False:
            print(f"This region isn't registered")
            exit(0)

    print('Форма фінансування: ''Державна''/Приватна''/Комунальна')
    _string = str(input("Обреріть щось одне з вибірки: "))

    r = requests.get('https://registry.edbo.gov.ua/api/universities/?ut=1&lc=' + _region_key + '&exp=json')
    universities: list = r.json()

    _filteredData = [{k: row[k] for k in [
        'university_id',
        'university_parent_id',

        'university_type_name',

        'university_name',
        'university_short_name',
        'university_name_en',

        'registration_year',

        'university_director_post',
        'university_director_fio',

        'region_name',
        'region_name_u',
        'university_address',
        'university_address_u',
        'post_index',
        'post_index_u',
        'is_from_crimea',

        'koatuu_id',
        'koatuu_name',
        'koatuu_id_u',
        'koatuu_name_u',

        'university_phone',
        'university_email',
        'university_site',

        'close_date',
        'primitki',

        'university_edrpou',
        'university_governance_type_name',
        'university_financing_type_name',
    ]
                      } for row in universities]

    _filter_financing_type_name = [{k: row[k] for k in ['university_name',
                                                        'university_director_fio',
                                                        'university_financing_type_name'
                                                        ]
                                    }
                                   for k in ['university_financing_type_name']
                                   for row in universities if row[k] == _string]

    with open('universities.csv', mode='w', encoding='UTF-8') as _file:
        writer = csv.DictWriter(_file, fieldnames=_filteredData[0].keys())
        writer.writeheader()
        writer.writerows(_filteredData)

    with open('universities_' + _region_key + '.csv', mode='w', encoding='UTF-8') as _file:
        writer = csv.DictWriter(_file, fieldnames=_filteredData[0].keys())
        writer.writeheader()
        writer.writerows(_filteredData)

    with open('rectors.csv', mode='w', encoding='UTF-8') as _file:
        writer = csv.DictWriter(_file, fieldnames=_filter_financing_type_name[0].keys())
        writer.writeheader()
        writer.writerows(_filter_financing_type_name)