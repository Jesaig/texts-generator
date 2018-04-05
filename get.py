import argparse
import sys
import os
import json

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', nargs='?', default=os.getcwd(),
                    help='Directory with texts to train model')
parser.add_argument('--model', nargs='?',
                    type=argparse.FileType('w', encoding="utf-8"),
                    default=sys.stdout,
                    help='Output file')
parser.add_argument('--lc', nargs='?', const=True, default=False,
                    help='To lowercase')

args = parser.parse_args()

ins = vars(args).get('input_dir')
outs = vars(args).get('model')
lc = vars(args).get('lc')


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


# считывание слов из файла
words = dict()


@static_vars(eof=-1)
@static_vars(file=None)
def get_word():
    s = ""
    while True:
        symb = get_word.file.read(1)
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
    for filename in os.listdir(ins):
        get_word.file = open(ins + '\\' + filename, 'r', encoding="utf-8")
        first = get_word()
        if first == get_word.eof:
            get_word.file.close()
            continue
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
        get_word.file.close()


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


# каждому слову соответствует слово, которое встречается после
# него чаще всего, и его частота
wordsList = list()
wordsFrequency = list()
newWords = dict()


def transfiguration():
    global wordsList, wordsFrequency
    wordsList, wordsFrequency = getLists(frequency)
    for key, value in words.items():
        newWords[key] = getLists(value)


insert_to_dict()
transfiguration()

outs.write(json.dumps([wordsList, wordsFrequency, newWords], ensure_ascii=False))
