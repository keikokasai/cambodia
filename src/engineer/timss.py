import pandas as  pd
from src.read.timss import read_data_timss


def engineer_timss(df):
    # setting
    use_cols = ['s1', 's2', 's3', 's4', 's5', 's6', 'total', 'correct_answer_rate']
    id_col = ['student_id', 'test_type', 'D', 'timing']
    # engineer
    df_tidy = pd.DataFrame()
    for col in use_cols:
        df_melt = df[id_col + [col]].melt(
            id_vars=id_col,
            value_vars=col,
            var_name='qes',
            value_name='value_original')
        df_melt['value'] = df_melt['value_original']
        df_tidy = df_tidy.append(df_melt)
    return df_tidy

def example():
    path_excel = "./data/original/TIMSS result.xlsx"
    df = read_data_timss(path_excel)
    df_tidy = engineer_timss(df)