import pandas as pd
from src.lib import get_column_mapper_from_re_mapper

def specific_readr(path_excel, first=True):
    """
    assessmentはシートごとに構造が違うから特注で作んなきゃ。。。
    """
    # setting
    if first is True:
        all_sheets_data = pd.read_excel(path_excel, header=1, sheet_name=None, encoding='sjis')
    elif first is False:
        all_sheets_data = pd.read_excel(path_excel, header=2, sheet_name=None, encoding='sjis')
    else:
        raise ValueError
    all_sheet_names = list(all_sheets_data.keys())
    no_data_sheets = ['Done Class', 'Sample', 'Done Entered Class', 'Samples']
    use_sheet_names = all_sheet_names.copy()
    for no_data_sheet in no_data_sheets:
        if no_data_sheet in all_sheet_names:
            use_sheet_names.remove(no_data_sheet)
    # start
    info_sheets_dict = {}
    for sheet in use_sheet_names:
        data = all_sheets_data[sheet]
        info_sheets_dict.update({sheet: data})
    return info_sheets_dict, use_sheet_names


def read_student_survey(path_excel1, path_excel2):
    """
    Example
        path_excel1 = 'data/original/1st-Assessment Student Questionnairies .xlsx'
        path_excel2 = 'data/original/2nd-Assessment-Student Questionnairies.xlsx'
        df = read_student_survey(path_excel1, path_excel2)
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
        '^Q1$': 'q1',
        '^Q2$': 'q2',
        '^Q3$': 'q3',
        '^Q4$': 'q4',
        '^Q5$': 'q5',
        '^Q6$': 'q6',
        '^Q7$': 'q7',
        '^Q8$': 'q8',
        '^Q9$': 'q9',
        '^Q10$': 'q10',
        '^Q11$': 'q11',
        '^Q12$': 'q12',
        '^Q13$': 'q13',
        '^Q14$': 'q14',
        '^Q15$': 'q15',
        '^Q16$': 'q16',
        '^Q17$': 'q17',
        '^Q18$': 'q18',
        '^Q19$': 'q19',
        '^Q20$': 'q20',
        '^Q21$': 'q21',
        '^Q22$': 'q22',
        '^Q23$': 'q23',
        '^Q24$': 'q24',
        '^Q25$': 'q25',
        '^Q26$': 'q26',
        '^Q27$': 'q27',
        '^Q28$': 'q28',
        '^Q29$': 'q29',
        '^Q30$': 'q30'
    }
    col_for_data = 'Student ID'
    # # excelブックのそれぞれのシートにデータが入っている
    info_sheets_dict1, sheet_names1 = specific_readr(path_excel1, first=True)
    info_sheets_dict2, sheet_names2 = specific_readr(path_excel2, first=False)
    # collect dat
    df_res = pd.DataFrame()
    setting = zip(
        ['before', 'after'],
        [sheet_names1, sheet_names2],
        [info_sheets_dict1, info_sheets_dict2]
    )
    for timing, sheet_names, info_sheets_dict in setting:
        for sheet_name in sheet_names:
            df = info_sheets_dict[sheet_name]
            qes_mapper = get_column_mapper_from_re_mapper(qes_mapper_re,
                                                          df)
            # 'Student ID'があるレコードだけ使う
            df_use = df.loc[df[col_for_data].notnull(), :]\
                .rename(columns=qes_mapper)\
                .copy()
            # engineer
            df_use['timing'] = timing
            # append
            df_res = df_res.append(df_use)
    return df_res