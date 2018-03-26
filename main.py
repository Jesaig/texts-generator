import numpy as np
from get import *

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


# считывание слов из файла
words = dict()
@static_vars(eof = -1)
def get_word():
    s = ""
    while True:
        symb = ins.read(1)
        if symb == "":
            if s != "":
                break
            return get_word.eof
        if s != "" and (symb == " " or symb == "\n"):
            break
        if symb.isalpha() or symb == '-':
            if lc:
                s += symb.lower()
            else:
                s += symb
    if s not in words:
        words[s] = dict()
    return s


# вставляем слова в словарь словарей
frequency = dict()
def insert_to_dict():
    first = get_word()
    frequency[first] = 1
    while True:
        second = get_word()
        if second == get_word.eof:
            break
        if second not in words[first]:
            words[first][second] = 0
        words[first][second] += 1
        if second not in frequency:
            frequency[second] = 0
        frequency[second] += 1
        first = second


def getLists(d):
    dList = list()
    dFrequency = list()
    dWords = 0
    for key, value in frequency.items():
        dWords += value
    for key, value in frequency.items():
        dList.append(key)
        dFrequency.append(value / dWords)
    return (dList, dFrequency)


# какждому слову соответствует слово, которое встречается после него чаще всего, и его частота
wordsList = list()
wordsFrequency = list()
newWords = dict()
def transfiguration():
    global wordsList, wordsFrequency
    wordsList, wordsFrequency = getLists(frequency)
    for key, value in words.items():
        newWords[key] = getLists(value)


def getFirstWord():
    return np.random.choice(wordsList, 1, wordsFrequency)[0]


def getWord(word = -1):
    if word not in newWords or newWords[word][0].__len__ == 0:
        return getFirstWord()
    return np.random.choice(newWords[word][0], 1, newWords[word][1])[0]


def genText(len):
    if len == 0:
        return
    word = getWord()
    outs.write("%s " % word)
    for i in range(len - 1):
        word = getWord(word)
        outs.write("%s " % word)
    outs.write('\n')


insert_to_dict()
transfiguration()

genText(200)
