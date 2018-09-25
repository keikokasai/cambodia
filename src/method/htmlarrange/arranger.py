# sample code
import pandas as pd
import os


def str_mapping(data, mapper):
    data = data.replace('nan', '')
    data = data.replace('\(', '\'(')
    data = data.replace('\n', '\r\n')
    for m in mapper.keys():
        data = data.replace(m, mapper[m])
    return data


def df_str_mapping(data, mapper):
    data = data.astype(str)
    data = data.replace('nan', '')
    data = data.replace('\(', '\'(', regex=True)
    data = data.replace('\n', '\r\n', regex=True)
    for m in mapper.keys():
        data = data.replace(m, mapper[m], regex=False)
    for m in mapper.keys():
        data = data.replace(m, mapper[m], regex=True)
    return data


def tex_str_mapping(data, mapper):
    for m in mapper.keys():
        data = data.replace(m, mapper[m])
    return data


def create_summary_list_xlsx(folder_path, replace_name, mapper):
    summary_list = []
    summary_name_list = []
    for folder in os.walk(folder_path):
        foldername = folder[0]
        filelist = folder[2]
        for filename in filelist:
            if filename.count('html') > 0:
                res = foldername + '/' + filename
                print(res)
                summary = df_str_mapping(pd.read_html(res)[0], mapper)
                summary_list.append(summary)
                summary_name_list.append(filename)
    excel_writer = pd.ExcelWriter(path=replace_name)
    for summary, sheetname in zip(summary_list, summary_name_list):
        summary.to_excel(excel_writer, sheet_name=sheetname[:31], index=False, header=False)
    pd.DataFrame(summary_name_list).to_excel(excel_writer, sheet_name='memo')
    excel_writer.save()


def open_texfile(path):
    f = open(path, 'rb')
    txt = f.read().decode()
    f.close()
    return txt


def save_texfile(save_path, tex):
    f = open(save_path, 'w')
    f.write(tex)
    f.close()


def create_summary_list_tex(folder_path, mapper):
    replace_folder = folder_path + '/tex'
    if os.path.exists(replace_folder) is False:
        os.makedirs(replace_folder)
    for folder in os.walk(folder_path):
        foldername = folder[0]
        filelist = folder[2]
        for filename in filelist:
            if filename.count('tex') > 0:
                res = foldername + '/' + filename
                print(res)
                summary = tex_str_mapping(open_texfile(res), mapper)
                save_path = replace_folder + '/' + filename
                save_texfile(save_path=save_path, tex=summary)
