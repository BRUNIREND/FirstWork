import os.path
import sqlite3
import random


def normalise(num, cor):
    return '0' * (cor - len(str(num))) + str(num)


def check_sum(half_num):
    summ = 0
    pre_sum_1 = [int(half_num[i]) * 2 for i in range(len(half_num)) if i % 2 == 0]
    pre_sum_1 = sum([i if i < 10 else i % 10 + i // 10 for i in pre_sum_1])
    pre_sum_2 = sum([int(half_num[i]) for i in range(len(half_num)) if i % 2 != 0])
    summ += pre_sum_1 + pre_sum_2

    for i in range(10):
        if (summ + i) % 10 == 0:
            return str(i)



if os.path.isfile('card.s3db') == 0:
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE card(
                                  id INTEGER,
                                  number TEXT,
                                  pin TEXT,
                                  balance INTEGER DEFAULT 0);

    """)
else:
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()


class UserCard:
    def __init__(self, card_number, PIN, balance):
        self.card_number = card_number
        self.PIN = PIN
        self.balance = balance

    def log_in(self, card_input, PIN_input):
        cur.execute(f'SELECT number, pin FROM card WHERE number = {card_input} ')
        in_date = cur.fetchone()
        if in_date == None:
            print('\nWrong card number or PIN!\n')
            return False
        else:
            if int(PIN_input) != int(in_date[1]):
                print('\nWrong card number or PIN!\n')
                return False
            else:
                print('\nYou have successfully logged in!\n')
                return True

    def first_create(self):
        user_unic = random.randint(0, 999999999)
        user_pin_first = random.randint(0, 9999)
        bank_IIN = '400000'
        if len(str(user_unic)) < 9:
            user_unic = normalise(user_unic, 9)

        if len(str(user_pin_first)) < 4:
            user_pin_first = normalise(user_pin_first, 4)

        user_card_first = int(bank_IIN + str(user_unic) + check_sum(bank_IIN + str(user_unic)))

        self.card_number = user_card_first
        self.PIN = user_pin_first
        cur.execute(f"INSERT INTO card (id, number, pin, balance) VALUES (0,{self.card_number}, {self.PIN}, 0);")
        conn.commit()
    def add_income(self, value, my_card):
        cur.execute(f'SELECT id, number, pin, balance FROM card WHERE number = {my_card};')
        interm_date = cur.fetchone()
        cur.execute(f'DELETE FROM card WHERE number = {my_card};')
        cur.execute(f'INSERT INTO card(id, number, pin, balance) VALUES({interm_date[0]}, {interm_date[1]}, {interm_date[2]},{int(value) + int(interm_date[3])});')
        conn.commit()

    def do_transfer(self, card_sender, my_card):
        if int(card_sender)==int(my_card):
            return "You can't transfer money to the same account!\n"
        if check_sum(str(card_sender)[:-1])!=str(card_sender)[-1]:
            return 'Probably you made a mistake in the card number. Please try again!\n'

        else:
            cur.execute(f'SELECT number FROM card WHERE number = {card_sender};')
            if cur.fetchone()==None:
                return 'Such a card does not exist\n'
            value = int(input('Enter how much money you want to transfer:\n'))
            cur.execute(f'SELECT balance FROM card WHERE number = "{my_card}"')
            user_value = cur.fetchone()[0]

            if int(user_value) < int(value):
                return 'Not enough money!\n'
            else:
                cur.execute(f'SELECT id, number, pin, balance FROM card WHERE number = {my_card};')
                interm_date = cur.fetchone()
                cur.execute(f'DELETE FROM card WHERE number = {my_card};')
                cur.execute(f'INSERT INTO card(id, number, pin, balance) VALUES({interm_date[0]}, {interm_date[1]}, {interm_date[2]},{int(user_value) - int(value)});')
                cur.execute(f'SELECT id, number,pin, balance from card WHERE number = "{card_sender}";')
                sender_info = cur.fetchone()
                cur.execute(f'DELETE FROM card WHERE number = {card_sender};')
                cur.execute(f'INSERT INTO card(id, number, pin, balance) VALUES({sender_info[0]}, {sender_info[1]}, {sender_info[2]},{int(sender_info[3]) + int(value)});')
                conn.commit()
                return 'Success!\n'

    def close_account(self, my_card):
        cur.execute(f'DELETE FROM card WHERE number = {my_card}')
        return 'The account has been closed!\n'





second_flag = True
while True and second_flag:
    first_user_input = input('1. Create an account\n2. Log into account\n0. Exit\n')
    if first_user_input == '0':
        print('\nBye!')
        break
    elif first_user_input == '1':
        user_card = UserCard(0, 0, 0)
        user_card.first_create()
        print('\nYour card has been created\nYour card number:\n{}\nYour card PIN:\n{}\n'.format(user_card.card_number,
                                                                                                 user_card.PIN))
    elif first_user_input == '2':
        check_card = int(input('\nEnter your card number:\n'))
        check_PIN = int(input('Enter your PIN:\n'))
        flag = user_card.log_in(check_card, check_PIN)
        while flag:
            user_second_input = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
            if user_second_input == '1':
                cur.execute(f'SELECT balance From card WHERE number = {user_card.card_number}')
                print('\nBalance: {}\n'.format(cur.fetchone()[0]))
            elif user_second_input == '2':
                add_value = int(input("\nEnter income:\n"))
                user_card.add_income(add_value, check_card)
                print('Income was added!\n')
            elif user_second_input == '3':
                print(user_card.do_transfer(input('Enter card number:\n'), check_card))
            elif user_second_input == '4':
                print(user_card.close_account(check_card))
                flag = False

            elif user_second_input == '5':
                print('\nYou have successfully logged out!\n')
                break
            elif user_second_input == '0':
                second_flag = False
                print('\nBye!')
                break
    conn.commit()