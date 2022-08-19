"""
Count words.

Code source:
https://github.com/a1da4/sppmi-svd/blob/d1648f59a650caafec2f3de7ac30c9aed2a87e75/make_id2word.py
"""

import argparse
from collections import Counter

from ioutils import write_pickle


def main(args):
    word2freq = Counter()

    with open(args.file_path) as fp:
        for line in fp:
            words = line.strip().split()
            for word in words:
                word2freq[word] += 1

    write_pickle(word2freq, args.counter_dic_path)


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file_path",
                        help="the path of word_pos data directory")
    parser.add_argument("-c",
                        "--counter_dic_path",
                        help="the path of output counter directory")
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
