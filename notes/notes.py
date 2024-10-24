class Note:
    def __init__(self, surname, name, telNumber, birthdate):
        self.surname = surname
        self.name = name
        self.telNumber = telNumber
        self.birthdate = birthdate

    def __str__(self):
        return f"{self.surname} {self.name}, Номер телефона: {self.telNumber}, Дата Рождения: {self.birthdate[0]:02}.{self.birthdate[1]:02}.{self.birthdate[2]}"
def input_notes():
    notes = []
    for _ in range(2):
        surname = input('Введите фамилию: ')
        name = input('Введите имя: ')
        telNumber = input('Введите номер телефона: ')
        while True:
            try:
                day = int(input('Введите день рождения (1-31): '))
                month = int(input('Введите месяц рождения (1-12): '))
                year = int(input('Введите год рождения: '))
                if 1 <= day <= 31 and 1 <= month <= 12:
                    break
                else:
                    print('Вы ввели некорректную дату. Попробуйте снова')
            except ValueError:
                print('Пожалуйста,введите числовое значение')
        birthdate = [day, month, year]
        notes.append(Note(surname, name, telNumber, birthdate))
    return notes
def sorted_notes(notes):
    return sorted(notes, key=lambda note: (note.surname, note.name))
def display_notes(notes, month):
    found = False
    for note in notes:
        if note.birthdate[1] == month:
            print(note)
            found = True
    if not found:
        print('Нет людей с днем рождения в этом месяце')
def save_to_file(notes, filename):
    with open(filename, 'w', encoding='UTF-8') as file:
        for note in notes:
            file.write(f"{note} \n")
def main():
    notes = []
    while True:
        print('Меню:')
        print("1. Ввести записи")
        print("2. Отсортировать и отобразить записи")
        print("3. Показать дни рождения в месяце")
        print("4. Сохранить записи в файл")
        print("5. Выход")
        choice = input('Выберите пункт меню (от 1 до 5): ')
        if choice == "1":
            new_notes = input_notes()
            notes.extend(new_notes)
            print('Записи успешно введены!')
        elif choice == "2":
            if notes:
                notes = sorted_notes(notes)
                print('Записи успешно отсортированы!')
                for note in notes:
                    print(note)
            else:
                print('Сначала введите записи')
        elif choice == "3":
            if notes:
                month = int(input('Введите номер месяца для поиска дней рождений (1-12): '))
                display_notes(notes, month)
            else:
                print('Сначала введите записи')
        elif choice == "4":
            if notes:
                filename = input('Введите полное название файла для сохранения: ')
                save_to_file(notes, filename)
                print(f"Записи сохранены в файл {filename}")
            else:
                print('Сначала введите записи')
        elif choice == "5":
            print('Выход из программы')
            break
        else:
            print('Некорректный выбор пункта меню, повторите снова')
if __name__ == "__main__":
    main()
