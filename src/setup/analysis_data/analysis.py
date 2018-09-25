import pandas as pd
from functools import reduce
from src.setup.mapper import Mapper
from src.lib import tidy_to_wide

class Visitor:
    path = './data/work/info.csv'
    def __init__(self, ** argv):
        for attr_name in list(argv.keys()):
            self.__setattr__(attr_name, argv[attr_name])

    def build(self):
        df = self.read()
        self.data = df
        return self

    def read(self):
        return pd.read_csv(self.path)


class Accepter:
    key = None
    def __init__(self, ** argv):
        for attr_name in list(argv.keys()):
            self.__setattr__(attr_name, argv[attr_name])

    def build(self):
        df = self.read()
        self.data = df
        return self

    def read(self):
        return pd.read_csv(self.path, encoding='sjis')

    def accept(self):
        pass


class ScoreAccepter(Accepter):
    path = './data/work/score.csv'
    key = 'student_id'
    score_type = 'all'
    value_name = 'value'
    col_name = 'correct_answer_rate'
    test_type = 'NationalAssesment'

    def accept(self, v):
        vis_data = v.data
        df = self.data
        # df = pd.read_csv(path, encoding='sjis')
        key = self.key
        value_name = self.value_name
        col_name = self.col_name
        test_type = self.test_type
        timing_list = ['before', 'after']
        for timing in timing_list:
            slicing1 = df['test_type'] == test_type
            slicing2 = df['timing'] == timing
            slicing3 = df['qes'] == col_name
            slicing = reduce(pd.np.logical_and, [slicing1, slicing2, slicing3])
            df_slice = df.loc[slicing, [key, 'value']]\
                .rename(columns = {'value': timing + '_' + value_name})
            vis_data = pd.merge(vis_data, df_slice, on=key, how='left')
        v.data = vis_data


class ParentAccepter(Accepter):
    path = './data/work/parent.csv'
    keys = ['student_id']
    qes_col = 'qes'
    value_name = 'value'
    column_mapper = Mapper.parent_survey
    fetch_cols = None

    def accept(self, v):
        # df = pd.read_csv(path, encoding='sjis')
        vis_data = v.data
        df = self.data
        keys = self.keys
        qes_col = self.qes_col
        value_name = self.value_name
        fetch_cols = self.fetch_cols
        slicing1 = df['qes'].isin(fetch_cols)
        slicing = reduce(pd.np.logical_and, [slicing1])
        df_slice = df.loc[slicing, :]
        df_wide = tidy_to_wide(
            df = df_slice,
            keys=keys,
            qes_col=qes_col,
            value_col=value_name,
            fetch_cols=fetch_cols)
        # import pdb;pdb.set_trace()
        df_wide_rename = df_wide.rename(columns=self.column_mapper)
        vis_data = pd.merge(vis_data, df_wide_rename, on=keys, how='left')
        v.data = vis_data



def main():
    v = Visitor().build()
    sa = ScoreAccepter(test_type='NationalAssesment',
                       value_name='nat_ass').build()
    sa2 = ScoreAccepter(test_type='TIMSS',
                       value_name='timss').build()
    fetch_cols = [
        'relationship',
        'q1_1', 'q1_2', 'q1_3', 'q2', 'q3', 'q4', 'q5', 'q6',
        'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16']
    pa = ParentAccepter(fetch_cols=fetch_cols).build()
    for accepter in [sa, sa2, pa]:
        accepter.accept(v)
    v.data.to_csv('./data/tmp/tmp.csv', index=False, encoding='sjis')

    # from src.setup.work import info
    # wei = info(drop_duplicated_id=False)