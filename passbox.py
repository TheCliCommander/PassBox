import random
import secrets 
import string
import sqlite3
import pyperclip

#CREATE PASSWORD OF GIVEN LENGTH
def get_pass(length):
		return "".join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for x in range(length))

length = int(input("Enter the length of password: "))
password= get_pass(length)
print(password)


name = str(input("Enter name for password: "))

#CREATE DATABASE CONNECTION
conn = sqlite3.connect("*****.db")

#CREATE CURSOR OBJECT
c = conn.cursor()

#CREATE TABLE IN DISK FILE BASED DATABASE
c.execute("""CREATE TABLE IF NOT EXISTS password_table (
						name TEXT,
						pswd TEXT
						)""")
c.execute("DELETE FROM password_table")
c.execute("INSERT INTO password_table (name, pswd) VALUES (?, ?)", (name, password))

#COMMIT CHANGES
conn.commit()
conn.close()

def query_pswd_by_name(name):
	conn = sqlite3.connect('.*****.db')
	c = conn.cursor()
	query_password = "SELECT pswd FROM password_table WHERE name = ?"
	c.execute(query_password,(name,))
	result = c.fetchall()
	for row in result:
		pyperclip.copy(str(row[0]))
		print("Password copied to clipboard")
	conn.commit()
query_pswd_by_name(name)



#CLOSE CONNECTION
conn.close()



