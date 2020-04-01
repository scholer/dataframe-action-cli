# dataframe-action-cli

Dataframe-action-cli is a pragmatic command-line interface program/application
to edit and manipulate tabular data from e.g. CSV files.

Dataframe-action-cli is designed to be suitable for use in scripts, 
e.g. as part of a reproducible scientific pipeline.
For this reason, dataframe-action-cli is not intended to function as an interactive 
data viewer or editor; there are plenty of alternatives for this (see below).


## Examples:

Examples, quick overview:

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

    # Print table:
    dataframe-action-cli (...) -print-csv
    
    # Write to file:
    dataframe-action-cli (...) -write-to file.csv




### Loading data:

To load data from files you use the `-read-from` action:

    dataframe-action-cli -read-from <inputfile>

For example, to load data from `input.csv`, use:

    dataframe-action-cli -read-from input.csv

You can read and concatenate data from multiple files by simply using `-read` multiple times:

    dataframe-action-cli -read-from input1.csv -read-from input2.csv


### Selecting rows using `select-where`:

The primary way to select rows is using the `-select-where` action:

For instance, to select rows where the "name" column is either "Peter" or "Michael", use:

    dataframe-action-cli -read-from input.csv -select-where name matches "(Peter|Michael)"

The above example uses the "matches" operator, which uses a regular expression to compare the row 
values against.

The generalized form of the `-select-where` action is:

    dataframe-action-cli -read-from input.csv -select-where <columnX> <operator> <value>

Where <column> is the column you want to select based on, `<operator` is the operator you wish to use,
and `<value>` is the value you wish to use as selection criteria. 
For instance, other operators include `glob`, `in`, etc.:

    dataframe-action-cli -read-from input.csv -select-where <columnX> matches <regex-pattern>
    dataframe-action-cli -read-from input.csv -select-where <columnX> glob <glob-pattern>
    dataframe-action-cli -read-from input.csv -select-where <columnX> in <list-of-values>


### Selecting rows using `select-query`:

The `-select-query` is a little more advanced than `-select-where`.
In this case, you provide a single "query", which is parsed for each row using
Python's `eval` function.

    dataframe-action-cli -read-from input.csv -select-query <query>
    dataframe-action-cli -read-from input.csv -select-query "name in ('Peter', 'Michael')"


### Sorting rows using `-sort-by`:

Use the `-sort-by` action to sort your table:

    dataframe-action-cli -read-from input.csv -sort-by <column>



### Creating new columns:

You can use the `-create-column` action to create a new column.
This is pretty simple, just use:

    dataframe-action-cli -read-from input.csv -create-column <columnname> <expression>
    dataframe-action-cli -read-from input.csv -create-column total "amount * price_each"

You can also create a new column using a single assignment expression:

    dataframe-action-cli -read-from input.csv -create-column <expression>
    dataframe-action-cli -read-from input.csv -create-column "total = amount * price_each"

The two forms are equivalent, just different ways of typing the same thing.


### Writing table to file or stdout:

After selecting rows, creating columns, the final step is generally to output your table,
either to a file or print to standard out.
This is easily done with the `-write-to <file>` and `-print` actions:
    
Write table to file:

    dataframe-action-cli (...) -write-to file.csv

Print table to stdout:

    dataframe-action-cli (...) -print-csv


### Complete example:

Here is a complete example that will load data from `input.csv`,
select rows where name is either "Peter" or "Michael",
create a new column, "total", equalling amount times the price for each product,
then sort by the new "total" column,
and finally write the output to `output.csv`.


    dataframe-aciton-cli \
        -read-from input.csv
        -select-where name matches "(Peter|Michael)"
        -create-column "total = amount * price_each"
        -sort-by total
        -write-to output.csv



## Prior art

Similar/alternative applications:


* **`sort`** GNU command line program - is great for sorting and merging tabular data,
  but doesn't provide the all the other features that I required.
  
* **`awk`** is another GNU CLI for working with text-based files, using a program-like syntax.
  Awk is very powerful, but really hard to learn and use for the regular user,
  and is basically its own language.

* **Miller**: 
    *"Miller is like awk, sed, cut, join, and sort for name-indexed data such as CSV, TSV, and tabular JSON."*
    Written in C. 
    http://johnkerl.org/miller/doc
    Miller is the closest application I've found that suited my need.
    Miller is great for working with tabular data in a scripting environment, 
    and it has a very large feature-set, which is basically an entire domain-specific language.
    Miller is also a little hard to learn, because of the large feature-set.
    The Miller documentation includes a list of other tools and inspirational prior art: 
    http://johnkerl.org/miller/doc/originality.html.
    
    * For my purpose, Miller seems a bit overkill. 
      I also prefer a CLI syntax that is a little easier read and understand.
      Finally, I like to use Python apps, because then I know that I can always 
      refer to the source code to understand what is going on and add new features
      as required. (I'm not a very good C programmer.)

* **jq** is a CLI app for working with JSON data (rather than tabular data).

* **VisiData** is a versatile and comprehensive text user interface (TUI),
  for working interactively with datasets.

  * VisiData did not fit my needs, since it is geared towards viewing and manipulating
      data *interactively* - rather than via a command line arguments.
      VisiData *does* provide a feature to "record and play back" a session, 
      saving the session to a file, which can later be used in "batch mode".
      However, the documentation does not do much to describe how to create 
      new vd-session files from scratch (the cmdlog documentation page is currently empty). 

* **TabView** is another TUI application, but mostly for viewing data, rather than 
  manipulating it as part of a script/pipeline. (Also, not to be confused with the popular
  tabview.js javascript library!)


See also:

* https://github.com/dbohdan/structured-text-tools - a list of tools for working with structured text.




TODO:
-----

* TODO: Consider alternative row-selection action which uses 
  https://github.com/yhat/pandasql for selecting rows.

* TODO: Add column selection action, e.g. `limit_columns_to (list of column names)`.
* TODO: Add `-drop-column` action.

* TODO: Compare with other structured-text-tools from
    https://github.com/dbohdan/structured-text-tools#dsv

* TODO: Side-by-side comparison with Miller.
    * http://johnkerl.org/miller/doc/reference.html
    * http://johnkerl.org/miller/doc/originality.html


