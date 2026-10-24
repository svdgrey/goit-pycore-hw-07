from decorators import input_error
from models import Record

# Parse user input into command and arguments
def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.lower(), *args

# Handler to add a new contact to the address book
@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."

# Handler to change an existing contact's phone number
@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

# Handler to show a contact's phone numbers
@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name.")
    record = book.find(args[0])
    if record is None:
        raise KeyError("Contact not found.")
    return "; ".join(phone.value for phone in record.phones)


# Handler to show all contacts in the address book
@input_error
def show_all(book):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())

# Handler to add a birthday to a contact
@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."

# Handler to show a contact's birthday
@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name.")
    record = book.find(args[0])
    if record is None:
        raise KeyError("Contact not found.")
    if record.birthday is None:
        return "Birthday not found."
    return record.birthday.value.strftime("%d.%m.%Y")

# Handler to show upcoming birthdays within the next 7 days
@input_error
def birthdays(args, book):
    if args:
        raise ValueError("Invalid command.")
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    result = ""
    for contact in upcoming:
        result += f"{contact['name']}: {contact['congratulation_date']}\n"
    return result.strip()
