import sqlite3

#connect to main database, create new in not exist
conn = sqlite3.connect('main.db')
cursor = conn.cursor()

# create tables if not exist
sql = ''' CREATE TABLE IF NOT EXIST '''

# main content


conn.commit()
conn.close()