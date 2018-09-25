import pandas as pd
from src.lib import get_column_mapper_from_re_mapper
from functools import reduce
from operator import or_


def parse_treatment_from_sheetname_national_assesment_data(sheet_name):
    """
    sheetnameから情報を取得
        exapme:
        parse_treatment_from_sheetname_timss_data('1st - Timss NT')  #  0, 'before'

    :param sheet_name:
    :return:
    """
    # treatmentを判定
    is_treatment = \
        reduce(or_,
               [sheet_name.count('- T') > 0])
    is_nontreatment = \
        reduce(or_,
               [sheet_name.count('- N') > 0,
                sheet_name.count('-NT') > 0])
    if is_treatment is True:
        treatment = 1
    elif is_nontreatment is True:
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


def specific_readr(path_excel):
    """
    assessmentはシートごとに構造が違うから特注で作んなきゃ。。。
    """
    # setting
    all_sheet_names = [
        'By Assessment\'s type - Summary ',
        '1st - National Exam grade 3 - T',
        '1st - National Exam grade 3 - N',
        '2nd - National Exam grade 3 - T',
        '2nd - National Exam grade 3 -NT'
    ]
    no_data_sheets = ['By Assessment\'s type - Summary ']
    sheet_names = all_sheet_names.copy()
    for no_data_sheet in no_data_sheets:
        sheet_names.remove(no_data_sheet)
    # start
    all_sheets_data = pd.read_excel(path_excel, sheet_name=None, encoding='sjis', header=0)
    for sheet in list(all_sheets_data.keys()):
        if sheet not in all_sheet_names:
            print(repr(sheet))
            raise KeyError
    info_sheets_dict = {}
    for sheet in sheet_names:
        if sheet in [
            '1st - National Exam grade 3 - T',
            '1st - National Exam grade 3 - N']:
            data = pd.read_excel(path_excel, header=1, sheet_name=sheet, encoding='sjis')
            info_sheets_dict.update({sheet: data})
        elif sheet in [
            '2nd - National Exam grade 3 - T',
            '2nd - National Exam grade 3 -NT']:
            data = pd.read_excel(path_excel, header=2, sheet_name=sheet, encoding='sjis')
            info_sheets_dict.update({sheet: data})
    return info_sheets_dict, sheet_names


