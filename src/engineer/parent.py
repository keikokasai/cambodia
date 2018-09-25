import pandas as  pd
from src.read.parent import read_parent_survey


def column_engineer_parent_survey(dt_original, col):
    if col in ['q1_1', 'q1_2','q1_3']:
        return dt_original.replace({
            'High school': 'high',
            'High School': 'high',
            'BA': 'univ',
            'Secondary school': 'second',
            'Primary school': 'primary',
            'Secondary School': 'second',
            'Primary School': 'primary',
            'MBA': 'master',
            'High School ': 'high',
            'Primary School ': 'primary',
            'primary school': 'primary',
            'Sechondary School': 'second',
            'High school ': 'high',
            'Primary school ': 'primary',
            'PhD': 'phd',
            'PHD': 'phd',
            'Secondary school ': 'second',
            'B.A': 'univ',
            'No Education ': 'nan',
            'Seconday school': 'second',
            'Secondary School ': 'second',
            'Ph.D': 'phd',
            ' N/A': pd.np.nan,
            'Secondaryn school': 'second',
            'Priamry school': 'primary',
            'Primary shcool': 'primary'
        })
    elif col == 'q8':
        return dt_original.replace({'A': 1,'B': 2,'C': 3,'D': 4})
    elif col =='q9':
        return dt_original.replace({'A': pd.np.nan, 'B': pd.np.nan})
    elif col =='q10':
        dt_original_return =  dt_original.replace({'A': pd.np.nan,
                                                   'B': 0,
                                                   'B ': 0,
                                                   'b': 0,
                                                   'C': pd.np.nan,
                                                   ' C': pd.np.nan,
                                                   'V': pd.np.nan})
        return dt_original_return.replace(',','.', regex=True).astype(float)
    elif col =='q11':
        return dt_original.replace({'A': 1,
                                    'B': 2,
                                    'B ': 2,
                                    'b': 2,
                                    'A2': pd.np.nan,
                                    75: pd.np.nan,
                                    'C': pd.np.nan})
    else:
        return dt_original


def engineer_parent_survey(df):
    # setting
    use_cols = ['relationship',
               'q1_1', 'q1_2', 'q1_3', 'q2', 'q3', 'q4', 'q5', 'q6',
               'q7', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16']
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
    path_parent_survey = 'data/original/Final Parent\'s Survey.xlsx'
    df = read_parent_survey(path_parent_survey)
    df_tidy = engineer_parent_survey(df)
