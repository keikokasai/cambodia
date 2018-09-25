import pandas as pd


def get_column_mapper_from_re_mapper(col_mapper_re, df,
                                     ignorecase=True,
                                     verbose_cannot_map=False,
                                     verbose_can_df_col=True):
    """
    正規表現でcolumns mapperを作成する。

    ex:
    df = pd.DataFrame(['12'], columns=['Q11'])
    col_mapper_re = {
        'Q\d{2}': 'Q99'
    }
    get_column_mapper_from_re_mapper(col_mapper_re, df)  # {'Q11': 'Q99'}

    """
    import re
    col_mapper_proposed = {}
    cannot_map_key_list = []
    can_df_col_list = []
    for key in list(col_mapper_re.keys()):
        count_key = 0
        for col in df.columns:
            match_key = key
            if ignorecase is True:
                match_key = '(?i)' + match_key
            if re.search(match_key, col) is not None:
                # keyには正規表現が入りうる。escape文字列などあるから、 raw stringにする(repr関数)
                col_mapper_proposed.update({col: col_mapper_re[key]})
                count_key += 1
                can_df_col_list.append(col)
        if count_key == 0:
            cannot_map_key_list.append(key)
            # raise LookupError
        if count_key > 1:
            print('2つ以上のカラムにマッチしています. : {key}'.format(key=key))
            raise LookupError
    if verbose_cannot_map is True:
        print('col_mapper_reの中にmapできないkeyがあります. : {key_list}'.format(
            key_list=' ,'.join(cannot_map_key_list)))
    if verbose_can_df_col is True:
        can_not_df_col_list = []
        for col in df.columns:
            if col not in can_df_col_list:
                can_not_df_col_list.append(col)
        if len(can_not_df_col_list) > 0:
            print('data columnsの中にmap対象がなかったカラムがありまず. : {col_list}'.format(
                col_list=' ,'.join(can_not_df_col_list)))
    return col_mapper_proposed


def tidy_to_wide(df, keys: list, qes_col: str, value_col: str, fetch_cols: list):
    """
    Documentを見る限り、マルチインデックスのシリーズにして
    unstacksするのが良い？
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html

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
    df_long = df.loc[df[qes_col].isin(fetch_cols), use_col].set_index(tidy_key)
    series_long = pd.Series(df_long[value_col], index=df_long.index)
    df_wide = series_long\
        .unstack(level=-1)\
        .reset_index()
    # to trash
    # df_wide = df.loc[df[qes_col].isin(fetch_cols), use_col]\
    #         .set_index(tidy_key)\
    #         .unstack(level=-1)\
    #         .reset_index()
    # df_wide.columns = df_wide.columns.droplevel(0)
    return df_wide
