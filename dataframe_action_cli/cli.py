# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

import sys
import pandas as pd

from actionista.action_cli_core.action_cli_argv_parser import parse_argv
from .dataframe_actions import ACTIONS as dataframe_actions
from .config_actions import ACTIONS as config_actions
from .help_actions import ACTIONS as help_actions
from .config import get_config

ACTION_COLLECTIONS = {
    'dataframe': dataframe_actions,
    'config': config_actions,
    'help': help_actions,
}


def get_action(action_key):
    for action_type, action_collection in ACTION_COLLECTIONS.items():
        if action_key in action_collection:
            return action_type, action_collection[action_key]
    else:
        raise KeyError(f"action_key '{action_key}' could not be found in any of the action collections.")


def action_cli(argv=None, verbose=0):
    """ CLI to sort and select data from csv file, inspired by actionista todoist-action-cli.

    Examples:

        # Loading data:
        dataframe-action-cli -read <inputfile>
        dataframe-action-cli -read input.csv
        dataframe-action-cli -read input1.csv -read input2.csv

        # Selecting using `select-where`:
        dataframe-action-cli -read-from input.csv -select-where <columnX> matches <regex-pattern>
        dataframe-action-cli -read-from input.csv -select-where name matches "(Peter|Michael)"
        dataframe-action-cli -read-from input.csv -select-where <columnX> glob <glob-pattern>
        dataframe-action-cli -read-from input.csv -select-where <columnX> in <list-of-values>

        # Selecting using `select-query`:
        dataframe-action-cli -read-from input.csv -select-query <query>
        dataframe-action-cli -read-from input.csv -select-query "name in ('Peter', 'Michael')"

        # Creating new columns, using `df.eval`, form 1:
        dataframe-action-cli -read-from input.csv -create-column <columnname> <expression>
        dataframe-action-cli -read-from input.csv -create-column total "amount * price_each"
        # Creating new columns, using `df.eval`, form 2:
        dataframe-action-cli -read-from input.csv -create-column <expression>
        dataframe-action-cli -read-from input.csv -create-column "total = amount * price_each"

    """
    (base_args, base_kwargs), action_groups = parse_argv()

    config = get_config() or {}
    config.update(base_kwargs)

    config.setdefault('verbosity', 1)

    if len(action_groups) == 0:
        # Print default help
        action_groups.append(('help', [], {}))

    # For each action in the action chain, invoke the action providing the (remaining) tasks as first argument.
    dataframe = pd.DataFrame()

    for action_key, action_args, action_kwargs in action_groups:
        n_rows = len(dataframe)

        if config['verbosity'] >= 2:
            print(f"\nLooking up action '{action_key}' among the action collections...", file=sys.stderr)

        if action_key in dataframe_actions:
            action_func = dataframe_actions[action_key]
            if config['verbosity'] >= 1:
                print(f"\nInvoking '{action_key}' action on {n_rows} rows dataframe with "
                      f"args = {action_args!r}, kwargs = {action_kwargs!r}", file=sys.stderr)
            dataframe = action_func(dataframe, *action_args, **action_kwargs, config=config)
        elif action_key in config_actions:
            action_func = config_actions[action_key]
            if config['verbosity'] >= 1:
                print(f"\nInvoking '{action_key}' config action with args: {action_args!r}", file=sys.stderr)
            action_func(*action_args, **action_kwargs, config=config)
        elif action_key in help_actions:
            action_func = help_actions[action_key]
            action_func(*action_args, **action_kwargs, config=config)
        else:
            raise KeyError(f"action_key '{action_key}' could not be found in any of the action collections.")
