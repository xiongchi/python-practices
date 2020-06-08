# coding:utf-8

import os

import configparser

'''
    基础读取配置文件
        -read(filename)         直接读取文件内容
        -sections()             得到所有的section，并以列表的形式返回
        -options(section)       得到该section的所有option
        -items(section)         得到该section的所有键值对
        -get(sectionoption)    得到section中option的值，返回为string类型
        -getint(section,option) 得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。
'''


class GetIni(object):

    # 初始化配置文件对象
    def __init__(self, path, parent_path=None):
        self.cf = configparser.ConfigParser()
        if parent_path is None:
            pro_path = os.path.abspath(os.path.abspath(os.getcwd()))
            # 实例化
        else:
            pro_path = parent_path
        # 读取配置文件
        self.cf.read(pro_path + '/' + path)

    # 获取所有的sections
    def get_sections(self):
        sections = self.cf.sections()
        return sections

    # 获取section下的所有key
    def get_options(self,section):
        opts = self.cf.options(section=section)
        return opts

    # 获取section下的所有键值对
    def get_kvs(self,section):
        kvs = self.cf.items(section=section)
        kvs_dict = dict()
        for i in kvs:
            kvs_dict[i[0]] = i[1]
        return kvs_dict

    # 根据section和option获取指定的value
    def get_key_value(self,section,option):
        opt_val = self.cf.get(section=section,option=option)
        return opt_val
