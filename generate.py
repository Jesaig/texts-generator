import numpy as np
import argparse
import sys
import json
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('--model', nargs='?',
                    type=argparse.FileType('r', encoding="utf-8"),
                    default=sys.stdin,
                    help='Model file')
parser.add_argument('--output', nargs='?',
                    type=argparse.FileType('w', encoding="utf-8"),
                    default=sys.stdout,
                    help='Output file')
parser.add_argument('--length', nargs='?',
                    type=int,
                    default=200,
                    help='Generated text length (in words)')
parser.add_argument('--seed', nargs='?',
                    type=str,
                    default=-1,
                    help='First word')

args = parser.parse_args()

ins = vars(args).get('model')
outs = vars(args).get('output')

data = json.load(ins)
wordsList = data[0]
wordsFrequency = data[1]
newWords = data[2]


def getFirstWord():
    return np.random.choice(wordsList, 1, wordsFrequency)[0]


def getWord(word=-1):
    if word not in newWords or newWords[word][0].__len__ == 0:
        return getFirstWord()
    return np.random.choice(newWords[word][0], 1, newWords[word][1])[0]


def genText(len, firstWord):
    if (firstWord != -1):
        len -= 1
        outs.write("%s " % firstWord)
    word = getWord(firstWord)
    outs.write("%s " % word)
    for i in range(len - 1):
        word = getWord(word)
        outs.write("%s " % word)

genText(vars(args).get('length'), vars(args).get('seed'))
