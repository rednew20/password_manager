import base64
from contextvars import copy_context
import os
import datetime
from unittest import result

from requests import Request, Session
import sqlite3
from sqlite3 import Error
import getpass
from match import Match
# from command import Command

# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage
import random
import string


userlogged = []
conn = sqlite3.connect('mypassword.db')


def email_sender(email, code):

    msg = EmailMessage()
    msg['Subject'] = f'Password Reset Code '
    msg['From'] = 'info@wenderalvarado.com'
    msg['To'] = email
    msg.set_content(f' Your Code to change password is: {code} ')

    # Send the message via our own SMTP server.
    user = os.environ.get('EMAIL_ADDR')
    password = os.environ.get('EMAIL_PASS')
    url = os.environ.get('EMAIL_PASS')

    smtpObj = smtplib.SMTP_SSL(url, 465)
    smtpObj.login(user, password)
    #smtpObj = smtplib.SMTP('localhost', 25)
    #smtpObj.sendmail(user, email, msg)
    smtpObj.send_message(msg)
    print("Successfully sent email")

    # except smtplib.SMTPException:
    #    print("Error: unable to send email")


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
            #print('SQLite Connection closed')


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
    # finally:
    #     if conn:
    #         conn.close()


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


def is_logged():
    if (len(userlogged) > 0):
        return True

    print("Please Login. \n")
    return False


def getacc():
    if (is_logged()):
        print("\n=== Get Account Password ===")
        account = input('Input Account Name: ')
        username = input('Confirm the Username: ')
        user_info = execute_query(conn,
                                  f"SELECT account_password FROM account WHERE account_name = '{account}' and account_username = '{username}'")
        if (user_info):
            dbpass = base64.urlsafe_b64decode(user_info[0])
            print("______________________\n")
            print(f"Account:{account}, Username: {username} \n")
            print("Password is :", dbpass.decode('utf-8'), " \n")
        else:
            print('Password not stored. \n')
        # return True


def addacc():
    if (is_logged()):
        conn = sqlite3.connect('mypassword.db')
        print("\n=== Setting new Account ===")
        account = input('Input Account Name: ')
        username = input('Input Account Username: ')
        password = getpass.getpass(prompt='Input account Password: ')
        try:
            db_cursor = conn.cursor()
            sql_str = f"""INSERT INTO account (account_name,account_username,account_password,created_at,updated_at) 
                        VALUES ('{account}', '{username}', '{gen_key(password).decode('utf-8')}','{datetime.datetime.now()}','{datetime.datetime.now()}')"""

            # print(sql_str)
            db_cursor.execute(sql_str)
            conn.commit()
            print("Account saved successfully. \n")
        except Error as e:
            print(e)
        return True


def updacc():
    if (is_logged()):
        conn = sqlite3.connect('mypassword.db')
        print("\n=== Update Account ===")
        account = input('Input Account Name: ')
        username = input('Input Account Username: ')
        password = getpass.getpass(prompt='Input Account new Password: ')
        try:
            db_cursor = conn.cursor()
            sql_str = f"""UPDATE account SET account_password = '{gen_key(password).decode('utf-8')}', updated_at='{datetime.datetime.now()}' 
            WHERE account_name = '{account}' and account_username = '{username}'"""

            db_cursor.execute(sql_str)
            conn.commit()
            print("Account updated successfully. \n")
        except Error as e:
            print(e)
        return True


def delacc():
    if (is_logged()):
        conn = sqlite3.connect('mypassword.db')
        print("\n=== Update Account ===")
        account = input('Input Account Name: ')
        username = input('Input Account Username: ')
        confirm = input('Confirm to Delete (y/n): ')

        if (confirm.lower() == 'y'):
            try:
                db_cursor = conn.cursor()
                sql_str = f"""DELETE FROM account WHERE account_name = '{account}' and account_username = '{username}'"""

                print(sql_str)
                db_cursor.execute(sql_str)
                conn.commit()
                print("Account Deleted successfully. \n")
            except Error as e:
                print(e)
            return True


def listacc():
    if ((is_logged())):
        conn = sqlite3.connect('mypassword.db')

        try:
            db_cursor = conn.cursor()
            sql_str = f"SELECT account_name FROM account"
            result = db_cursor.execute(sql_str)
            rows = result.fetchall()
            for row in rows:
                print("-", row[0])

        except Error as e:
            print(e)
        return True


def recover():
    conn = sqlite3.connect('mypassword.db')
    print('=========Password Recovery========= \n')
    username = input('Input the Main username: ')
    email = input('Confirm Main User Email: ')

    data = execute_query(conn,
                         f"SELECT username,email FROM user_info WHERE username = '{username}'")

    if (data[1] == email):
        # email match
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        print(result_str)
        email_sender(email, result_str)


def login():
    print('=========User Login========= \n')
    username = input('Input Username: ')
    password = getpass.getpass(prompt='Input Password: ')
    authenticate_user(username, password)


def print_help():
    print("---------------------------------------------------------")
    print("> help - Command to get the list of command inputs. ")
    print("> login - Command to authenticate. ")
    print("> addacc - Command to get stored password. ")
    print("> setacc - Command to add new password info to the vault.")
    print("> updacc - Command to update stored password. ")
    print("> delacc - Command to delete stored password. ")
    print("> listacc - Command to list the account stored. ")
    print("> recover - Recover admin user password via Email ")
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

    # switch = Command()
    while True:
        # command = input('Input command:')
        # switch.switcher.get(command, switch.default)()
        my_switch = Match()
        input_cmd = input('Input command:')
        call_option = (my_switch.case(input_cmd))
        eval(call_option)
except KeyboardInterrupt:
    pass
