import sqlite3

#connect to main database, create new in not exist
conn = sqlite3.connect('main.db')
cursor = conn.cursor()

#open init sql script
with open('deploy/destroy.sql', 'r') as file:
    sqlCommandFile = file.read().split(';')
    
    for command in sqlCommandFile:
        try:
            cursor.execute(command)
            
        except sqlite3.OperationalError as msg:
            print("Error during initialization SQL script: ", msg)

conn.commit()
conn.close()