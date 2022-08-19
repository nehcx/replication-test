import yaml
import pandas as pd

df = pd.read_csv("../cache/log.csv")
df = df[df["group_match_per"] == df["group_match_per"].max()][[
    "alpha", "beta", "gamma", "k", "only_content_feature", "top_n_feature",
    "top_n_target", "window_size"
]]
with open('../param/hyparam.yaml', 'w') as fn:
    yaml.dump(df.to_dict('records')[0], fn, default_flow_style=False)
