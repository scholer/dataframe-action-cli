# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

import sys
import pandas as pd

from actionista import binary_operators
from .input_type_conversion import STR_TO_BOOL, ensure_input_type


def read_file(df: pd.DataFrame, filename, *args, config=None, sep=",", ignore_index=True, join='outer', copy=True, **kwargs) -> pd.DataFrame:
    df2 = pd.read_csv(filename, sep=sep, **kwargs)
    if df is None or len(df) == 0:
        return df2
    else:
        return pd.concat([df, df2], join=join, ignore_index=ignore_index, copy=copy)


def write_csv(df: pd.DataFrame, filename, header=True, index=False, index_label=None, config=None) -> pd.DataFrame:
    df.to_csv(filename)
    return df


def print_csv(df: pd.DataFrame, *args, limit=None, header=True, index=False, index_label=None, config=None, **kwargs) -> pd.DataFrame:
    header = ensure_input_type(header, bool, varname='header', args=args)
    index = ensure_input_type(index, bool, varname='index', args=args)
    limit = int(limit)
    print_df = df
    if limit:
        print_df = df.iloc[:limit]
    print(print_df.to_csv(header=header, index=index, index_label=index_label))
    return df


def select_rows_from(df: pd.DataFrame, from_row, config=None) -> pd.DataFrame:
    return df.loc[from_row:]


def select_rows_to(df: pd.DataFrame, to_row, config=None) -> pd.DataFrame:
    return df.loc[:to_row]


def select_rows_between(df: pd.DataFrame, from_row, to_row, config=None) -> pd.DataFrame:
    return df.loc[from_row:to_row]


def select_rows_islice(df: pd.DataFrame, from_row, to_row, config=None) -> pd.DataFrame:
    return df.iloc[from_row:to_row]


def select_rows_loc_eval(df: pd.DataFrame, *args, config=None) -> pd.DataFrame:
    """ A more advanced, general-purpose row-selection method.

    Examples:

        -select-rows 2:5 8 13 20:25

    """
    return pd.concat([eval("df.loc[{arg}]".format(arg=arg)) for arg in args])


def select_query_action(df: pd.DataFrame, *query, config=None) -> pd.DataFrame:
    # Pandas query() uses Python compile() to evaluate expressions.
    query = " ".join(query)
    return df.query(query)


def select_where(df: pd.DataFrame, column, comparison_method, comparison_value=None, invert=False, config=None) -> pd.DataFrame:
    """ Select rows where a column matches a given value (using some kind of comparison method).

    Args:
        df: DataFrame.
        column: The column to select based on.
        comparison_method: The method to match with, e.g. 'eq', 'matches', 'less-than', etc.
        comparison_value: The value to match/compare against.
        invert: Invert the selection.
        config: App-level config.

    Returns:
        DataFrame

    Examples:

        # Selecting using `select-where`:
        dataframe-action-cli -read-from input.csv -select-where <columnX> matches <regex-pattern>
        dataframe-action-cli -read-from input.csv -select-where name matches "(Peter|Michael)"
        dataframe-action-cli -read-from input.csv -select-where <columnX> glob <glob-pattern>
        dataframe-action-cli -read-from input.csv -select-where <columnX> in <list-of-values>

    """
    invert = ensure_input_type(invert, ensure_type=bool)
    if comparison_method.lower() == 'isna' or (
            comparison_method == 'is' and comparison_value.lower() in ("na", "n/a", "nan")):
        return df.loc[df[column].isna()]
    comparison_func_ = getattr(binary_operators, comparison_method)
    if invert:
        def comparison_func(a, b):
            return not comparison_func_(a, b)
    else:
        comparison_func = comparison_func_
    if comparison_method == 'in':
        if "," in comparison_value:
            comparison_value = {v.strip() for v in comparison_value.split(",")}
        print(f"Comparison: {column} {comparison_func} {comparison_value}")
    # This doesn't cache e.g. regex comparison, maybe optimize for special cases.
    apply_func = lambda row_val: bool(comparison_func(row_val, comparison_value))
    return df.loc[df[column].apply(apply_func)]


