// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

#define LENGTH 45 // Maximum length for a word
#define HASH_TABLE_SIZE 100 // Buckets in hash table

// Node for linked list
typedef struct node
{
    char word[LENGTH]; // Word
    struct node *next; // Pointer to next node
}node;

// Prototypes
bool check(const char *word);
bool load(const char *dictionary);
unsigned int size(void);
bool unload(void);
unsigned long hash(unsigned char *str);

// Functios for linked list
node *add_node(node *ptr, char *word);
node *remove_node(node *ptr);

#endif // DICTIONARY_H