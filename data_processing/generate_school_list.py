# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:09:16 2020

@author: zmddzf
"""
import pandas as pd

# 读取数据
df = pd.read_excel('common_source/times_ranking.xlsx', dtype=object)

# 取出部分有用的属性
en_name = list(df['英文学校名称'])
cn_name = list(df['学校名称'])
code = list(df['编号'])

# 生成英文首字母简称
en_simp_name = []
for name in en_name:
    words = name.split(' ')
    if len(words) == 1:
        en_simp_name.append(name)
        continue
    simp = ''.join([i[0].casefold() for i in words])
    en_simp_name.append(simp)


en_name = [name.casefold().replace(' ', '') for name in en_name]


# 生成中文潜在的简写（去除“大学”、“学院”）
cn_simp_name = []
for name in cn_name:
    words = name.replace('学院', '')
    words = words.replace('大学', '')
    cn_simp_name.append(words)

# 生成学校列表
school_df = pd.DataFrame(columns=['code', 'en_name', 'en_simp', 'cn_name', 'cn_simp'])
school_df.code = code
school_df.en_name = en_name
school_df.en_simp = en_simp_name
school_df.cn_name = cn_name
school_df.cn_simp = cn_simp_name

# 存储
school_df.to_csv('./common_source/school_list.csv', index=None)







