"""Search hyperparameters.

n_trial is defined in ../param/default.yaml.
"""
import yaml
import pandas as pd
import optuna
from omegaconf.dictconfig import DictConfig
from hydra import initialize, compose

from waka_variable import Results

with initialize(config_path="../param"):
    default = compose(config_name="default.yaml")


def objective(trial):
    """Study objectives."""
    umap_params = {
        "window_size":
        trial.suggest_int('window_size', 2, 3),
        "only_content_feature":
        trial.suggest_categorical('only_content_feature', [True, False]),
        "top_n_feature":
        trial.suggest_int('top_n_feature', 2000, 3000, step=1000),
        "top_n_target":
        trial.suggest_int('top_n_target', 500, 1000, step=500),
        # trial.suggest_int('top_n_feature', 2000, 3000, step=500),
        "k":
        trial.suggest_int('k', 100, 100),
        "alpha":
        trial.suggest_float('alpha', 0.2, 0.6, step=0.2),
        "beta":
        trial.suggest_float('beta', 0.4, 0.8, step=0.2),
        "gamma":
        trial.suggest_float('gamma', 0.2, 0.6, step=0.2)
    }
    default_params = {
        "corpus_f": default.corpus_f,
        "context_f": default.context_f,
        "id2lemma_f": default.id2lemma_f,
    }
    config = DictConfig({**default_params, **umap_params})
    res = Results(config)
    res.write_()
    return res.pos_match_num, res.group_match_num, res.field_match_num, \
        res.pos_match_per, res.group_match_per, res.field_match_per


# search hyperparameters
study = optuna.create_study(directions=[
    "maximize", "maximize", "maximize", "maximize", "maximize", "maximize"
],
                            sampler=optuna.samplers.TPESampler(seed=123))
study.optimize(
    objective,
    # timeout=default.timeout,
    n_trials=default.n_trials)

# write trial table
df = study.trials_dataframe()
df = df.rename(
    columns={
        "values_0": "pos_match_num",
        "values_1": "group_match_num",
        "values_2": "field_match_num",
        "values_3": "pos_match_per",
        "values_4": "group_match_per",
        "values_5": "field_match_per",
        "params_alpha": "alpha",
        "params_beta": "beta",
        "params_gamma": "gamma",
        "params_k": "k",
        "params_only_content_feature": "only_content_feature",
        "params_top_n_feature": "top_n_feature",
        "params_top_n_target": "top_n_target",
        "params_window_size": "window_size"
    })
df.to_csv("../cache/log.csv")
df = df[df[default.metrics] == df[default.metrics].max()][[
    "alpha", "beta", "gamma", "k", "only_content_feature", "top_n_feature",
    "top_n_target", "window_size"
]]
with open('../param/hyparam.yaml', 'w') as fn:
    yaml.dump(df.to_dict('records')[0], fn, default_flow_style=False)
