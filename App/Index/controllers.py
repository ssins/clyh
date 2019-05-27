import pulp
import numpy as np
from App.Index import static_folder
import os
import sys
from werkzeug import secure_filename
from config import ALLOWED_EXTENSIONS
from flask import redirect, url_for
import time
from App.Index.models import Work


def _allowed_file(filename):
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in ALLOWED_EXTENSIONS)


def upload_files(file):
    if file and _allowed_file(file.filename):
        filename = '{}.txt'.format(int(time.time()))
        pre_path = os.path.join(static_folder, 'upload')
        if not os.path.exists(pre_path):
            os.makedirs(pre_path)
        path = os.path.join(pre_path, filename)
        file.save(path)
        return path
    return None


def cal_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        target_dict = {}
        try:
            for i, line in enumerate(lines):
                tmp = line.strip().split()
                if i == 0:
                    if len(tmp) > 0:
                        source_list = [int(source) for source in tmp]
                elif i == 1:
                    if len(tmp) > 0:
                        target_add = int(tmp[0])
                else:
                    if len(tmp) > 1:
                        leng = int(tmp[0])
                        num = int(tmp[1])
                        target_dict[leng] = num
        except:
            return '文件格式错误'
        result_lines = get_result_string(source_list, target_dict, target_add)
        save_path = path.replace('upload', 'download')
        with open(save_path, 'w+', encoding='utf-8') as fo:
            fo.writelines([line+'\n' for line in result_lines])
        return redirect(url_for('index.download', path=save_path))
        


def getMinResult(z, a, b):
    m = pulp.LpProblem(sense=pulp.LpMinimize)
    x = [pulp.LpVariable(f'x{i}', lowBound=0, cat=pulp.LpInteger)
         for i in range(len(z))]
    m += pulp.lpDot(z, x)
    for i in range(len(a)):
        m += (pulp.lpDot(a[i], x) >= b[i])
    m.solve()
    return pulp.value(m.objective), [pulp.value(var) for var in x]


def getAllMethods(source_len_list, target_len_dict):
    source_len_list.sort()
    methods = [[0] * len(target_len_dict)]
    methods_len = [0, ]
    values = [0, ]
    for idx, (length, max_count) in enumerate(target_len_dict.items()):
        new_methods = []
        new_values = []
        new_methods_len = []
        for count in range(1, max_count + 1):
            for i, method in enumerate(methods):
                tmp_value = values[i] + length*count
                for source_len in source_len_list:
                    if tmp_value <= source_len:
                        tmp_method = method[:]
                        tmp_method[idx] = count
                        new_methods.append(tmp_method)
                        new_values.append(tmp_value)
                        new_methods_len.append(source_len)
                        break
        methods += new_methods
        methods_len += new_methods_len
        values += new_values
    return methods, methods_len


def getMinMethods(old_list, methods_len_list):
    source_list = old_list[:]
    methods_len = methods_len_list[:]
    new_list = []
    new_len = []
    count = 0
    length = len(source_list)
    while count != length:
        count = 0
        length = len(source_list)
        new_list = []
        new_len = []
        for i in range(len(source_list) - 1):
            m1 = source_list[i]
            l1 = methods_len[i]
            m2 = source_list[i+1]
            for j in range(len(m1)):
                if m1[j] > m2[j]:
                    new_list.append(m1)
                    new_len.append(l1)
                    count += 1
                    break
        if length > 0:
            new_list.append(source_list[length-1])
            new_len.append(methods_len[length-1])
            count += 1
        source_list = new_list[:]
    return new_list, new_len


def get_result_string(source_list, target, target_add, is_always=False):
    source_bu = source_list
    target_bu = target.copy()

    w = Work(source_bu,target_bu,target_add,False)

    if target_add:
        tmp_t = {}
        for key, val in target.items():
            tmp_t[key+target_add] = val
        target = tmp_t

    if not is_always:
        source_list = [source + target_add for source in source_list]

    methods, methods_len = getAllMethods(source_list, target)
    min_methods, min_methods_len = getMinMethods(methods, methods_len)
    a = np.transpose(min_methods).tolist()
    b = list(target.values())
    z = [1]*len(a[0])
    r, l = getMinResult(z, a, b)

    out_lines = []

    lens = list(target_bu.keys())
    r_b = [0] * len(b)
    out_lines.append('料材：{}\t锯缝：{}'.format(source_bu[0], target_add))
    out_lines.append('-----------------------------------------------------')
    out_lines.append('总计：{}'.format(int(r)))
    out_lines.append('数量\t-->\t分割方案')
    for i, num in enumerate(l):
        if num > 0:
            out = '{}\t-->'.format(int(num))
            for j, count in enumerate(min_methods[i]):
                if count > 0:
                    out += '\t{} ×{}'.format(lens[j], count)
                    r_b[j] += num*count
            out_lines.append(out)
            #print(' {} --> {}'.format(min_methods[i], int(num)))

    out_lines.append('-----------------------------------------------------')
    out_lines.append('长度\t需求量\t实际分割\t(多余)')
    r_b = [int(i) for i in r_b]
    for i in range(len(b)):
        out_lines.append(
            '{}\t{}\t{}\t(+{})'.format(lens[i], b[i], r_b[i], r_b[i]-b[i]))
    return out_lines
