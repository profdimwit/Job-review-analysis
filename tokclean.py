# -*- coding: utf-8 -*-
import nltk
import string
from nltk.corpus import stopwords


def tokenize_me(file_text):
    # nltk tokenization
    tokens = nltk.word_tokenize(file_text)

    # delete punctuation symbols
    tokens = [i for i in tokens if (i not in string.punctuation)]

    # making everything lowercase
    tokens = [i.lower() for i in tokens]

    # deleting stop_words
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])
    tokens = [i for i in tokens if (i not in stop_words)]

    # cleaning words
    tokens = [i.replace("«", "").replace("»", "").replace('""', '') for i in tokens]



    return tokens
