#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 13:02:28 2021

@author: jason
"""

import random
import string


WORDLIST_FILENAME = "words.txt"

def load_words():
    '''
    returns: list, a list of valid words. Words are strings of lowercase letters.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    '''
    wordlist (list): list of words (strings)

    returns: a word from wordlist at random
    '''
    return random.choice(wordlist)



# Load the list of words to be accessed from anywhere in the program
wordlist = load_words()

def check_victory(secret_word, letters_guessed):
    '''
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    '''
    l1 = list(secret_word) #turn word into list
    l2 = list(letters_guessed) #turn letters into list
    if all([x in l2 for x in l1]) == True: #returns True if all letters in letters_guessed is found in secret_word
        return True #if letters are in word, great!
    else:
        return False #if letters are not in word, bad!


def get_word_progress(secret_word, letters_guessed):
    '''
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters and underscores (_) that represents
      which letters in secret_word have not been guessed so far
    '''
    word = ""
    for character in secret_word:
        if character not in letters_guessed:
            word += "_" #if character has not been guessed yet, then add "_"
        else:
            word += character #if characters has been guessed, then reveal letter
    
    return word #return a combination of _ and letters


def get_remaining_letters(letters_guessed):
    '''
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
      letters have not yet been guessed. The letters should be returned in
      alphabetical order
    '''
    list1 = list(string.ascii_lowercase) #turn all characters (lowercase) into list
    for letter in string.ascii_lowercase:
        if letter in letters_guessed:
            list1.remove(letter) #remove letter from list of remaining letters 
    result =''.join(list1) #joins all letters in list into empty string
    
    return result

        
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.
    '''
    guesses_remaining = 10
    number_of_letters = len(secret_word)
    letters_guessed = []
    print("Welcome to Hangman!")
    print("I am thinking of a word that is " + str(number_of_letters) + " long.")
    print("--------------")
    unique_letters = []
    for character in secret_word:
        if character in unique_letters:
            something = 0
        else:
            unique_letters.append(character)
            number_of_unique_letters = len(unique_letters)
    while not check_victory(secret_word, letters_guessed) and guesses_remaining > 0:
        print("You have " + str(guesses_remaining) + " guesses left.")
        print("Available letters: " + get_remaining_letters(letters_guessed))
        guess = input("Please guess a letter: ")
        if guess not in string.ascii_lowercase or guess == " ":
            print("Oops! That is not a valid letter. Please input a letter from the alphabet: ", get_word_progress(secret_word, letters_guessed))
            print("--------------")
        else:
            guess=guess.lower()
            if guess in secret_word and guess not in letters_guessed:
                letters_guessed.append(guess)
                print("Good guess: " + get_word_progress(secret_word, letters_guessed))
                print("--------------")
            elif guess in letters_guessed:
                print("Oops! You've already guessed that letter: " + get_word_progress(secret_word, letters_guessed))
                print("--------------")
            else:
                letters_guessed.append(guess)
                print("Oops! That letter is not in my word: " + get_word_progress(secret_word, letters_guessed))
                guesses_remaining -= 1
                print("--------------")
    if check_victory(secret_word, letters_guessed):
        print("Congratulations, you won!")
        print("Your total score for this game is: " + str((2*guesses_remaining + 3*(len(secret_word) + number_of_unique_letters))))
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)


def hangman_with_help(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.
    '''
    guesses_remaining = 10
    number_of_letters = len(secret_word)
    letters_guessed = []
    print("Welcome to Hangman!")
    print("I am thinking of a word that is " + str(number_of_letters) + " long.")
    print("--------------")
    unique_letters = []
    for character in secret_word:
        if character in unique_letters:
            something = 0 #do nothing
        else:
            unique_letters.append(character) #goes through word and appends letter only once
            number_of_unique_letters = len(unique_letters)
    while not check_victory(secret_word, letters_guessed) and guesses_remaining > 0: #keep going through loop unless victory or no more guesses
        print("You have " + str(guesses_remaining) + " guesses left.")
        print("Available letters: " + get_remaining_letters(letters_guessed))
        guess = input("Please guess a letter: ")
        if guess == "!": #get a hint
            x = choose_letter(secret_word, get_remaining_letters(letters_guessed)) #random letter is generated that is in word
            print("Letter revealed: " + x)
            letters_guessed.append(x) #append letter to letters guessed
            print(get_word_progress(secret_word, letters_guessed))
            print("--------------")
            guesses_remaining -= 2
        elif guess not in string.ascii_lowercase or guess == " ": #when input is nota lowercase letter
            print("Oops! That is not a valid letter. Please input a letter from the alphabet: ", get_word_progress(secret_word, letters_guessed))
            print("--------------")
        else:
            guess=guess.lower() #make letter turn into lowercase
            if guess in secret_word and guess not in letters_guessed:
                letters_guessed.append(guess) #when letter is not in secret word and has not already been guessed, then append letter to word
                print("Good guess: " + get_word_progress(secret_word, letters_guessed))
                print("--------------")
            elif guess in letters_guessed: #if guess has already been guessed, then print
                print("Oops! You've already guessed that letter: " + get_word_progress(secret_word, letters_guessed))
                print("--------------")
            else: #if guess is not in word, then append letter to list of letters guessed
                letters_guessed.append(guess)
                print("Oops! That letter is not in my word: " + get_word_progress(secret_word, letters_guessed))
                guesses_remaining -= 1 #lose a guess
                print("--------------")
    if check_victory(secret_word, letters_guessed): #after going through while loop, if the guesses amounted to the word, then success
        print("Congratulations, you won!")
        print("Your total score for this game is: " + str((2*guesses_remaining + 3*(len(secret_word) + number_of_unique_letters)))) #calculate score
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)


def choose_letter(secret_word, letters_remaining):
    unique_letters = []
    for character in secret_word:
        if character not in unique_letters and character in letters_remaining:
            unique_letters.append(character) #append letters that are in word that has not been guessed to a list
    new = random.randint(0, len(unique_letters)-1) #return a random number between 0 and number of characters in word
    revealed_letter = unique_letters[new] #reveal that character related to number
    return revealed_letter

# if __name__ == "__main__"

#     secret_word = choose_word(wordlist)
#     hangman(secret_word)

# ###############

#     secret_word = choose_word(wordlist)
#     hangman_with_help('wildcard')

#     pass
