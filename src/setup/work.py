import pandas as pd


def info(drop_duplicated_id = True):
    # setting
    path_excel_na = "./data/original/national assessment .xlsx"
    path_excel_timss = "./data/original/TIMSS result.xlsx"
    path_save = './data/work/info.csv'

    from src.read.national_assesment import read_national_assesment
    from src.engineer.info import engineer_info
    df = read_national_assesment(path_excel_na)
    df_info1 = engineer_info(df)
    from src.read.timss import read_data_timss
    df2 = read_data_timss(path_excel_timss)
    df_info2 = engineer_info(df2)
    # save
    df = pd.concat([df_info1, df_info2], axis=0)
    if drop_duplicated_id is True:
        #  # 二重登録のデータを削除する
        df['count'] = df.apply('count', axis=1)
        df_unique = df.sort_values('count', ascending=False).groupby(['student_id']).head(1)
        df_unique.to_csv(path_save, encoding='sjis', index=False)
    else:
        return df
    # memo
    print('yearとかMonthの認識はbirthを元にすべき。もともとageから作っていたが。。。')


def score():
    # setting
    path_excel_na = "./data/original/national assessment .xlsx"
    path_excel_timss = "./data/original/TIMSS result.xlsx"
    path_save = './data/work/score.csv'
    # start
    from src.read.national_assesment import read_national_assesment
    from src.engineer.national_assesment import engineer_national_assesment_score
    df = read_national_assesment(path_excel_na)
    df_tidy1 = engineer_national_assesment_score(df)
    from src.read.timss import read_data_timss
    from src.engineer.timss import engineer_timss
    df = read_data_timss(path_excel_timss)
    df_tidy2 = engineer_timss(df)
    # save
    df = pd.concat([df_tidy1, df_tidy2], axis=0)
    df.to_csv(path_save, encoding='sjis', index=False)


def parent():
    # setting
    path_excel = 'data/original/Final Parent\'s Survey.xlsx'
    path_save = './data/work/parent.csv'
    # start
    from src.read.parent import read_parent_survey
    from src.engineer.parent import engineer_parent_survey
    df = read_parent_survey(path_excel)
    df_tidy = engineer_parent_survey(df)
    # save
    df = df_tidy
    df.to_csv(path_save, encoding='sjis', index=False)


def student_survey():
    path_excel1 = 'data/original/1st-Assessment Student Questionnairies .xlsx'
    path_excel2 = 'data/original/2nd-Assessment-Student Questionnairies.xlsx'
    path_save = './data/work/student_survey.csv'
    from src.read.student_survey import read_student_survey
    from src.engineer.student_survey import engineer_student_survey
    df = read_student_survey(path_excel1, path_excel2)
    df_tidy = engineer_student_survey(df)
    df_tidy.to_csv(path_save, encoding='sjis', index=False)


def main():
    info()
    score()
    parent()
    student_survey()
