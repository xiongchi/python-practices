# -*- coding: utf-8 -*-


# 基本插入
def base_insert(obj, table, db):
    key_str = ''
    s_str = ''
    value_dict = []
    for key, value in obj.items():
        key_str += '`' + str(key) + '`,'
        s_str += '%s,'
        value_dict.append(value)
    key_str = key_str[:len(key_str) - 1]
    s_str = s_str[:len(s_str) - 1]
    sql = 'insert `' + table + '`(' + key_str + ')' + ' values(' + s_str + ')'
    obj_insert = db.insertOne(sql, tuple(value_dict))
    return obj_insert


# 不提交的新增
def not_commit_insert(obj, table, cursor):
    key_str = ''
    s_str = ''
    value_dict = []
    for key, value in obj.items():
        key_str += '`' + str(key) + '`,'
        s_str += '%s,'
        value_dict.append(value)
    key_str = key_str[:len(key_str) - 1]
    s_str = s_str[:len(s_str) - 1]
    sql = 'insert `' + table + '`(' + key_str + ')' + ' values(' + s_str + ')'
    cursor.execute(sql, tuple(value_dict))
    return cursor.lastrowid


# 不提交的更新
def not_commit_upd(revises, conditions, table, cursor):
    r = []
    c = []
    for k, v in revises.items():
        s = k + "='" + str(v) + "'"
        r.append(s)
    for k, v in conditions.items():
        cs = k + "='" + str(v) + "'"
        c.append(cs)
    r_str = (',').join(r)
    c_str = (' and ').join(c)
    sql = 'update `' + table + '` set ' + r_str + ' where ' + c_str
    cursor.execute(sql)


# 基本插入
def base_insert_many(obj_arr, table, db):
    if obj_arr is None or len(obj_arr) == 0:
        return None
    obj_column = obj_arr[0]
    columns = []
    key_str = ''
    s_str = ''
    for key in obj_column:
        key_str += '`' + str(key) + '`,'
        s_str += '%s,'
        columns.append(str(key))
    key_str = key_str[:len(key_str) - 1]
    s_str = s_str[:len(s_str) - 1]
    comp_arr = []
    for obj in obj_arr:
        o_arr = []
        for c in columns:
            o_arr.append(obj[c])
        comp_arr.append(tuple(o_arr))
    sql = 'insert ' + table + '(' + key_str + ')' + ' values(' + s_str + ')'
    obj_insert = db.insertMany(sql, comp_arr)
    return obj_insert


# 基本查询
def base_sel(params, table, db):
    k_v = []
    sql = ''
    for k, v in params.items():
        s = k + "='" + v + "'"
        k_v.append(s)
    if len(k_v) != 0:
        sql += ' where ' + (' and ').join(k_v)
    result = db.getAll('select * from ' + table + sql)
    return result