def sort_by(df: pd.DataFrame, *args, kind='quicksort', na_position='last', config=None) -> pd.DataFrame:
    """

    Args:
        df: DataFrame.
        *args:
            Use <column>::ascending or <column>::descending to control ascending or descending sort order.
        config:

    Returns:

    Examples:

        >>> sort_by(df, ["Pool-name::desc", "Plate-name", "Pos"])

    """
    sort_by, ascending = zip(*[
        (column.split("::")[0], False) if '::des' in column else (column, True)
        for column in args
    ])
    # OBS: When giving multiple columns to sort on, it should be a list, not a tuple.
    return df.sort_values(by=list(sort_by), ascending=list(ascending), kind=kind, na_position=na_position)


def natsort_by(df: pd.DataFrame, column, reverse=False, config=None) -> pd.DataFrame:
    """ Sort strings naturally, e.g. sort "A2" before "A10" """
    try:
        import natsort
    except ImportError:
        print("\n\nERROR!   --> Could not import natsort! <--  "
              "DataFrame will not be sorted. Please install the 'natsort' package.",
              file=sys.stderr)
        return df
    sorted_idxs = natsort.index_natsorted(df[column], reverse=reverse)
    return df.iloc[sorted_idxs]


def create_column_dfeval(df: pd.DataFrame, *args, config=None) -> pd.DataFrame:
    """ Create a new column using DataFrame.eval(expr, engine='python'). """

    # OBS: Slicing is not a supported operation, meaning you cannot do much string manipulation.
    #
    if args[1] == "=":
        # Forgot quote marks, e.g. `-create-column total = colA + colB`
        args = [" ".join(args)]
    if len(args) == 1:
        # Style: "col3 = col1 + col2"
        expr, = args[0]
        print("create-column expr:", expr)
        return df.eval(expr, engine='python')
    elif len(args) == 2:
        # Style: "col3", "col1 + col2"
        col, expr = args
        print(f"create-column {col} expr:", expr)
        df[col] = df.eval(expr, engine='python')
        return df
    else:
        raise RuntimeError("`create-column` arguments could not be recognized:", args)


def create_column_pyeval(df: pd.DataFrame, columnname, expr, *args, use_format=False, config=None) -> pd.DataFrame:
    """ Create a new column, using a `eval(expr)` inside a list comprehension (slow).

    Args:
        df: DataFrame.
        columnname: Name of the new column to create.
        expr: Expression used to create the new column.
        *args: Additional arguments, e.g. ['no-use-format'].
        use_format: Whether to apply string format, e.g. use `eval(expr.format(**row))`.
        config: app-wide config object.

    Returns:
        DataFrame

    Examples:

        >>> create_column_pyeval(df, columnname="WellRow", expr="row + column")

        # Use string format:
        >>> create_column_pyeval(df, columnname="WellRow", expr="{row}{column:02}")

        # Can use slicing, and builtin operations:
        >>> create_column_pyeval(df, columnname="WellRow", expr="str(int(Pos[1:])) + ' ' + Pos[0]")

    Examples, called from the Action CLI:
        > -create-column WellRow "row + column"
        > -create-column WellRow "str(int(Pos[1:])) + ' ' + Pos[0]"
    """
    use_format = ensure_input_type(
        use_format, bool, varname='use-format', args=args)
    if use_format:
        df[columnname] = [eval(expr.format(**dict(row)), None, dict(row)) for rowidx, row in df.iterrows()]
    else:
        df[columnname] = [eval(expr, None, dict(row)) for rowidx, row in df.iterrows()]
    return df


ACTIONS = {

    # data input/output commands:
    'read-file': read_file,
    'read-from': read_file,
    'read-csv': read_file,
    'write-file': write_csv,
    'write-to': write_csv,
    'write-csv': write_csv,
    'print-csv': print_csv,

    # Row-selection commands:
    'select-rows-from': select_rows_from,
    'select-rows-to': select_rows_to,
    'select-rows-between': select_rows_between,
    'select-rows-islice': select_rows_islice,
    'select-query': select_query_action,
    'select-where': select_where,

    # Row sorting:
    'sort-by': sort_by,
    'natsort-by': natsort_by,
    'natsort': natsort_by,
    'sort-natural': natsort_by,

    # Column creation:
    'create-column-fast': create_column_dfeval,
    'create-column': create_column_pyeval,
}
