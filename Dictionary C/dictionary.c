// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Declare array for hash table
node *table[HASH_TABLE_SIZE];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Declare an array for word
    char term[LENGTH];

    // Copy word and convert to lowercase
    strcpy(term, word);
    for (int i = 0; word[i]; i++)
    {
        term[i] = tolower(word[i]);
    }

    // Get the hash value for word
    int hash_value = hash((unsigned char *) term) % HASH_TABLE_SIZE;

    // Sets list to point that `hash_value` element of table
    node *list = table[hash_value];

    // Iterate over linked list
    while (list != NULL)
    {
        // If word found return
        if (strcmp(list->word, term) == 0)
        {
            return true;
        }

        // Set pointer to next element
        list = list->next;
    }

    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    // Allocate memory for word
    char *word = malloc(sizeof(char) * LENGTH);
    if (word == NULL)
    {
        fclose(dict);
        return false;
    }

    // Iterate over dictionary
    while (fscanf(dict, "%s", word) != EOF)
    {
        // Add word to hash table
        int hash_value = hash((unsigned char *) word) % HASH_TABLE_SIZE;
        table[hash_value] = add_node(table[hash_value], word);
    }

    // Free allocated memory
    free(word);

    // Close dictionary
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // Initialize counter and declare pointer to node
    int counter = 0;
    node *list = NULL;

    // Iterate over the hash table
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        // Set list as pointer to the linked list
        list = table[i];

        // Iterate over the linked list
        while (list != NULL)
        {
            counter++;
            list = list->next;
        }
    }
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Iterate over hash table
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        // Remove linked list connected to the pointer
        while (table[i] != NULL)
        {
            table[i] = remove_node(table[i]);
        }
    }

    return true;
}

// Add new node to the linked list
node *add_node(node *ptr, char *word)
{
    // Allocate memory for new node
    node *new = malloc(sizeof(node));
    if (new == NULL)
    {
        return NULL;
    }

    // Copy word into new node
    strcpy(new->word, word);

    // Update pointer
    new->next = ptr;

    // Return pointer to new node
    return new;
}

// Remove node from the linked list
node *remove_node(node *ptr)
{
    // Temporary pointer to store the next pointer
    node *temp = ptr->next;

    // Free the allocated memory for node
    free(ptr);

    // Return the next pointer
    return temp;
}

// djb2 hash function source: http://www.cse.yorku.ca/~oz/hash.html
unsigned long hash(unsigned char *str)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *str++))
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }

    return hash;
}