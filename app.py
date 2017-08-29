import sqlite3

#connect to main database, create new in not exist
conn = sqlite3.connect('main.db')
cursor = conn.cursor()

# create tables if not exist
fd = open('script.sql', 'r')
sqlScriptFile = fd.read()
fd.close()

sqlScript = sqlScriptFile.split(';')

for command in sqlScript:
    try:
        result = cursor.execute(command)
        
    except sqlite3.OperationalError as msg:
        print("Error: ", msg)
        
# main content

conn.commit()
conn.close()