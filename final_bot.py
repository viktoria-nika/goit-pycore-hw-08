import pickle
from class_Birthday import AddressBook, Record

# @input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact upadated."
    else:
       return "contakt not found" 

def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        string_book = ""
        for phone in record.phones:
            string_book += f"{phone}\n"
        return string_book
    return "contact not found"   

def show_all(book: AddressBook):
    if not book.data:
        return "not contacts"
    else:
        string = ""
        for name, record_ in book.data.items():
            string += f"{record_}\n"
        return string
    
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "birthday added"
    return "contact not found"
    

def show_birthday(args, book: AddressBook):
    name = args [0]
    record = book.find(name)
    if record:
        return record.birthday
    return "contact not found"

def birthdays(book: AddressBook):
    list_b = book.get_upcoming_birthdays()
    if not list_b:
        return "not birthday"
    else:
        string_book_birthday = ""
        for birthday in list_b:
            string_book_birthday += f"{birthday}\n"
        return string_book_birthday

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
