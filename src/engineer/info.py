import pandas as pd


def engineer_info(df):
    """
    timss と national assessmentからinfoデータを作る
    :param df:
    :return:
    """
    # definition
    age_col = 'age'
    sex_col = 'sex'
    school_col = 'school'
    need_col = ['school', 'age', 'sex', 'grade', 'class', 'student_id', 'D', 'date_of_birth']
    return_col = ['school_id', 'age', 'male', 'grade', 'class','student_id', 'D', 'birth', 'years', 'month']
    school_mapper = {
        'Anouk Wat': 'NGS',
        'AW': 'NGS',
        'Krapeu Ha': 'KH',
        'Kroper Ha': 'KH',
        'KroperHa': 'KH',
        'Phum Thom': 'PT',
        'Prek Russey': 'PR',
        'Prek Reussey': 'PR',
        'PR': 'PR',
        'Wat Krous': 'WK',
        'NGS': 'NGS'
    }
    sex_mapper = {
        'M': 1,
        'F': 0
    }
    # check_col_exists
    for col in need_col:
        if not (col in df.columns):
            print('{col} does not exits in df'.format(col=col))
            raise KeyError
    # engineer
    df['birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
    df['years'] = pd.np.floor((pd.Timestamp.today() - df['birth'])/pd.np.timedelta64(1, 'Y'))
    df['month'] = df['birth'].dt.month
    # df['years'] = df[age_col].str.replace('Years.*', '') * 1
    # df['month'] = df[age_col].str.replace('.*Years, *', '') * 1
    # sex に関しては表記ゆれを回収しつつ寄せる必要がある.
    for sex in list(sex_mapper.keys()):
        slicing = df[sex_col].str.count(sex) > 0
        df.loc[slicing, 'male'] = sex_mapper[sex]
    print(df.loc[df['male'].isnull(), sex_col].unique())
    # school に関しては表記ゆれを回収しつつ寄せる必要がある.
    for school in list(school_mapper.keys()):
        slicing = df[school_col].str.count(school) > 0
        df.loc[slicing, 'school_id'] = school_mapper[school]
    print(df.loc[df['school_id'].isnull(), school_col].unique())
    # sasa
    return df[return_col]


def example():
    from src.read.national_assesment import read_national_assesment
    path_excel = "./data/original/national assessment .xlsx"
    df = read_national_assesment(path_excel)
    df_info1 = engineer_info(df)
    from src.read.timss import read_data_timss
    path_excel = "./data/original/TIMSS result.xlsx"
    df2 = read_data_timss(path_excel)
    df_info2 = engineer_info(df2)
