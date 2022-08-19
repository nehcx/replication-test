"""External uniformity value.

Test
"""

import pandas as pd
import argparse
from collections import Counter
from logging import basicConfig, getLogger, DEBUG

basicConfig(format="%(asctime)s %(message)s", level=DEBUG)
logger = getLogger(__name__)


def load_data(tar_vars, before_f, after_f):
    """Load data."""
    with open(before_f) as bf,\
         open(after_f) as af:
        words_b, words_a = [], []
        for line in bf:
            words_b += line.strip("\n").split(" ")
        for line in af:
            words_a += line.strip("\n").split(" ")

    before_d = Counter(words_b)
    after_d = Counter(words_a)
    return pd.read_csv(tar_vars), before_d, after_d


def ex_uni_var(var_, before_d, after_d):
    """Calculate external uniformaty value of a lexical variable.

    :param var_: str of tuple, lexical variable.
    :param before_d: Counter, text dataset before target period.
    :param after_d: Counter, text dataset after targert period.

    :return before_per: tuple, relative frequency of variants in before.
    :return after_per: tuple, relative frequency of variants in after.
    :return value: external uniformaty.
    """
    var_ = eval(var_)

    def freq_gen(b_or_a):
        for lex in var_:
            yield b_or_a[lex]

    before_lst = list(freq_gen(before_d))
    after_lst = list(freq_gen(after_d))
    before_tup = [i / sum(before_lst) for i in before_lst]
    after_tup = [i / sum(after_lst) for i in after_lst]
    value = 0
    for i in range(len(var_)):
        value += min(before_tup[i], after_tup[i])
    before_tup = tuple(map(lambda x: float(str(round(x, 3))), before_tup))
    after_tup = tuple(map(lambda x: float(str(round(x, 3))), after_tup))
    return before_tup, after_tup, value


def main(args):
    logger.info("[INFO] load data...")
    vars_df, before_d, after_d = load_data(args.path_vars, args.path_before,
                                           args.path_after)
    logger.info("[INFO] computing...")
    vars_df["period_a_dist"], vars_df["period_b_dist"], vars_df[
        "external_uniformity"] = tuple(
            zip(*vars_df.apply(
                lambda row: ex_uni_var(row.bg_id, before_d, after_d), axis=1)))
    vars_df = vars_df.sort_values(by=['external_uniformity'])
    vars_df.to_csv(f"../artifact/{args.path_out}")
    logger.info("[INFO] finished.")


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--path_vars", help="path of lexical variables")
    parser.add_argument("-b", "--path_before", help="path of before part")
    parser.add_argument("-a", "--path_after", help="path of after part")
    parser.add_argument("-o", "--path_out", help="path of after part")
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