def read_national_assesment(path_excel):
    """
    example:

        path_excel = "./data/original/national assessment .xlsx"
        df_res = read_national_assesment(path_excel=path_excel)

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
        '^P1$': 'p1',
        '^P2$': 'p2',
        '^P3$': 'p3',
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
        '^Q30$': 'q30',
        '^Q31$': 'q31',
        '^Q32$': 'q32',
        '^Q33$': 'q33',
        '^Q34$': 'q34',
        '^Q35$': 'q35',
        '^Practice answer1$': 'pa1',
        '^Practice answer2$': 'pa2',
        '^Practice answer3$': 'pa3',
        '^Correct\n\s*answer 1$': 'ca1',
        '^Correct\n\s*answer 2$': 'ca2',
        '^Correct\n\s*answer 3$': 'ca3',
        '^Correct\n\s*answer 4$': 'ca4',
        '^Correct\n\s*answer 5$': 'ca5',
        '^Correct\n\s*answer 6$': 'ca6',
        '^Correct\n\s*answer 7$': 'ca7',
        '^Correct\n\s*answer 8$': 'ca8',
        '^Correct\n\s*answer 9$': 'ca9',
        '^Correct\n\s*answer 10$': 'ca10',
        '^Correct\n\s*answer 11$': 'ca11',
        '^Correct\n\s*answer 12$': 'ca12',
        '^Correct\n\s*answer 13$': 'ca13',
        '^Correct\n\s*answer 14$': 'ca14',
        '^Correct\n\s*answer 15$': 'ca15',
        '^Correct\n\s*answer 16$': 'ca16',
        '^Correct\n\s*answer 17$': 'ca17',
        '^Correct\n\s*answer 18$': 'ca18',
        '^Correct\n\s*answer 19$': 'ca19',
        '^Correct\n\s*answer 20$': 'ca20',
        '^Correct\n\s*answer 21$': 'ca21',
        '^Correct\n\s*answer 22$': 'ca22',
        '^Correct\n\s*answer 23$': 'ca23',
        '^Correct\n\s*answer 24$': 'ca24',
        '^Correct\n\s*answer 25$': 'ca25',
        '^Correct\n\s*answer 26$': 'ca26',
        '^Correct\n\s*answer 27$': 'ca27',
        '^Correct\n\s*answer 28$': 'ca28',
        '^Correct\n\s*answer 29$': 'ca29',
        '^Correct\n\s*answer 30$': 'ca30',
        '^Correct\n\s*answer 31$': 'ca31',
        '^Correct\n\s*answer 32$': 'ca32',
        '^Correct\n\s*answer 33$': 'ca33',
        '^Correct\n\s*answer 34$': 'ca34',
        '^Correct\n\s*answer 35$': 'ca35',
        '^Practice score 1$': 'ps1',
        '^Practice score 2$': 'ps2',
        '^Practice score 3$': 'ps3',
        '^Score 1$': 's1',
        '^Score 2$': 's2',
        '^Score 3$': 's3',
        '^Score 4$': 's4',
        '^Score 5$': 's5',
        '^Score 6$': 's6',
        '^Score 7$': 's7',
        '^Score 8$': 's8',
        '^Score 9$': 's9',
        '^Score 10$': 's10',
        '^Score 11$': 's11',
        '^Score 12$': 's12',
        '^Score 13$': 's13',
        '^Score 14$': 's14',
        '^Score 15$': 's15',
        '^Score 16$': 's16',
        '^Score 17$': 's17',
        '^Score 18$': 's18',
        '^Score 19$': 's19',
        '^Score 20$': 's20',
        '^Score 21$': 's21',
        '^Score 22$': 's22',
        '^Score 23$': 's23',
        '^Score 24$': 's24',
        '^Score 25$': 's25',
        '^Score 26$': 's26',
        '^Score 27$': 's27',
        '^Score 28$': 's28',
        '^Score 29$': 's29',
        '^Score 30$': 's30',
        '^Score 31$': 's31',
        '^Score 32$': 's32',
        '^Score 33$': 's33',
        '^Score 34$': 's34',
        '^Score 35$': 's35',
        'Overall Total': 'overall_toal',
        '^Total': 'total',
        'Correct answer rate': 'correct_answer_rate'
    }
    # start
    # excelブックのそれぞれのシートにデータが入っている
    info_sheets_dict, sheet_names = specific_readr(path_excel=path_excel)
    # collect data
    df_res = pd.DataFrame()
    for sheet_name in sheet_names:
        print('Parse:::::::', sheet_name)
        df = info_sheets_dict[sheet_name]
        qes_mapper = get_column_mapper_from_re_mapper(qes_mapper_re, df)
        # 'Student ID'があるレコードだけ使う
        df_use = df.loc[df[col_for_data].notnull(), :]\
            .rename(columns=qes_mapper)\
            .copy()
        treatment, timing = parse_treatment_from_sheetname_national_assesment_data(sheet_name)  # sheet_nameから情報を取得
        df_use['D'] = treatment
        df_use['timing'] = timing
        df_use['test_type'] = 'NationalAssesment'
        df_res = df_res.append(df_use)
    return df_res


def memo_df_columns_mapper(df):
    """
    mapperを作るときに今回多すぎるので、お手手でやるのはいやだ

    :return:
    """
    import re
    print_list = []
    for col in df.columns:
        count = 0
        match = re.search('^P(\d+)', col)
        if match is not None:
            key = repr('^' + col + '$')
            value_base = 'p'
            value = repr(value_base + '{n}'.format(n=match.group(1)))
            print_list.append(key + ": " + value)
            count += 1
        match = re.search('^Q(\d+)', col)
        if match is not None:
            key = repr('^' + col + '$')
            value_base = 'q'
            value = repr(value_base + '{n}'.format(n=match.group(1)))
            print_list.append(key + ": " + value)
            count += 1
        match = re.search('^Practice answer(\d+)', col)
        if match is not None:
            key = repr('^' + col + '$')
            value_base = 'pa'
            value = repr(value_base + '{n}'.format(n=match.group(1)))
            print_list.append(key + ": " + value)
            count += 1
        match = re.search('^Correct\n answer (\d+)', col)
        if match is not None:
            key = repr('^' + col + '$')
            value_base = 'ca'
            value = repr(value_base + '{n}'.format(n=match.group(1)))
            print_list.append(key + ": " + value)
            count += 1
        match = re.search('^Practice score (\d+)', col)
        if match is not None:
            key = repr('^' + col + '$')
            value_base = 'ps'
            value = repr(value_base + '{n}'.format(n=match.group(1)))
            print_list.append(key + ": " + value)
            count += 1
        match = re.search('^Score (\d+)', col)
        if match is not None:
            key = repr('^' + col + '$')
            value_base = 's'
            value = repr(value_base + '{n}'.format(n=match.group(1)))
            print_list.append(key + ": " + value)
            count += 1
        if count == 0:
            print_list.append(repr(col))
    print(",\n".join(print_list))
