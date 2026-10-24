from collections import UserDict
from datetime import datetime, date, timedelta
import re


# Base class for all fields in the contact record
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Representing the contact's name field
class Name(Field):
    pass


# Representing the contact's phone number field   
class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"[0-9]{10}", value):
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)

# Representing the contact's birthday field
class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
            if birthday.strftime("%d.%m.%Y") != value:
                raise ValueError
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(birthday)


# Representing a contact record containing name, phones, and birthday
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Add a phone number to the contact
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Remove a phone number from the contact
    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        if found_phone:
            self.phones.remove(found_phone)

    # Edit an existing phone number for the contact
    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)
        if not found_phone:
            raise ValueError("Phone number not found.")
        new_phone = Phone(new_phone)
        found_phone.value = new_phone.value

    # Find a phone number in the contact's phone list
    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    # Add a birthday to the contact
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    
    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"

# Representing the address book containing multiple contact records
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    # Find a contact record by name
    def find(self, name):
        return self.data.get(name)

    # Delete a contact record by name
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # Adjust February 29 birthdays to March 1 in non-leap years.
    def adjust_leap_day_birthday(self, date_of_birth: date, year: int) -> date:
        try:
            return date_of_birth.replace(year=year)
        except ValueError:
            return date_of_birth.replace(year=year, month=3, day=1)

    # Find the next birthday, adjusting February 29 if necessary.
    def get_next_birthday(self, date_of_birth: date, today: date) -> date:
        next_birthday = self.adjust_leap_day_birthday(date_of_birth, today.year)

        if next_birthday < today:
            next_birthday = self.adjust_leap_day_birthday(date_of_birth, today.year + 1)

        return next_birthday

    # Get birthdays within the next 7 days, including today.
    # Move weekend congratulations to Monday.
    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            date_of_birth = record.birthday.value.date()
            next_birthday = self.get_next_birthday(date_of_birth, today)

            if 0 <= (next_birthday - today).days <= 7:
                weekday = next_birthday.weekday()

                # Move weekend birthdays to Monday
                if weekday >= 5:
                    next_birthday += timedelta(days=7 - weekday)

                congratulation_date = next_birthday

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })

        return upcoming_birthdays
