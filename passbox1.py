import random
import secrets 
import string
import sqlite3
import pyperclip
import optparse

#CREATE PASSWORD OF GIVEN LENGTH
def get_pass(length):
	return "".join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for x in range(length))

	length = int(input("Enter the length of password: "))
	password= get_pass(length)
	print(password)
	pyperclip.copy(password)
	print('Password copied to clipboard')

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
	#c.execute("DELETE FROM password_table")
	c.execute("INSERT INTO password_table (name, pswd) VALUES (?, ?)", (name, password))

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
	conn.commit()
	conn.close()
# query_pswd_by_name(name)

def main():
	"""Runs program and handles command line options"""
	p = optparse.OptionParser(description='Generates random keys of given length, returns keys to clipboard when called by name',
							  prog='passbox',
							  usage='passbox [option] [argument]')
	p.add_option('-q', '--query', action='store_true', help='queries existing password by given name and pastes it to your clipboard')
	p.add_option('-n', '--new', action='store_true', help='creates and stores new password and pastes it to your clipboard')

	options, arguments = p.parse_args()
	if options.query:
		name = str(input('Name of desired password: '))
		query_pswd_by_name(name)
	if options.new:
		length = int(input("Enter the length of password: "))
		get_pass(length)
main()




