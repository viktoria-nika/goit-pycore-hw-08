from datetime import datetime, timedelta, date
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
         return str(self.value)

class Name(Field):
        pass

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
     
class Phone(Field):
    def __init__(self, value:str):
        if len(value) == 10 and value.isdigit():
            # self.value=value
            super().__init__(value)
        else:
            raise ValueError("не вірний номер")
            # print("помилка")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone  
    
    def find_phone(self,phone):
        for p in self.phones:
            if p.value == phone:
                return p
            
    def remove_phone(self, phone):
        object_phone = self.find_phone(phone)
        if object_phone:
            self.phones.remove(object_phone)

    def add_birthday(self, birthday):
           self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        return self.data.get(name)
    
    def delete(self, name):
        res = self.data.get(name)
        if res:
            del self.data[name]

    def get_upcoming_birthdays(self):
        if not self.data:
            return []
        to_date = date.today()
        res = []
        for record in self.data.values():
            birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=to_date.year).date()

            if birthday < to_date:
                birthday = birthday.replace(year=to_date.year+1)

            if to_date <= birthday<=to_date+timedelta(days=7):
                dete_week = birthday.weekday()

                if dete_week == 5:
                    birthday = birthday+timedelta(days=2)

                if dete_week == 6:
                    birthday = birthday+timedelta(days=1)

                res.append({"name":record.name.value,"congratulation_date":birthday.strftime("%d.%m.%Y")})

        return res
   
if __name__ == "__main__":

# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("13.08.2000")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("10.08.2001")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record_ in book.data.items():
        print(record_)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john.birthday)
    # john.remove_phone("1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    # book.delete("Jane")

    print(book.get_upcoming_birthdays())
