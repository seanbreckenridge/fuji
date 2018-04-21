#!/usr/local/env python3
from random import randint, sample, choice
from os import path

alpha_words_file = path.join(path.dirname(__file__), 'short_alpha_words.txt')

def generate(name_length):
    """Generates a random username and password"""
    pw_chars = r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    with open(alpha_words_file, 'r') as f:
        words = set(map(lambda s: s.strip(), f.readlines())) # readlines
    username = ''.join(w.capitalize() for w in sample(words, name_length)) + str(randint(100,1000))
    password = ''.join(choice(pw_chars) for i in range(randint(11, 20)))
    return username, password
