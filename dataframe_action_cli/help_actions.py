# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

from actionista import binary_operators


NEWLINE = '\n'


def print_help(tasks, cmd=None, *, verbose=0):
    """ Print help messages. Use `-help <action>` to get help on a particular action. """
    # import re
    # print(repr(action_cli.__doc__))  # Nope, escapes proper line breaks.
    # print(re.escape(action_cli.__doc__))  # Nope, escapes whitespace.
    if cmd is None:
        print(action_cli.__doc__)  # Works, if you are using r""" for your docstrings (which you probably should).
        print("    Complete list of available actions:")
        print("    -------------------------------------\n")
        print("\n".join(
            f"      -{action:20} {(func.__doc__ or '').split(NEWLINE, 1)[0]}"
            for action, func in list(ACTIONS.items())))
        print("\n")
    elif cmd == "operators":
        print("""
Binary comparison operators are used to compare two values:

    valueA  operator  valueB

For example: "1 eq 2" returns False ("no match"), while "2 eq 2" returns True ("match").

Tasks where the two operands compare to true are included/kept in the list, while non-matching items are discarted.
""")
        print("\nAvailable operators include:")
        print(", ".join(sorted(op for op in dir(binary_operators) if not op.startswith('_'))))
        print("""
Some operators expect strings (e.g. "abcdefg startswith abc"), 
while others are mostly type-agnostic, e.g. "123 greaterthan 100".

For `todoist-action-cli`, most arguments are assumed to be strings, and you have to use the 'value_transform' 
argument to convert input values to e.g. integers. 

""")
        print(binary_operators.__doc__)
    else:
        if cmd not in ACTIONS:
            print(f"\nERROR: {cmd!r} command not recognized.\n")
            return print_help(tasks)
        else:
            print(ACTIONS[cmd].__doc__)


ACTIONS = {
    'help': print_help,
    'h': print_help,
}
