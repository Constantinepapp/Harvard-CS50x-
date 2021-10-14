import cs50
change = - 1.0


change=-1

while change < 0:
    change = float(input("Change owed:"))



coin = 0

change=change*100

while change >= 1:
    while change - 25 >= 0.00:

        if change >= 25:
            change = change - 25
            coin = coin + 1


    while change - 10 >= 0.00:

        if change >= 10:

            change = change - 10
            coin = coin + 1


    while change - 5 >= 0.00:

        if change >= 5:

            change = change - 5
            coin = coin + 1


    while change - 1 >= 0.00:

        if change >= 1:

            change = change - 1
            coin = coin + 1





print(coin)


