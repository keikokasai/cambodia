class Mapper:
    map_type = []
    def __init__(self):
        pass

    def get_all_mapper(self):
        mapper = {}
        for attr in self.__dir__():
            if attr.count('mapper') > 0:
                if type(self.__getattribute__(attr)) is dict:
                    mapper.update(self.__getattribute__(attr))
        return mapper


class MapperProvider:
    def __init__(self, map_object_list):
        self.map_object_list = map_object_list

    def provide(self):
        mapper = {}
        for map_object in self.map_object_list:
            mapper.update(map_object.get_all_mapper())
        return mapper


class ColumnNameEnglishMapper(Mapper):
    map_type = ['en']
    rename_mapper = {
        '(z)?(C|c)ram': 'Cram',
        '(z)?(C|c)ramschool': 'CramTime',
        '(z)?(t|T)eacherrelation': 'TeacherRelation',
        '(z)?(i|I)nputweek': 'InputWeek',
        '(z)?(f|F)riendrelation': 'FriendRelation',
        'cram': 'Cram',
        'cramschool': 'CramTime',
        'teacherrelation': 'TeacherRelation',
        'inputweek': 'InputWeek',
        'friendrelation': 'FriendRelation',
    }
    mapper = {
        'pq1_1': 'father education:',
        'pq1_2': 'mother education:',
        'pq2': '# of family',
        'pq3': '# of children',
        'pq4': 'studying time: Mon-Sat(m)',
        'pq5': 'studying time: Sun(m)',
        'pq6': 'ideal studying time: Mon~Sat(m)',
        'pq7': 'ideal studying time: Sun(m)',
        'pq8': 'will your children go to university?',
        'pq10': 'saving',
        'pq11': 'saving for education',
        'prelationship': 'relationship with kids',
        'after_nat_ass': 'after: national assessment',
        'before_nat_ass': 'before: national assessment',
        'after_timss': 'after: timss',
        'before_timss': 'before: timss',
        ' ^ D$': 'thinkthink_dummy'
    }
