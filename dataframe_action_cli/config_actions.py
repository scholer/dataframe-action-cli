# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

Config actions are actions that changes the runtime configuration object.

"""


def increment_verbosity(config, *args, **kwargs):
    """ Increase program informational output verbosity. """
    # If you modify (reassign) an immutable type within a closure, it is by default considered a local variable.
    # To prevent this, declare that the variable is non-local:
    config['verbosity'] = config.get('verbosity', 0) + 1


ACTIONS = {
    'verbose': increment_verbosity,
    'v': increment_verbosity,
}


