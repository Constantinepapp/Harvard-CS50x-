#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // check if number of arguments is 2 (if not, throw error code 1)
    if(argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        // convert 2nd argument from string to int
        int key = atoi(argv[1]);

        // get plaintext from user
        printf("plaintext: ");
        string s = get_string("input");

        // iterate plaintext and check if current character is a letter, lower or upper case..
        printf("ciphertext: ");
        for(int i = 0, l = strlen(s); i < l; i++)
        {
            if(isalpha(s[i]))
            {
                if(islower(s[i]))
                {
                    if(s[i] + key > 122)
                    {

                        printf("%c", (s[i] - 97 + key) % 26 + 97);
                    }

                    else
                    {
                        printf("%c", s[i] + key);
                    }
                }
                else if(isupper(s[i]))
                {
                    if(s[i] + key > 90)
                    {
                        printf("%c", (s[i] - 65 + key) % 26);
                    }
                    else
                    {
                        printf("%c", s[i] + key);
                    }
                }
            }
            else
            {
                printf("%c", s[i]);
            }
        }
        printf("\n");
        return 0;
    }
}