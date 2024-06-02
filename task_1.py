
""""
реализовать копирование данных из одного файла в другой файл.
написать отдельную функцию copy_data:
прочитать список словарей (read_file)
и записать его в новый файл используя функцию standart_write
дополнить функцию main
из phone.csv в phone2.csv
"""

from csv import DictReader, DictWriter
from os.path import exists

class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_info():
    flag = False
    while not flag:
        try:
            first_name = input('Имя: ')
            if len(first_name) < 2:
                raise NameError('Слишком короткое имя')
            second_name = input('Введите фамилию: ')
            if len(second_name) < 4:
                raise NameError('Слишком короткая фамилия')
            phone_number = input('введите номер телефона: ')
            if len(phone_number) < 11:
                raise NameError('Слишком короткий номер телефона')
        except NameError as err:
            print(err)
        else:
            flag = True
    return [first_name, second_name, phone_number]

def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()

def write_file(file_name):
    user_data = get_info()
    res = read_file(file_name)
    new_obj = {'first_name': user_data[0], 'second_name': user_data[1], 'phone_number': user_data[2]}
    res.append(new_obj)
    standart_write(file_name, res)

def read_file(file_name):
    with open(file_name, encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r)

def remove_row(file_name):
    search = int(input('Введите номер строки для удаления: '))
    res = read_file(file_name)
    if search <= len(res):
        res.pop(search - 1)
        standart_write(file_name, res)
    else:
        print('Введен не верный номер строки')

def update_row(file_name):
    search = int(input('Введите номер строки для изменения: '))
    res = read_file(file_name)
    if search <= len(res):
        print(f'Текущие данные: {res[search - 1]}')
        new_data = get_info()
        res[search - 1] = {'first_name': new_data[0], 'second_name': new_data[1], 'phone_number': new_data[2]}
        standart_write(file_name, res)
    else:
        print('Введен не верный номер строки')

def standart_write(file_name, res):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
        f_w.writerows(res)

def search_by_name(file_name):
    search_name = input("Введите имя или фамилию для поиска: ")
    data = read_file(file_name)
    results = [row for row in data if search_name.lower() in row['first_name'].lower() or search_name.lower() in row['second_name'].lower()]
    if results:
        print("Найденные данные:")
        for row in results:
            print(row)
    else:
        print("Данные не найдены.")

def update_by_name(file_name):
    search_name = input("Введите имя или фамилию для изменения: ")
    data = read_file(file_name)
    found = False
    for i, row in enumerate(data):
        if search_name.lower() in row['first_name'].lower() or search_name.lower() in row['second_name'].lower():
            print(f"Текущие данные: {row}")
            new_data = get_info()
            data[i] = {'first_name': new_data[0], 'second_name': new_data[1], 'phone_number': new_data[2]}
            found = True
            break
    if found:
        standart_write(file_name, data)
        print("Данные успешно изменены.")
    else:
        print("Данные не найдены.")

def remove_by_name(file_name):
    search_name = input("Введите имя или фамилию для удаления: ")
    data = read_file(file_name)
    new_data = [row for row in data if search_name.lower() not in row['first_name'].lower() and search_name.lower() not in row['second_name'].lower()]
    if len(data) != len(new_data):
        standart_write(file_name, new_data)
        print("Данные успешно удалены.")
    else:
        print("Данные не найдены.")

def copy_data(source_file, dest_file):
    data = read_file(source_file)
    standart_write(dest_file, data)
    print(f'Данные успешно скопированы из {source_file} в {dest_file}')

file_name = 'phone.csv'

def main():
    while True:
        command = input('Введите команду: ')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
        elif command == 'r':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            print(*read_file(file_name))
        elif command == 'd':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            remove_row(file_name)
        elif command == 'u':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            update_by_name(file_name)
        elif command == 's':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            search_by_name(file_name)
        elif command == 'r':
            if not exists(file_name):
                print('Файл отсутствует, пожалуйста , создайте файл')
                continue
            remove_by_name(file_name)
        elif command == 'c':
            source_file = 'phone.csv'
            dest_file = 'phone2.csv'
            copy_data(source_file, dest_file)

main()