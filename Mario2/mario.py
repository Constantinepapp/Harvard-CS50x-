from cs50 import get_int

height = -1

while height<1 or height>8:
    height = get_int("Height: ")

if height >= 1 and height <= 8:

    for i in range(1,height + 1):
        spaces = height - i
        hashes = i
        print(" "*spaces+"#"*hashes)

        i = i + 1



