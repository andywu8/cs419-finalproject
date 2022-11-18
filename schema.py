"""
Run this file to create SQL tables
"""
import sqlite3
from sqlite3 import OperationalError

conn = sqlite3.connect('database.db')
c = conn.cursor()

fd = open('schema.sql', 'r')
sqlFile = fd.read()
fd.close()

# all SQL commands (split on ';')
sqlCommands = sqlFile.split(';')

# Execute every command from the input file
for command in sqlCommands:
    # This will skip and report errors
    # For example, if the tables do not yet exist, this will skip over
    # the DROP TABLE commands
    try:
        c.execute(command)
    except OperationalError as msg:
        print("Command skipped: ", msg)