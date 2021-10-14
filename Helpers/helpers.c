#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    double gray = 0.0;
    float red = 0.0;
    float green = 0.0;
    float blue = 0.0;

    for (int i=0; i < width;i++)
    {
        for (int j=0; j< height;j++)
        {
            red = image[i][j].rgbtRed;
            blue = image[i][j].rgbtBlue;
            green = image[i][j].rgbtGreen;

            gray = (red + blue + green)/3.0;

            gray = round(gray);

            image[i][j].rgbtRed = gray;
            image[i][j].rgbtBlue = gray;
            image[i][j].rgbtGreen = gray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed = 0;
    int sepiaBlue = 0;
    int sepiaGreen = 0;

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            sepiaRed = round(image[i][j].rgbtRed * 0.393 + image[i][j].rgbtBlue * 0.189 + image[i][j].rgbtGreen * 0.769);
            sepiaGreen = round(image[i][j].rgbtRed * 0.349 + image[i][j].rgbtBlue * 0.168 + image[i][j].rgbtGreen * 0.686);
            sepiaBlue = round(image[i][j].rgbtBlue * 0.131 + image[i][j].rgbtRed * 0.272 + image[i][j].rgbtGreen * 0.534);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[width];

    for (int i = 0; i < height; i++)
    {
        for (int j =0; j < width; j++)
        {
            temp[j]= image[i][width -j-1];

        }
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[j].rgbtRed;
            image[i][j].rgbtBlue = temp[j].rgbtBlue;
            image[i][j].rgbtGreen = temp[j].rgbtGreen;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i< height; i++)
    {
        for (int j=0; j<width; j++)
        {
            if (i < height -1 & i > 0)
            {
                if (j < width -1 & j > 0)
                {
                    image[i][j].rgbtRed = round((image[i-1][j-1].rgbtRed + image[i-1][j].rgbtRed + image[i-1][j+1].rgbtRed + image[i][j-1].rgbtRed + image[i][j+1].rgbtRed + image[i+1][j-1].rgbtRed + image[i+1][j].rgbtRed + image[i+1][j+1].rgbtRed)/8);
                    image[i][j].rgbtBlue = round((image[i-1][j-1].rgbtBlue + image[i-1][j].rgbtBlue + image[i-1][j+1].rgbtBlue + image[i][j-1].rgbtBlue + image[i][j+1].rgbtBlue + image[i+1][j-1].rgbtBlue + image[i+1][j].rgbtBlue + image[i+1][j+1].rgbtBlue)/8);
                    image[i][j].rgbtGreen = round((image[i-1][j-1].rgbtGreen + image[i-1][j].rgbtGreen + image[i-1][j+1].rgbtGreen + image[i][j-1].rgbtGreen + image[i][j+1].rgbtGreen + image[i+1][j-1].rgbtGreen + image[i+1][j].rgbtGreen + image[i+1][j+1].rgbtGreen)/8);

                }

            }


        }
    }
    return;
}
