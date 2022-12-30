def dataframe_to_dict(df):
    """
        Convert to Dataframe to dictionary and 
        alter columns names with;
        - Underscores (_) to spaces 
        - All Strings are converted to Title Case. 
    """
    list_of_dicts = df.to_dict('records')
    return [{k.replace("_", " ").title(): v for k, v in dict.items()} for dict in list_of_dicts]

def dict_to_markdown_table(list_of_dicts: list, columns_to_include: list = None):
    """
        Description: Generate a Markdown table based on a list of dictionaries.
        Args:
            list_of_dicts       -> List of Dictionaries that need to be converted
                                   to a markdown table.
            columns_to_include  -> Default = None, and all colums are included. 
                                   If a list is supplied, those columns will be included.
        Example:
            columns = ['Referenced Object Type', 'Referenced Table', 'Referenced Object']
            dict_to_markdown_table(dependancies, columns)

        Result: 
            | Referenced Object Type | Referenced Table | Referenced Object               |
            | ---------------------- | ---------------- | ------------------------------- |
            | TABLE                  | Cases            | Cases                           |
            | COLUMN                 | Cases            | IsClosed                        |
            | CALC_COLUMN            | Cases            | Resolution Time (Working Hours) |

    """
    keys = set().union(*[set(d.keys()) for d in list_of_dicts])

    if columns_to_include is not None:
        keys = list(keys.intersection(columns_to_include))      

    table_header = f"| {' | '.join(map(str, keys))} |"
    table_header_separator = '|-----' * len(keys) + '|'
    markdown_table = [table_header, table_header_separator]

    for row in list_of_dicts:
        table_row = f"| {' | '.join(str(row.get(key, '')) for key in keys)} |"
        markdown_table.append(table_row)
    return '\n'.join(markdown_table)