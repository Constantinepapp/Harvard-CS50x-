#include <cs50.h>
#include <stdio.h>

int main(void)
{   
    // initializes height
    int height = 0;

    // checks if user input is valid
    do
    {

        height = get_int("Height:");
    
    }
    while (height < 1 || height > 8);

    //creates rows
    for (int i = 0; i < height; i++)
    {
        //create columns
        for (int j = 1; j <= height; j++)
        {
            if (j >= height - i)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
            
        }
        printf("\n");
    }
}
