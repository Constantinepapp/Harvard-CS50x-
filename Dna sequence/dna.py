from sys import argv
import sys
from csv import reader,DictReader
import pandas
import re


with open(argv[2]) as file:
    dna_reader=reader(file)
    dna_array=[]
    for line in dna_reader:
        dna_array.append(line)




df_people = pandas.read_csv(argv[1])

sequence=[]

for col in df_people:
    sequence.append(col)


genes=[]
for item in sequence:
    genes.append(item)



indice_AGATC=[]


if not "TTTTTTCT" in df_people:
    indice_AGATC=[]

    for item in dna_array:
        for word in item:
            for m in re.finditer("AGATC", word):
                x = m.start()
                indice_AGATC.append(x)


    target_AGATC=[]
    for i in range(1,len(indice_AGATC)):
        target_AGATC.append(indice_AGATC[i]-indice_AGATC[i-1])




    indice_AATG=[]

    for item in dna_array:
        for word in item:
            for m in re.finditer("AATG", word):
                x = m.start()
                indice_AATG.append(x)


    target_AATG=[]
    for i in range(1,len(indice_AATG)):
        target_AATG.append(indice_AATG[i]-indice_AATG[i-1])






    indice_TATC=[]

    for item in dna_array:
        for word in item:
            for m in re.finditer("TATC", word):
                x = m.start()
                indice_TATC.append(x)


    target_TATC=[]
    for i in range(1,len(indice_TATC)):
        target_TATC.append(indice_TATC[i]-indice_TATC[i-1])



    sum_AGATC = 1
    sum_AATG = 1
    sum_TATC = 1


    for i in range(0,len(target_AGATC)):
        if target_AGATC[i] == 5:
            sum_AGATC = sum_AGATC +1


    for i in range(0,len(target_AATG)):
        if target_AATG[i] == 4:
            sum_AATG = sum_AATG +1

    for i in range(0,len(target_TATC)):
        if target_TATC[i] == 4:
            sum_TATC = sum_TATC +1




    for i in range(0,len(df_people['AGATC'])):
        if sum_AGATC == df_people['AGATC'][i]:
            print (df_people['name'][i])




    for i in range(0,len(df_people['AATG'])):
        if sum_AATG == df_people['AATG'][i]:
           pass#print (df_people['name'][i])



    for i in range(0,len(df_people['TATC'])):
        if sum_TATC == df_people['TATC'][i]:
            pass#print (df_people['name'][i])








    sys.exit()









for item in dna_array:
    for word in item:
        for m in re.finditer("AGATC", word):
            x = m.start()
            indice_AGATC.append(x)


target_AGATC=[]
for i in range(1,len(indice_AGATC)):
    target_AGATC.append(indice_AGATC[i]-indice_AGATC[i-1])







indice_TTTTTTCT=[]

for item in dna_array:
    for word in item:
        for m in re.finditer("TTTTTTCT", word):
            x = m.start()
            indice_TTTTTTCT.append(x)


target_TTTTTTCT=[]
for i in range(1,len(indice_TTTTTTCT)):
    target_TTTTTTCT.append(indice_TTTTTTCT[i]-indice_TTTTTTCT[i-1])







indice_AATG=[]

for item in dna_array:
    for word in item:
        for m in re.finditer("AATG", word):
            x = m.start()
            indice_AATG.append(x)


target_AATG=[]
for i in range(1,len(indice_AATG)):
    target_AATG.append(indice_AATG[i]-indice_AATG[i-1])










indice_TCTAG=[]

for item in dna_array:
    for word in item:
        for m in re.finditer("TCTAG", word):
            x = m.start()
            indice_TCTAG.append(x)


target_TCTAG=[]
for i in range(1,len(indice_TCTAG)):
    target_TCTAG.append(indice_TCTAG[i]-indice_TCTAG[i-1])






indice_GATA=[]

for item in dna_array:
    for word in item:
        for m in re.finditer("GATA", word):
            x = m.start()
            indice_GATA.append(x)


