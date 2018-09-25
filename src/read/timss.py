import pandas as pd
from src.lib import get_column_mapper_from_re_mapper


def parse_treatment_from_sheetname_timss_data(sheet_name):
    """
    sheetnameから情報を取得
        exapme:
        parse_treatment_from_sheetname_timss_data('1st - Timss NT')  #  0, 'before'

    :param sheet_name:
    :return:
    """
    # treatmentを判定
    if sheet_name.count('NT') == 0:
        treatment = 1
    elif sheet_name.count('NT') > 0:
        treatment = 0
    else:
        print('Cannot parse: ', sheet_name)
        raise ValueError
    #  before or after
    if sheet_name.count('1st') > 0:
        timing = 'before'
    elif sheet_name.count('2nd') > 0:
        timing = 'after'
    else:
        print('Cannot parse: ', sheet_name)
        raise ValueError
    print('sheet_name is {sheet_name}: Treatment is {treatment}, timing is {timing}'.format(
        sheet_name=sheet_name, treatment=treatment, timing=timing))
    return treatment, timing


def read_data_timss(path_excel):
    """
    example:

        path_excel = "./data/original/TIMSS result.xlsx"
        df_res = read_data_timss(path_excel=path_excel)

    :param path_excel:
    :return:
    """
    # setting
    col_for_data = 'Student ID'
    qes_mapper_re = {
        'School': 'school',
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
        '^Q1': 'q1',
        '^Q2': 'q2',
        '^Q3': 'q3',
        '^Q4': 'q4',
        '^Q5': 'q5',
        '^Q6': 'q6',
        'Correct\nanswer Q?1': 'a1',
        'Correct\nanswer Q?2': 'a2',
        'Correct\nanswer Q?3': 'a3',
        'Correct\nanswer Q?4': 'a4',
        'Correct\nanswer Q?5': 'a5',
        'Correct\nanswer Q?6': 'a6',
        'score 1': 's1',
        'score 2': 's2',
        'score 3': 's3',
        'score 4': 's4',
        'score 5': 's5',
        'score 6': 's6',
        'Total': 'total',
        'correct answer rate': 'correct_answer_rate'
    }
    # start
    # excelブックのそれぞれのシートにデータが入っている
    info_sheets_dict = pd.read_excel(path_excel, sheet_name=None, encoding='sjis')
    sheet_names = list(info_sheets_dict.keys())
    # collect data
    df_res = pd.DataFrame()
    for sheet_name in sheet_names:
        print('Parse:::::::',sheet_name)
        df = info_sheets_dict[sheet_name]
        qes_mapper = get_column_mapper_from_re_mapper(qes_mapper_re, df)
        # 'Student ID'があるレコードだけ使う
        df_use = df.loc[df[col_for_data].notnull(), :]\
            .rename(columns=qes_mapper)\
            .copy()
        treatment, timing = parse_treatment_from_sheetname_timss_data(sheet_name)  # sheet_nameから情報を取得
        df_use['D'] = treatment
        df_use['timing'] = timing
        df_use['test_type'] = 'TIMSS' 
        df_res = df_res.append(df_use)
    return df_res
