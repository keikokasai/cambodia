def tidy_to_wide(df, keys: list, qes_col: str, value_col: str, fetch_cols: list):
    """
        import pandas as pd
        keys = ['student_id']
        qes_col = 'qes'  # str
        value_col = 'value'  # str
        fetch_cols = ['relationship', 'q16']
        path = 'data/work/parent.csv'
        data = pd.read_csv(path)
        tidy_to_wide(data,
                     keys=keys,
                     qes_col=qes_col,
                     value_col=value_col,
                     fetch_cols=fetch_cols)
    :param df:
    :param keys:
    :param qes_col:
    :param value_col:
    :param fetch_cols:
    :return:
    """
    tidy_key = keys + [qes_col]
    use_col = tidy_key + [value_col]
    return df.loc[df[qes_col].isin(fetch_cols), use_col]\
            .set_index(tidy_key)\
            .unstack(level=-1)\
            .reset_index()
