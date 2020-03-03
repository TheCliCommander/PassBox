#!/usr/bin/env python3

import random
import secrets
import string
import sqlite3
import pyperclip
import argparse
import getpass
from pysqlcipher3 import dbapi2 as sqlcipher


#CREATE PASSWORD OF GIVEN LENGTH
def get_pass(length):
    return "".join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for x in range(length))


def get_pass_length():
    length = int(input("Enter the length of password: "))
    password= get_pass(length)
    pyperclip.copy(password)
   
    return password
def create_and_store_pwsd():
    password = get_pass_length()
    name = str(input("Enter name for password: "))
    
    #CREATE DATABASE CONNECTION
    conn = sqlite3.connect('managerDB.db') 

    #CREATE CURSOR OBJECT
    c = conn.cursor()

    #CREATE TABLE IN DISK FILE BASED DATABASE
    c.execute("""CREATE TABLE IF NOT EXISTS password_table (
                            name TEXT,
                            pswd TEXT
                            )""")
    gather_names = "SELECT name FROM password_table WHERE name = ?"
    c.execute(gather_names,(name,))
    result = c.fetchall()
    if (name,) in result:
        print("Error: Password for " + name +" already exists!\nRemove with [-r] or choose another name.")
    else:  
        c.execute("INSERT INTO password_table (name, pswd) VALUES (?, ?)", (name, password))
        print('Password for ' + name + ' saved and copied to clipboard')

    #COMMIT CHANGES
    conn.commit()
    conn.close()


def query_pswd_by_name(name):

    conn = sqlite3.connect('managerDB.db')
    c = conn.cursor()
    query_password = "SELECT pswd FROM password_table WHERE name = ?"
    c.execute(query_password,(name,))
    result = c.fetchall()
    for row in result:
        pyperclip.copy(str(row[0]))
        print("Password for " + name +" copied to clipboard")
        
    conn.commit()
    conn.close()



def input_name_and_query():
    conn = sqlite3.connect('managerDB.db')
    c = conn.cursor()
    gather_names = "SELECT name FROM password_table WHERE name= ?"
    name = input('Name of password you wish to query: ')
    c.execute(gather_names,(name,))
    result = c.fetchall()
    
    if (name,) in result:
        query_pswd_by_name(name)
    else:
        print("Error: No password for " + name +"!")

def collect_pswd(name):
    conn = sqlite3.connect('managerDB.db')
    c = conn.cursor()
    query_password = "SELECT pswd FROM password_table WHERE name = ?"
    c.execute(query_password, (name,))
    result = c.fetchall()
    for row in result:
            print(row[0])
def view_pswd():
    conn = sqlite3.connect('managerDB.db')
    c = conn.cursor()
    gather_names = "SELECT name FROM password_table WHERE name = ?"
    name = input('Name of password you wish to view: ')
    c.execute(gather_names,(name,))
    result = c.fetchall()
    if (name,) in result:
        collect_pswd(name)
    else:
        print('Error: No password for ' + name +'!')

def remove_entry():
    name = input('Name of password you wish to remove: ')
    conn = sqlite3.connect('managerDB.db')
    c = conn.cursor()
    gather_names = "SELECT name FROM password_table Where name = ?"
    c.execute(gather_names,(name,))
    result = c.fetchall()
    if (name,) not in result:
        print("Error: "+name+ " does not exist!")
    else:
        confirm = str(input(("Are you sure you want to delete your "+name+" password? [Y/N]: ")))
        if confirm == "N":
            print(name+ " NOT deleted.")
        if confirm == "Y":
            delete_pswd = "DELETE FROM password_table WHERE name = ?"
            c.execute(delete_pswd, (name,))
            print('Password for '+ name +' removed')
        else:
            print("Please choose either [Y] or [N], case sensitive")
    conn.commit()
    conn.close()

def empty_passbox():
    confirm = str(input("Are you sure you want to delete all your passwords? [Y/N]: "))
    conn = sqlite3.connect('managerDB.db')
    c = conn.cursor()
    delete_all = "DELETE FROM password_table"
    # print(confirm)
    if confirm == "N":
        print("Whew, that was close!")
    elif confirm == "Y":
        c.execute(delete_all)
        print("Passbox has been permanently emptied!")
    else:
        print("Please choose [Y] or [N], case sensitive")
    conn.commit()
    conn.close()
def list_names():
    conn = sqlite3.connect('managerDB.db')
    c = conn.cursor()
    get_names = "SELECT name FROM password_table"
    c.execute(get_names)
    result = c.fetchall()
    for row in result:
        print(row[0])


def main():
#Runs program and handles command line options

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--new", action="store_true", help="create a new password")
    group.add_argument("-q", "--query", action="store_true", help="query an existing password")
    group.add_argument("-r", "--remove", action="store_true", help="remove an existing password")
    group.add_argument("-e", "--empty", action="store_true", help="delete all passwords")
    group.add_argument("-l", "--list", action="store_true", help="lists all names")
    group.add_argument("-v", "--view", action="store_true", help="displays password in terminal instead of just copying it to clipboard")
    args = parser.parse_args()
    if args.new:
        create_and_store_pwsd()
    
    elif args.query:
        input_name_and_query()
    elif args.remove:
        remove_entry()
    elif args.empty:
        empty_passbox()
    elif args.list:
        list_names()
    elif args.view:
        view_pswd()

    else:
       print("Please select an option. [-h] for help and list of options")
if __name__ == '__main__':
    main()




