from cs50 import SQL
from sys import argv
import pandas


db = SQL("sqlite:///students.db")


students = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last", argv[1])

for person in students:

    if person['middle'] is None:
        print(person['first'],person['last'],"born",person['birth'])
    else:
        print(person['first'],person['middle'],person['last'],"born",person['birth'])