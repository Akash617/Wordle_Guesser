import copy
import string
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pyautogui


driver = webdriver.Firefox()
driver.get("https://www.wordleunlimited.com/")
words = []
elsewhere = []
correct = []
correct_letters = 0
guess_number = 0
letter_frequency = list(("EAROTLISNCUYDHPMGBFKWVZXQJ").lower())  # Frequency list to priortize guessing

# Copies the text file with possible guesses into a wordlist
with open("words.txt", "r") as f:
    line = f.readline()
    words = line.split(",")


# Removes words with an incorrect letter
def remove_words(letter):
    global words, elsewhere, correct

    # Ensures that it doesn't remove incorrect repeated letters that are elsewhere or correct
    if not (any(letter in letters for letters in elsewhere) or any(letter in letters for letters in correct)):
        words = [x for x in words if letter not in x]


# Ensures all possible words have that letter in them but that they are not in the same position
def confirmed_elsewhere(letter, index):
    global words
    words = [x for x in words if letter in x]
    words = [x for x in words if letter not in x[index]]


# Ensures all possible words have this letter in the exact position
def confirmed_correct(letter, index):
    global words
    words = [x for x in words if letter in x[index]]


def type(list):
    for i in list:
        pyautogui.press(i)

    pyautogui.press("enter")
    time.sleep(1)  # Gives sufficient time to input next word


def guess(word):
    global alphabet_list, letter_frequency, guess_number, correct_letters, elsewhere, correct
    correct_letters = 0  # Used to stop guessing if correct word is found
    guess = list(word)
    type(guess)

    # Find the results of the latest guess
    list1 = (driver.find_elements(By.CLASS_NAME, "RowL-letter"))[(guess_number*5):(guess_number*5 + 5)]

    # Go through the result to update the word list
    for i in list1:
        letter = guess[list1.index(i)]
        index = guess.index(letter)
        response = i.get_attribute("class")

        if "elsewhere" in response:
            elsewhere.append([letter, index])
            confirmed_elsewhere(letter, index)
        elif "correct" in response:
            correct_letters += 1
            correct.append([letter, index])
            confirmed_correct(letter, index)
        elif "absent" in response:
            letter_frequency = [x for x in letter_frequency if letter != x]
            remove_words(letter)

    guess_number += 1  # Used to identify the elements of the results of the latest guess


def next_guess():
    # Using temporary lists to whittle down words by frequency
    tmp_words = copy.deepcopy(words)
    tmp_freq = copy.deepcopy(letter_frequency)
    backup_words = copy.deepcopy(tmp_words)

    while len(tmp_words) > 1:
        backup_words = copy.deepcopy(tmp_words)
        tmp_words = [x for x in tmp_words if tmp_freq[0] in x]
        tmp_freq.pop(0)

    if len(tmp_words) == 0:
        tmp_words = copy.deepcopy(backup_words)

    print("Certainty of guess: " + str((1 / len(words)) * 100) + "%")  # Shows how random the guess is
    guess(random.choice(tmp_words))


guess("orate")

while correct_letters != 5:
    next_guess()
