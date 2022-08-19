"""Compare results with metacode annotations.

Input: path of results, a csv file.
"""
import pandas as pd
from omegaconf.dictconfig import DictConfig
import waka_variable
from dataclasses import dataclass


@dataclass
class Objectives:
    """Results metacode matching degrees."""

    config: DictConfig
    res: dict

    def __post_init__(self):
        self.res = waka_variable.main(self.config)
        self.res_df = pd.DataFrame()
        self.res_df["bg_id"] = list(zip(*self.res))[0]
        # average similarity among variable
        self.res_df["avg_sim"] = list(zip(*self.res))[1]
        self.res_df = self.res_df[len(self.res_df.bg_id) >= 2]
        with open("../data/id2lemma.json") as fn:
            id2lemma = json.load(fn)
        self.res_df["lemma"] = self.res_df.bg_id.map(
            lambda x: tuple([id2lemma[l][0] for l in x]))
        # reading
        self.res_df["rdg"] = self.res_df.bg_id.map(
            lambda x: tuple([id2lemma[l][1] for l in x]))
        # number of variants
        self.res_df["num"] = self.res_df.bg_id.apply(len)
        self.res_df["pos_match"], self.res_df["group_match"], self.res_df[
            "field_match"] = self.res_df["bg_id"].apply(self._match)

    @staticmethod
    def _match(var_):
        """Check whether match at specific levels.

        :param pair: tuple of str, pseudo lexical variable

        :return pos_match: bool, whether match at pos level
        :return group_match: bool, whether match at group level
        :return field_match: bool, whether match at field level
        """
        assert len(var_) != 1
        first_l_decomp = var_[0].split("-")
        pos_match = all(l.split("-")[1] == first_l_decomp[1] for l in var_)
        group_match = all(
            l.split("-")[1:3] == first_l_decomp[1:2] for l in var_)
        field_match = all(
            l.split("-")[1:4] == first_l_decomp[1:3] for l in var_)
        return pos_match, group_match, field_match

    @classmethod
    def write_(self):
        """Write results csv."""
        self.res_df.to_csv(
            "../artifact/k-{}_alpha-{}_beta-{}_gamma-{}_window_size-{}.csv".format(
                self.config.k, self.config.alpha, self.config.beta,
                self.config.gamma, self.config.window_size),
            index=False)

    @property
    def num_pos_match(self):
        """Obtain number of correct pos level matching."""
        return sum(self.res_df.pos_match.to_list())

    @property
    def num_group_match(self):
        """Obtain number of correct group level matching."""
        return sum(self.res_df.group_match.to_list())

    @property
    def num_field_match(self):
        """Obtain number of correct field level matching."""
        return sum(self.res_df.field_match.to_list())
