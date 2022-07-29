from cryptography.fernet import Fernet
import sqlite3
from sqlite3 import Error
import getpass

key = Fernet.generate_key()
crypter = Fernet(key)
conn = sqlite3.connect('mypassword.db')


def create_db():
    print('Run Script')
    cursor = conn.cursor()
    sql_file = open("sql_script.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)


def register_user(username, password):
    print("register main user.")
    answer = input('You want to register (y/n) ?:')

    if (answer.lower == 'y'):
        db_cursor = conn.cursor()
        register = db_cursor.execute(
            "INSERT INTO user_info VALUES as (?,?)", (username, password))


def db_connection(username, password):
    try:
        db_cursor = conn.cursor()
        credentials = db_cursor.execute(
            "SELECT * FROM user_info WHERE username =  ? and password = ?", (username, password)).fetchall()
        if (credentials != None):
            print(credentials[0])
        else:
            print('user not exists')
    except Error as e:
        print(e)
        create_db()
        #register_user(username, password)

    finally:
        if conn:
            conn.close()


def authenticate_user(username, password):
    encrypt_password = crypter.encrypt(password.encode())
    db_connection(username, encrypt_password)

    print('MyPass=', password)
    print('MyPass=', encrypt_password)
    decrypt_password = crypter.decrypt(encrypt_password).decode()
    print('MyPassAgain=', decrypt_password)


# get username and password

username = input('Input username: ')
print(username)
password = getpass.getpass(prompt='Input password: ')

authenticate_user(username, password)
