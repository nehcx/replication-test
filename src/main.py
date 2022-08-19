"""Write results with the best hyperparameter.

Metrics is defined in ../param/default.yaml.
"""
from omegaconf.dictconfig import DictConfig
from hydra import initialize, compose

from waka_variable import Results

with initialize(config_path="../param"):
    default = compose(config_name="default.yaml")
    hyparam = compose(config_name="hyparam.yaml")
default = {
    "corpus_f": default.corpus_f,
    "context_f": default.context_f,
    "id2lemma_f": default.id2lemma_f,
}

config = DictConfig({**default, **hyparam})
res = Results(config)
res.write_()
