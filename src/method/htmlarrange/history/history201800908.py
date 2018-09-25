from src.lib.htmlarrange.arranger import *
from src.lib.mapper import *

mapper = MapperProvider([ColumnNameEnglishMapper(),
                         ComposerMapper(),
                         FactorMapper()])\
    .provide()

target_list =  [
    # ['notebooks/Yamaguchi/RAE/20180618/res/20180908/t1t2/'],
    # ['notebooks/Yamaguchi/RAE/20180618/res/20180908/t3/'],
    # ['notebooks/Yamaguchi/RAE/20180618/res/20180908/t4/'],
    # ['notebooks/Yamaguchi/RAE/20180618/res/20180908/t5/'],
    # ['notebooks/Yamaguchi/RAE/20180618/res/20180908/t6/'],
    # ['notebooks/Yamaguchi/RAE/20180618/res/20180908/t7/'],
    ['notebooks/Yamaguchi/RAE/20180618/res/20180908/t8/'],
    ['notebooks/Yamaguchi/RAE/20180618/res/20180908/t9/']
]
# colspanにread_html対応していねえ。。。
for target in target_list:
    print(target)
    folder_path = target[0]
    replace_name = folder_path + 'tmp.xlsx'
    create_summary_list_xlsx(folder_path, replace_name, mapper)




# def remove_file(folder_path):
#     import os
#     for folder in os.walk(folder_path):
#         foldername = folder[0]
#         filelist = folder[2]
#         for filename in filelist:
#             if filename.count('tmp.xlsx') > 0:
#                 print(os.path.join(foldername, filename))
#                 os.remove(os.path.join(foldername, filename))
#
# folder_path = 'notebooks/Yamaguchi/RAE/20180618/res/20180908'
# remove_file(folder_path)