target_GATA=[]
for i in range(1,len(indice_GATA)):
    target_GATA.append(indice_GATA[i]-indice_GATA[i-1])








indice_TATC=[]

for item in dna_array:
    for word in item:
        for m in re.finditer("TATC", word):
            x = m.start()
            indice_GATA.append(x)


target_TATC=[]
for i in range(1,len(indice_TATC)):
    target_TATC.append(indice_TATC[i]-indice_TATC[i-1])











indice_GAAA=[]

for item in dna_array:
    for word in item:
        for m in re.finditer("GAAA", word):
            x = m.start()
            indice_GAAA.append(x)


target_GAAA=[]
for i in range(1,len(indice_GAAA)):
    target_GAAA.append(indice_GAAA[i]-indice_GAAA[i-1])









indice_TCTG=[]

for item in dna_array:
    for word in item:
        for m in re.finditer("TCTG", word):
            x = m.start()
            indice_TCTG.append(x)


target_TCTG=[]
for i in range(1,len(indice_TCTG)):
    target_TCTG.append(indice_TCTG[i]-indice_TCTG[i-1])



#print(target_AGATC, target_TTTTTTCT, target_AATG,target_TCTAG,target_GATA,target_GAAA,target_TCTG)

sum_AGATC = 1
sum_TTTTTTCT = 1
sum_AATG = 1
sum_TCTAG = 1
sum_GATA = 1
sum_GAAA = 1
sum_TCTG = 1
sum_TATC = 1


for i in range(0,len(target_AGATC)):
    if target_AGATC[i] == 5:
        sum_AGATC = sum_AGATC +1

for i in range(0,len(target_TTTTTTCT)):
    if target_TTTTTTCT[i] == 8:
        sum_TTTTTTCT = sum_TTTTTTCT +1

for i in range(0,len(target_AATG)):
    if target_AATG[i] == 4:
        sum_AATG = sum_AATG +1

for i in range(0,len(target_TATC)):
    if target_TATC[i] == 4:
        sum_TATC = sum_TATC +1


for i in range(0,len(target_TCTAG)):
    if target_TCTAG[i] == 5:
        sum_TCTAG = sum_TCTAG +1

for i in range(0,len(target_GATA)):
    if target_GATA[i] == 4:
        sum_GATA = sum_GATA +1

for i in range(0,len(target_GAAA)):
    if target_GAAA[i] == 4:
        sum_GAAA = sum_GAAA +1

for i in range(0,len(target_TCTG)):
    if target_TCTG[i] == 4:
        sum_TCTG = sum_TCTG +1





x=0
for i in range(0,len(df_people['AGATC'])):
    if sum_AGATC == df_people['AGATC'][i]:
        if sum_TTTTTTCT == df_people['TTTTTTCT'][i]:
            if sum_AATG == df_people['AATG'][i]:
                print (df_people['name'][i])
                x=1
if x==0:
    print("No match")



for i in range(0,len(df_people['TTTTTTCT'])):
    if sum_TTTTTTCT == df_people['TTTTTTCT'][i]:
        pass
        #print (df_people['name'][i])



for i in range(0,len(df_people['AATG'])):
    if sum_AATG == df_people['AATG'][i]:
       pass#print (df_people['name'][i])


for i in range(0,len(df_people['TCTAG'])):
    if sum_TCTAG == df_people['TCTAG'][i]:
        pass#print (df_people['name'][i])




for i in range(0,len(df_people['GATA'])):
    if sum_GATA == df_people['GATA'][i]:
        pass#print (df_people['name'][i])



for i in range(0,len(df_people['TATC'])):
    if sum_TATC == df_people['TATC'][i]:
        pass#print (df_people['name'][i])



for i in range(0,len(df_people['GAAA'])):
    if sum_GAAA == df_people['GAAA'][i]:
        pass#print (df_people['name'][i])




for i in range(0,len(df_people['TCTG'])):
    if sum_TCTG == df_people['TCTG'][i]:
        pass#print (df_people['name'][i])

































