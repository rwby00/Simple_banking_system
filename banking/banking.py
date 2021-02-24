# Import Random & Import sqlite
import random
import sqlite3
import luhn


class BankingSystem:
    def __init__(self, database):
        # Define DB Connections
        self.conn = sqlite3.connect(f'{database}.s3db')
        self.cur = self.conn.cursor()
        self.c = self.conn.cursor()

        # Temporary variables for use in printing stuff
        self.card_number = None
        self.card_pin = None
        self.card_balance = None
        self.amount = 0
        self.amount_transfer = 0
        self.card_number_check = None
        self.temp_info_balance_transfer_check = None

        # Functions
        self.db_init()
        self.print_menu()

    def db_init(self):
        # Create table card if it doesn't already exist & then commit it
        self.c.execute('DROP TABLE card')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card(
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
        );
        ''')
        self.conn.commit()

    def print_menu(self):
        # Print menu
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")

        menu_input = input()  # Take Input

        # Do stuff with input
        if menu_input == "1":
            self.create_card()
        elif menu_input == "2":
            self.log_in()
        elif menu_input == "0":
            print("Bye!")

    def create_card(self):
        # Generate numbers
        self.card_number = generate_card_number()
        self.card_pin = generate_pin_number()
        self.card_balance = 0

        # Add numbers to database
        self.cur.execute(f'INSERT INTO card (number, pin) VALUES ({self.card_number}, {self.card_pin});')
        self.conn.commit()

        # Print output
        print("Your card has been created")
        print("Your card number:")
        print(self.card_number)
        print("Your card PIN:")
        print(self.card_pin)

        self.print_menu()

    def log_in(self):
        # Take input
        card_number = input("Enter your card number:")
        card_pin = input("Enter your PIN:")

        # Query DB
        self.cur.execute(f'SELECT * FROM card WHERE number = ? AND pin = ?', (card_number, card_pin))
        temp_info = self.cur.fetchone()

        # If found in DB, then login
        if temp_info is not None:
            self.card_number = temp_info[1]
            self.card_pin = temp_info[2]
            self.card_balance = temp_info[3]
            print("You have successfully logged in!")
            self.banking_menu()
        else:
            print("Wrong card number or PIN!")
            self.print_menu()

    def banking_menu(self):

        # Print menu
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")

        banking_input = input()  # Take Input

        # Do stuff with input
        if banking_input == "1":
            self.balance()
        elif banking_input == "2":
            self.add_income()
        elif banking_input == "3":
            self.do_transfer()
        elif banking_input == "4":
            self.close_account()
        elif banking_input == "5":
            print("You have successfully logged out!")
            self.print_menu()
        elif banking_input == "0":
            print()

    def balance(self):
        self.cur.execute(f'SELECT balance FROM card WHERE number = {self.card_number}')
        temp_info_balance = self.cur.fetchone()
        self.card_balance = temp_info_balance[0]
        print(f'Balance: {self.card_balance}')
        self.banking_menu()

    def add_income(self):
        self.amount = int(input("Enter income:"))
        self.cur.execute(f'UPDATE card SET balance = (balance + {self.amount}) WHERE number = ({self.card_number});')
        self.conn.commit()
        print("Income was added")
        self.banking_menu()

    def do_transfer(self):
        self.card_number_check = input("Enter your card number:")
        self.cur.execute(f'SELECT number FROM card')
        temp_info_transfer = self.cur.fetchall()
        if int(self.card_number_check) == int(self.card_number):
            print("You can't transfer money to the same account!")
            self.banking_menu()
        elif (self.card_number_check,) in temp_info_transfer:
            self.cur.execute(f'SELECT balance FROM card where number = {self.card_number}')
            temp_info_balance_transfer = self.cur.fetchone()
            self.temp_info_balance_transfer_check = temp_info_balance_transfer[0]
            self.amount_transfer = int(input("Enter how much money you want to transfer:"))
            if self.amount_transfer > self.temp_info_balance_transfer_check:
                print("Not enough money")
                self.banking_menu()
            elif self.amount_transfer <= self.temp_info_balance_transfer_check:
                self.cur.execute(f'UPDATE card SET balance = (balance + {self.amount_transfer}) WHERE number = ({self.card_number_check});')
                self.cur.execute(f'UPDATE card set balance = (balance - {self.amount_transfer}) WHERE number = ({self.card_number});')
                self.conn.commit()
                print("Success")
                self.banking_menu()

        elif luhn.verify(self.card_number_check) is False:
            print("Probably you made a mistake in the card number. Please try again!")
            self.banking_menu()
        elif (self.card_number_check,) not in temp_info_transfer:
            print("Such a card does not exist.")
            self.banking_menu()

    def close_account(self):
        self.cur.execute(f'DELETE from card  WHERE number = ({self.card_number});')
        self.conn.commit()
        print("The account has been closed")
        self.print_menu()


# Number generation
def generate_card_number():
    first_15 = f'400000{str(random.randint(0, 999999999)).zfill(9)}'
    temp_15 = list(map(int, first_15))
    sum_temp_15 = 0
    for i_ in range(len(temp_15)):
        if i_ % 2 == 0:
            temp_15[i_] *= 2
            if temp_15[i_] > 9:
                temp_15[i_] -= 9
        sum_temp_15 += temp_15[i_]
    checksum_manual = str(10 - (sum_temp_15 % 10))[-1:]

    return f'{first_15}{checksum_manual}'


def generate_pin_number():
    return str(random.randint(1, 9999)).zfill(4)


# Bank Class
bank = BankingSystem("card")
