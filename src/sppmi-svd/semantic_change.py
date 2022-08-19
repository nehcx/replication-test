import argparse
import numpy as np
from logging import basicConfig, getLogger, DEBUG
import json
from tqdm import tqdm

from util import load_pickle


def main(args):
    """Find top n most changed word."""
    basicConfig(format="%(asctime)s %(message)s", level=DEBUG)
    logger = getLogger(__name__)
    logger.info(f"[INFO] args: {args}")

    logger.info("[INFO] Loading id2word...")

    id2word, word2id = load_pickle(args.dic_id2word)
    V = len(id2word)
    for i in range(V, V + V):
        id2word[i] = "_" + id2word[i - V]
    for word in list(word2id.keys()):
        word2id["_" + word] = word2id[word] * 2 + 1

    logger.info("[INFO] Loading model...")

    M = np.load(args.path_model)
    ds = len(M) // 2
    M_before = M[:ds]
    M_after = M[ds:]
    assert len(M_after) == len(M_before)

    id2change = {}

    logger.info("[INFO] Calculating degree of semantic/usage change...")
    for i in tqdm(range(V)):
        a = M_before[i]
        b = M_after[i]
        id2change[id2word[i]] = np.linalg.norm(a - b)
    id2change = dict(sorted(id2change.items(), key=lambda item: item[1]))
    logger.info("[INFO] Writing output...")
    with open(args.path_id2change, "w") as fp:
        fp.write(json.dumps(id2change))
    logger.info("[INFO] Finished all.")


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--dic_id2word", help="path of id2word dict")
    parser.add_argument("-m", "--path_model", help="path of model/matrix file")
    parser.add_argument("-o",
                        "--path_id2change",
                        help="path of id with degree of change")
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
