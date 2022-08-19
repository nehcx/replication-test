"""
Load data.

Code source:
https://github.com/a1da4/pmi-semantic-difference/blob/main/preprocess/coha-preprocess/ioutils.py
"""
import pickle


def write_pickle(data, filename):
    fp = open(filename, "wb")
    pickle.dump(data, fp)


def load_pickle(filename):
    fp = open(filename, "rb")
    return pickle.load(fp)
