
book = input("Text:")

n=len(book)
sumwords=0
sumsentence=0
sumletters=0


for i in range(0,n):
    if book[i]=='.' or book[i]=='!':

        sumsentence += 1;

    elif book[i]=='?':

        sumsentence += 1


    if book[i]==' ':

        sumwords += 1


    if book[i] >= 'A' and book[i] <= 'Z':

        sumletters += 1

    elif book[i] >= 'a' and book[i] <= 'z':

        sumletters += 1

sumwords += 1

averagesentence = (sumsentence/sumwords)*100
averageletters=(sumletters/sumwords)*100



index = 0.0588 * averageletters - 0.296 * averagesentence - 15.8;

grade=round(index)

if grade < 1:
    print("Before Grade 1")

elif grade >= 16:
    print("Grade 16+")
else:
    print("Grade",grade)

