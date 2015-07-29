"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1)==0:
        return list1
    newlist = []
    newlist.append(list1[0])
    for elem in list1:
        if elem !=newlist[-1]:
            newlist.append(elem)
    return newlist

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    newlist = []
    ind_i,ind_j = 0,0
    while ind_i<len(list1) and ind_j<len(list2):
        if list1[ind_i]<list2[ind_j]:
            ind_i+=1
        elif list2[ind_j]<list1[ind_i]:
            ind_j+=1
        else:
            newlist.append(list1[ind_i])
            ind_i+=1
            ind_j+=1
    return newlist

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    newlist = []
    ind_i,ind_j= 0,0

    while ind_i<len(list1) and ind_j<len(list2):
        if list1[ind_i]<list2[ind_j]:
            newlist.append(list1[ind_i])
            ind_i+=1

        elif list2[ind_j]<list1[ind_i]:
            newlist.append(list2[ind_j])
            ind_j+=1
        else:
            newlist.append(list1[ind_i])
            ind_i+=1
            
            
    
    #print i,j
    if ind_i ==len(list1):
        newlist +=list2[ind_j:]

    elif ind_j ==len(list2):
        newlist+=list1[ind_i:]

    return newlist
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    #base case:
    if len(list1)==1 or len(list1)==0:
        return list1
    else:
    #recursive
        middle = len(list1)/2
        left = list1[0:middle]
        right = list1[middle:]
        left_sorted = merge_sort(left)
        right_sorted = merge_sort(right)
        return merge(left_sorted,right_sorted)    

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    #base case
    if len(word)==0:
        return ['']
    else:
        single = word[0]
        remaining = word[1:]
        strings_from_remaining = gen_all_strings(remaining)
        strings_all = []
        for genword in strings_from_remaining:
            for ind_i in range(len(genword)):
                strings_all.append(genword[0:ind_i]+single+genword[ind_i:])
            strings_all.append(genword+single)
        return strings_all+strings_from_remaining
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    words = []
    for line in netfile.readlines():
        words.append(line.strip())

    return words


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    #print words[0:10]
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
