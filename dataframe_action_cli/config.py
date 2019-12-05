# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

import os
import yaml

CONFIG_PATHS = [
    "~/.dataframe_action_cli_config.yaml"
]
FILEPATHS = {
    'config': CONFIG_PATHS,
}


def get_config_file(name='config'):
    fn_cands = FILEPATHS[name]
    fn_cands = map(os.path.expanduser, fn_cands)
    try:
        return next(cand for cand in fn_cands if os.path.isfile(cand))
    except StopIteration:
        return None


def get_config(config_fn=None):
    if config_fn is None:
        config_fn = get_config_file()
    if config_fn is None:
        return
    with open(config_fn) as fp:
        config = yaml.safe_load(fp)
    return config


def get_config_and_filepath():
    config_fn = get_config_file()
    if config_fn is None:
        return None, None
    with open(config_fn) as fp:
        config = yaml.safe_load(fp)
    return config, config_fn
