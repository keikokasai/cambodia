import pandas as pd
from src.lib import get_column_mapper_from_re_mapper


def read_parent_survey(path):
    """
    Example
        path_parent_survey = 'data/original/Final Parent\'s Survey.xlsx'
        df = read_parent_survey(path_parent_survey)
    :param path:
    :return:
    """
    # setting
    qes_mapper_re = {
        # always exists
        '^No$': 'no',
        'Grade': 'grade',
        'Class': 'class',
        'Student ID': 'student_id',
        'Name in Khmer': 'name_khmer',
        'Name in English': 'name_eng',
        'Name in Tablet': 'name_tablet',
        'Tablet Number': 'tablet',
        'Sex': 'sex',
        'Date of Birth': 'date_of_birth',
        'Age': 'age',
        # parent survey specific
        'Kid\'s Name': 'kid_name',
        'Father\'s Name': 'father_name',
        'Mother\'s Name': 'mother_name',
        'Guardian\'s Name': 'guradridan_name',
        'Contact': 'contact',
        'Relationship with Kid': 'relationship',
        'Q1.1.': 'q1_1',
        'Q1.2.': 'q1_2',
        'Q1.3.': 'q1_3',
        'Q2.': 'q2',
        'Q3.': 'q3',
        'Q4.': 'q4',
        'Q5.': 'q5',
        'Q6.': 'q6',
        'Q7.': 'q7',
        'Q8.': 'q8',
        'Q9.': 'q9',
        'Q10.': 'q10',
        'Q11.': 'q11',
        'Q12.': 'q12',
        'Q13.': 'q13',
        'Q14.': 'q14',
        'Q15.': 'q15',
        'Q16.': 'q16',
        'NOTE': 'note',
        'SFSDF': 'SFSDF',
        'No answer': 'no_answer',
        'Uncomplete': 'uncomplete',
        'Valid': 'valid'
    }
    col_for_data = 'Student ID'
    #  excelブックのそれぞれのシートにデータが入っている
    info_sheets_dict = pd.read_excel(path, sheet_name=None, encoding='sjis')
    sheet_names = list(info_sheets_dict.keys())
    # collect data
    df_res = pd.DataFrame()
    for sheet_name in sheet_names:
        df = info_sheets_dict[sheet_name]
        qes_mapper = get_column_mapper_from_re_mapper(qes_mapper_re, df)
        # 'Student ID'があるレコードだけ使う
        df_use = df.loc[df[col_for_data].notnull(), :]\
            .rename(columns=qes_mapper)\
            .copy()
        # engineer
        # append
        df_res = df_res.append(df_use)
    return df_res