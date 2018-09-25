import pandas as  pd
from src.read.national_assesment import read_national_assesment


def engineer_national_assesment_score(df):
    """
    ex:
        path_excel = "./data/original/national assessment .xlsx"
        df = read_national_assesment(path_excel)
        df_tidy = engineer_timss_score_survey(df)

    """
    # setting
    use_cols = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10',
                's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20',
                's21', 's22', 's23', 's24', 's25', 's26', 's27', 's28', 's29', 's30',
                's31', 's32', 's33', 's34', 's35',
                'total', 'correct_answer_rate']
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
    path_excel = "./data/original/national assessment .xlsx"
    df = read_national_assesment(path_excel)
    df_tidy = engineer_national_assesment_score(df)