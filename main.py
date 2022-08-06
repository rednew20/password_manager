import base64
# import os
import datetime
# from cryptography.fernet import Fernet
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from requests import Request, Session
import sqlite3
from sqlite3 import Error
import getpass
from match import Match

userlogged = []


def gen_key(password):
    key = base64.urlsafe_b64encode(password.encode("utf-8"))
    return key


def create_db():
    try:
        conn = sqlite3.connect('mypassword.db')
        cursor = conn.cursor()
        sql_file = open("sql_script.sql")
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
    except sqlite3.Error as error:
        print('Error :', error)
    finally:
        if conn:
            conn.close()
            print('SQLite Connection closed')


def register_user(username, password, email):
    print("Register main user. \n")
    answer = input('You want to register (y/n) ?:')
    conn = sqlite3.connect('mypassword.db')
    if (answer.lower() == 'y'):
        db_cursor = conn.cursor()
        sql_str = f"INSERT INTO user_info (username,password,email) VALUES ('{username}', '{password.decode('utf-8')}', '{email}')"
        db_cursor.execute(sql_str)
        conn.commit()

    else:
        print('Good luck.')


def execute_query(conn, query):
    try:
        db_cursor = conn.cursor()
        result = db_cursor.execute(query)
        response = result.fetchone()
        return response
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def validate_user(username, password):
    conn = sqlite3.connect('mypassword.db')
    user_credentials = execute_query(conn,
                                     f"SELECT * FROM user_info WHERE username = '{username}'")

    if (user_credentials is not None):
        if (user_credentials[2].encode('utf-8') == password):
            return True
        else:
            print("Username/Password don't match.")
            return False
    else:
        create_db()
        register = input(
            'No Main exists, you want to register with the information you input?(y/n): ')
        if (register == 'Y' or register == 'y'):
            email = input('Input your email: ')
            register_user(username, password, email)


def authenticate_user(username, password):
    encrypted_password = gen_key(password)
    authenticated = validate_user(username, encrypted_password)
    if authenticated:
        print(f'Login Success. Welcome {username}, \n')
        userlogged.append([username, datetime.datetime.now()])


def store_password():
    return True


def get_password():
    return True


def login():
    print('=========User Login========= \n')
    username = input('Input Username: ')
    password = getpass.getpass(prompt='Input Password: ')
    authenticate_user(username, password)


def print_help():
    print("---------------------------------------------------------")
    print("> help - Command to get the list of command inputs. ")
    print("> login - Command to authenticate. ")
    print("> getpass - Command to get stored password. ")
    print("> setpass - Command to add new password info to the vault.")
    print("> updpass - Command to update stored password. ")
    print("> delpass - Command to delete stored password. ")
    print("> recover - Recover admin user password. ")
    print("> quit - Exit application. ")
    print("---------------------------------------------------------")


def default():
    print('Put a valid option. ')
    return 0


def quit():
    exit()


print("--------------------------------------------------------- \n")
print("Welcome to Password Manager, Please login. For command help please input 'help' command. \n")
print("--------------------------------------------------------- \n")
try:
    my_switch = Match()
    while True:
        command = input('Input command:')
        # switch(int(command))
        call_option = (my_switch.case(command))
        eval(call_option)
except KeyboardInterrupt:
    pass
