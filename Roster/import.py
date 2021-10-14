import pandas
from sys import argv
from cs50 import SQL

db = SQL("sqlite:///students.db")


df_people = pandas.read_csv(argv[1])

for row in range(0,len(df_people)):
    birth=str(df_people['birth'][row])
    name_list=df_people['name'][row].split()

    #print(name['house'],"-----------------------")

    if len(name_list) < 3:

        db.execute('INSERT INTO students (first,middle,last,house,birth) VALUES (?,?,?,?,?)',name_list[0],None,name_list[1],df_people['house'][row],birth)

    else:
        db.execute('INSERT INTO students (first,middle,last,house,birth) VALUES (?,?,?,?,?)',name_list[0],name_list[1],name_list[2],df_people['house'][row],birth)


