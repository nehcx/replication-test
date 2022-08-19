import argparse
import pandas as pd
import logging
from tqdm import tqdm

period_dic = {
    1: "kokin",
    2: "gosen",
    3: "shui",
    4: "goshui",
    5: "kinyo",
    6: "shika",
    7: "sensai",
    8: "shinkokin"
}


def main(args):
    """Split hachidaishu into two."""
    assert type(args.period) == int
    assert type(args.path_docs) == str

    period = period_dic[args.period]

    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    logging.info(f"[INFO] args: {args}")

    logging.info("[INFO] Loading corpus...")

    corpus = pd.read_csv(args.path_docs)
    sub_corpus_a = corpus[corpus.id.str.split(":").map(
        lambda x: int(x[0]) <= args.period)]
    sub_corpus_b = corpus[corpus.id.str.split(":").map(
        lambda x: int(x[0]) > args.period)]
    with open(args.path_output_before,
              mode="wt") as out_f_a,\
        open(args.path_output_after,
             mode="wt") as out_f_b:
        logging.info(f"[INFO] Write poems before {period}.")
        for line in tqdm(sub_corpus_a["source"].str.split(",").tolist()):
            out_f_a.write(" ".join(line) + "\n")
        logging.info(f"[INFO] Write poems after {period}.")
        for line in tqdm(sub_corpus_b["source"].str.split(",").tolist()):
            out_f_b.write(" ".join(line) + "\n")
    logging.info("[INFO] Finished.")


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--path_docs", help="path of docs")
    parser.add_argument("-a", "--path_output_after", help="path of after part")
    parser.add_argument("-b",
                        "--path_output_before",
                        help="path of before part")
    parser.add_argument("-p", "--period", type=int, help="pseudo shift period")
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
