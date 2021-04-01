# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 22:35:15 2020

@author: zmddzf
"""

import pandas as pd
import re

def match_school(name, school_list):
    """
    :param name: 待匹配学校名称
    :param school_list: 匹配学校列表
    """
    codes = school_list.code.tolist()
    en_name = school_list.en_name.tolist()
    en_simp = school_list.en_simp.tolist()
    cn_name = school_list.cn_name.tolist()
    cn_simp = school_list.cn_simp.tolist()
    
    pattern = re.compile(r'[a-z/A-Z]')
    
    processed_name = str(name).replace(' ', '').casefold()
    en_processed_name = ''.join(pattern.findall(processed_name))
    cn_processed_name = pattern.sub('', processed_name)
    
    if en_processed_name in en_name:
        code = codes[en_name.index(en_processed_name)]
        return True, code
    elif en_processed_name in en_simp:
        code = codes[en_simp.index(en_processed_name)]
        return True, code
    elif cn_processed_name in cn_name:
        code = codes[cn_name.index(cn_processed_name)]
        return True, code
    elif cn_processed_name in cn_simp:
        code = codes[cn_simp.index(cn_processed_name)]
        return True, code
    else:
        return False, None

# 读取offer
offers = pd.read_csv('data/offers.csv', dtype=str)
# 读取学校列表
school_list = pd.read_csv('../common_source/school_list.csv', dtype=str)

# 开始匹配
school_codes = []
for name in offers['申请学校']:
    if name:
        _, code = match_school(name, school_list)
        print(_)
        school_codes.append(code)
    else:
        school_codes.append(None)
        continue

offers['school_code'] = school_codes
offers.to_csv('./data/offers.csv', index=None)