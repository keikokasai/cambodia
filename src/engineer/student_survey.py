import pandas as  pd
from src.read.student_survey import read_student_survey


def column_engineer_parent_survey(dt_original, col):
        return dt_original


def engineer_student_survey(df):
    # setting
    use_cols = ['q1',
                'q2',
                'q3',
                'q4',
                'q5',
                'q6',
                'q7',
                'q8',
                'q9',
                'q10',
                'q11',
                'q12',
                'q13',
                'q14',
                'q15',
                'q16',
                'q17',
                'q18',
                'q19',
                'q20',
                'q21',
                'q22',
                'q23',
                'q24',
                'q25',
                'q26',
                'q27',
                'q28',
                'q29',
                'q30']
    id_col = ['student_id']
    # engineer
    df_tidy = pd.DataFrame()
    for col in use_cols:
        df_melt = df[id_col + [col]].melt(
            id_vars=id_col,
            value_vars=col,
            var_name='qes',
            value_name='value_original')
        df_melt['value'] = column_engineer_parent_survey(df_melt['value_original'], col)
        df_tidy = df_tidy.append(df_melt)
    return df_tidy


def example():
    path_excel1 = 'data/original/1st-Assessment Student Questionnairies .xlsx'
    path_excel2 = 'data/original/2nd-Assessment-Student Questionnairies.xlsx'
    df = read_student_survey(path_excel1, path_excel2)
    df_tidy = engineer_student_survey(df)