# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

STR_TO_BOOL = {
    'TRUE': True,
    'T': True,
    '1': True,
    1: True,
    'FALSE': False,
    'F': False,
    '0': False,
    0: False,
}


def ensure_input_type(input_val, ensure_type, varname=None, args=tuple()):
    """ Ensure that input value has a certain type.
    This is mostly useful for boolean types, where simply doing `val = bool(bal)`
    is likely to produce unintended results, e.g. `bool('0')` yields True.
    This also support var-args, where you might want to set a variable as
        -print-csv no-header index
    which should set header=False, index=True.
    Here, `args` will be `['no-header', 'index']`.

    Examples:

        >>> ensure_input_type(input_val='True', ensure_type=bool)
        True

        >>> ensure_input_type(input_val='1', ensure_type=bool)
        True

        >>> ensure_input_type(input_val='F', ensure_type=bool)
        False

        >>> ensure_input_type(input_val=0, ensure_type=bool)
        False

        # 'no-header' in `args` trumps the input value, even if it has correct starting type:
        >>> ensure_input_type(input_val=True, ensure_type=bool, varname='header', args=['no-header', 'index'])
        False

        # 'index' in `args` trumps the input value:
        >>> ensure_input_type(input_val='none', ensure_type=bool, varname='index', args=['no-header', 'index'])
        True

    """

    if ensure_type is bool:
        if varname and args:
            if f'no-{varname}' in args or f'no{varname}' in args:
                input_val = False
            elif 'header' in args:
                input_val = True
        if isinstance(input_val, str):
            input_val = STR_TO_BOOL[input_val.upper()]

    elif ensure_type is int:
        input_val = int(input_val)

    elif ensure_type is float:
        input_val = float(input_val)

    elif ensure_type is str:
        input_val = str(input_val)

    assert isinstance(input_val, ensure_type)

    return input_val
