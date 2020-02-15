import random
import secrets 
import string
import sqlite3
import pyperclip
import optparse

#CREATE PASSWORD OF GIVEN LENGTH
def get_pass(length):
	return "".join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for x in range(length))

	
def get_pass_length():
	length = int(input("Enter the length of password: "))
	password= get_pass(length)
	print(password)
	pyperclip.copy(password)
	print('Password copied to clipboard')
	return password
def create_and_store_pwsd():
	password = get_pass_length()
	name = str(input("Enter name for password: "))

	#CREATE DATABASE CONNECTION
	conn = sqlite3.connect("managerDB.db")

	#CREATE CURSOR OBJECT
	c = conn.cursor()

	#CREATE TABLE IN DISK FILE BASED DATABASE
	c.execute("""CREATE TABLE IF NOT EXISTS password_table (
							name TEXT,
							pswd TEXT
							)""")
	c.execute("DELETE FROM password_table")
	c.execute("INSERT INTO password_table (name, pswd) VALUES (?, ?)", (name, password))
	print(str(password) + 'copied to clipboard')

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
		print("Password copied to clipboard")
		print(str(row[0]))
	conn.commit()
	conn.close()

def input_name_and_query():
	name = input('Name of password you wish to query: ')
	query_pswd_by_name(name)

create_and_store_pwsd()

input_name_and_query()

# def main():
# 	"""Runs program and handles command line options"""
	
# 	parser = argparse.ArgumentParser()
# 	group = parser.add_mutually_exclusive_group()
# 	group.add_argument("-n", "--new", action="store_const", const=get_pass(arg.length))
# 	group.add_argument("-q", "--query", action="store_const", const=query_pswd_by_name(arg.name))
# 	parser.add_argument("name", help="The name of the password you wish to query.", type=str)
# 	parser.add_argument("length", , help="The desired length of password.",\
# 								type=int)

# 	args = parser.parse_args()

	




