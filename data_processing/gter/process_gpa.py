# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:39:44 2020

@author: HOILUI
"""
import pandas as pd
import csv
import re


# 正则匹配出gpa数据
def process_gpa(g):
    re1 = '[2, 3 ,4]+(\.[0-9]{1,2})/[4, 5]+(\.[0, 3, 4, 5]{1,2})'  # 匹配形如3.8/4.0的gpa
    re2 = '[2, 3, 4]+(\.[0-9]{1,2})/[4, 5]'  # 匹配形如3.8/4的gpa
    re3 = '[0-9]+(\.[0-9]{1,2})/100'  # 88.88/100
    re4 = '[0-9]{2,2}/100'  # 88/100
    re5 = '(?<!\.)([0-9]{2,2})'  # 88且数字前面不包含.，即不匹配3.88
    re6 = '[2, 3, 4]+(\.[0-9]{1,2})'  # 3.xx
    re7 = '(?<!\.)([0-9]{2,2})+(\.[0-9]{1,2})'  # XX.X or xx.X
    new_gpa = ''
    new_score = ''
    if re.search(re1, g) is not None:
        new_gpa = re.search(re1, g).group()

    elif (re.search(re2, g) is not None)and(re.search(re1, g) is None):
        new_gpa = re.search(re2, g).group()

    elif (re.search(re6, g) is not None)and(re.search(re2, g) is None)and(re.search(re1, g) is None):
        new_gpa = re.search(re6, g).group()

    if re.search(re3, g) is not None:
        new_score = re.search(re3, g).group()

    elif (re.search(re4, g) is not None)and(re.search(re3, g) is None):
        new_score = re.search(re4, g).group()

    elif (re.search(re7, g) is not None)and(re.search(re4, g) is None)and(re.search(re3, g) is None):
        new_score = re.search(re7, g).group()

    elif(re.search(re5, g) is not None)and(re.search(re3, g) is None)and(re.search(re4, g) is None)and(re.search(re7, g) is None):
        a = re.search(re5, g).group()
        if(int(a) < 100)and(int(a) > 70):
            new_score = a

    new_gpa = new_gpa.strip(' ').strip('\n').replace(',', '')
    new_score = new_score.strip(' ').strip('\n').replace(',', '')

    return new_gpa, new_score


# 四分绩点转为百分制均分
def four_grade_point2hundred_grade_point(g):
    g = g.strip(' ').strip('\n')
    g = float(g)
    score = (g - 1) * 10 + 60
    score = round(score, 2)
    return str(score)


def hundred_grade_point2four_grade_point(s):
    s = s.replace('/100', '').strip(' ').strip('\n')
    s = float(s)
    gpa = (s - 60) * 0.1 + 1
    if gpa > 4.0:
        gpa = 4.0
    gpa = round(gpa, 2)
    return str(gpa)


# 五分绩点转为百分制均分
def five_grade_poing2hundred_grade_point(g):
    g = g.strip(' ').strip('\n')
    g = float(g)
    score = (g+5) * 10
    score = round(score, 2)
    return str(score)


def hundred_grade_point2five_grade_point(s):
    s = s.replace('/100', '').strip(' ').strip('\n')
    s = float(s)
    gpa = s/10 - 5
    gpa = round(gpa, 2)
    return str(gpa)


# 4.3绩点转为百分制均分
def four_point_three2hundred_grade_point(g):
    g = g.strip(' ').strip('\n')
    g = float(g)
    score = (g+ 3.9466899) / 0.0861324
    score = round(score, 2)
    if score > 100:
        score = 100
    return str(score)


def hundred_grade_point2four_point_three(s):
    s = s.replace('/100', '').strip(' ').strip('\n')
    s = float(s)
    gpa = 0.0861324 * s - 3.9466899
    gpa = round(gpa, 2)
    if gpa > 4.3:
        gpa = 4.3

    return str(gpa)


def judge_gpa_system(g):
    g_list = g.split('/')
    gpa = ''
    total = ''
    if len(g_list) == 1:
        return g_list[0], '4.0'
    if len(g_list) == 2:
        gpa = g_list[0]
        total = g_list[1]
        return gpa, total
    else:
        return gpa, total


def if_gpa_valid(g):
    gpa, total = judge_gpa_system(g)
    if gpa != '':
        if float(gpa) > 4:
            g = ''
    return g


da = pd.read_csv('./data/applicants.csv')
da.insert(5, '本科4.0绩点', '')
da.insert(6, '本科4.3绩点', '')
da.insert(7, '本科5.0绩点', '')
da.insert(8, '本科均分', '')
da.insert(9, '本科原始成绩', '')
da.insert(13, '研究生4.0绩点', '')
da.insert(14, '研究生4.3绩点', '')
da.insert(15, '研究生5.0绩点', '')
da.insert(16, '研究生均分', '')
da.insert(17, '研究生原始成绩', '')


for i in range(len(da)):
    # 针对'1/64  3.58/4.0'会匹配出'4  3.58/4.0'的情况，把空格替换为','后续再去掉
    ug_gpa = ' ' + str(da['本科成绩和算法、排名'][i]).replace('／', '/').replace(' ', ',')
    pg_gpa = ' ' + str(da['研究生成绩和算法、排名'][i]).replace('／', '/').replace(' ', ',')
    if ug_gpa is not None:
        new_ug_gpa, new_ug_score = process_gpa(ug_gpa)
        new_ug_gpa = if_gpa_valid(new_ug_gpa)
        new_ug_gpa4 = ''
        new_ug_gpa5 = ''
        new_ug_gpa4_3 = ''
        if (new_ug_gpa == '')and(new_ug_score != ''):
            score, total = judge_gpa_system(new_ug_score)
            new_ug_gpa4 = hundred_grade_point2four_grade_point(score)
            new_ug_gpa5 = hundred_grade_point2five_grade_point(score)
            new_ug_gpa4_3 = hundred_grade_point2four_point_three(score)

        elif(new_ug_score == '')and(new_ug_gpa != ''):
            gpa, total = judge_gpa_system(new_ug_gpa)
            if(total == '4.0')or(total == '4')or(total == '4.00'):
                # print(new_ug_gpa)
                new_ug_score = four_grade_point2hundred_grade_point(gpa)
                new_ug_gpa4 = gpa
                new_ug_gpa5 = hundred_grade_point2five_grade_point(new_ug_score)
                new_ug_gpa4_3 = hundred_grade_point2four_point_three(new_ug_score)
            elif(total == '5.0')or(total == '5')or(total == '5.00'):
                # print(new_ug_gpa)
                new_ug_score = five_grade_poing2hundred_grade_point(gpa)
                new_ug_gpa4 = hundred_grade_point2four_grade_point(new_ug_score)
                new_ug_gpa4_3 = hundred_grade_point2four_point_three(new_ug_score)
                new_ug_gpa5 = gpa
            elif(total == '4.3')or(total == '4.30'):
                print(new_ug_gpa)
                new_ug_score = four_point_three2hundred_grade_point(gpa)
                new_ug_gpa4 = hundred_grade_point2four_grade_point(new_ug_score)
                new_ug_gpa5 = hundred_grade_point2five_grade_point(new_ug_score)
                new_ug_gpa4_3 = gpa

        elif(new_ug_gpa != '')and(new_ug_score != ''):
            score, total = judge_gpa_system(new_ug_score)
            new_ug_gpa4 = new_ug_gpa
            new_ug_gpa4_3 = hundred_grade_point2four_point_three(score)
            new_ug_gpa5 = hundred_grade_point2five_grade_point(score)

        # 统一格式，把3.XX/4.0转换为3.XX
        new_ug_gpa4, a = judge_gpa_system(new_ug_gpa4)
        new_ug_gpa4_3, d = judge_gpa_system(new_ug_gpa4_3)
        new_ug_gpa5, c = judge_gpa_system(new_ug_gpa5)
        new_ug_score, b = judge_gpa_system(new_ug_score)

        da['本科4.0绩点'][i] = new_ug_gpa4
        da['本科4.3绩点'][i] = new_ug_gpa4_3
        da['本科5.0绩点'][i] = new_ug_gpa5
        da['本科均分'][i] = new_ug_score
        da['本科原始成绩'][i] = da['本科成绩和算法、排名'][i]

    # 处理研究生成绩
    if pg_gpa is not None:
        new_pg_gpa, new_pg_score = process_gpa(pg_gpa)
        new_pg_gpa = if_gpa_valid(new_pg_gpa)
        new_pg_gpa4 = ''
        new_pg_gpa4_3 = ''
        new_pg_gpa5 = ''
        if(new_pg_gpa == '')and(new_pg_score != ''):
            pscore, ptotal = judge_gpa_system(new_pg_score)
            new_pg_gpa4 = hundred_grade_point2four_grade_point(pscore)
            new_pg_gpa4_3 = hundred_grade_point2four_point_three(pscore)
            new_pg_gpa5 = hundred_grade_point2five_grade_point(pscore)

        elif(new_pg_score == '')and(new_pg_gpa != ''):
            pgpa, ptotal = judge_gpa_system(new_pg_gpa)
            if(ptotal == '4.0')or(ptotal == '4')or(ptotal == '4.00'):
                # print(new_pg_gpa)
                new_pg_score = four_grade_point2hundred_grade_point(pgpa)
                new_pg_gpa5 = hundred_grade_point2five_grade_point(new_pg_score)
                new_pg_gpa4_3 = hundred_grade_point2four_point_three(new_pg_score)
                new_pg_gpa4 = pgpa
            elif(ptotal == '5.0')or(ptotal == '5'or(ptotal == '5.00')):
                # print(new_pg_gpa)
                new_pg_score = five_grade_poing2hundred_grade_point(pgpa)
                new_pg_gpa4 = hundred_grade_point2four_grade_point(new_pg_score)
                new_pg_gpa4_3 = hundred_grade_point2four_point_three(new_pg_score)
                new_pg_gpa5 = pgpa
            elif(ptotal == '4.3')or(ptotal == '4.30'):
                print(new_pg_gpa)
                new_pg_score = four_point_three2hundred_grade_point(pgpa)
                new_pg_gpa4 = hundred_grade_point2four_grade_point(new_pg_score)
                new_pg_gpa5 = hundred_grade_point2five_grade_point(new_pg_score)
                new_pg_gpa4_3 = pgpa
        elif(new_pg_gpa != '')and(new_pg_score != ''):
            score, total = judge_gpa_system(new_pg_score)
            new_pg_gpa4 = new_pg_gpa
            new_pg_gpa4_3 = hundred_grade_point2four_point_three(score)
            new_pg_gpa5 = hundred_grade_point2five_grade_point(score)

        # 统一格式，把3.XX/4.0转换为3.XX
        new_pg_gpa4, a = judge_gpa_system(new_pg_gpa4)
        new_pg_gpa4_3, d = judge_gpa_system(new_pg_gpa4_3)
        new_pg_gpa5, c = judge_gpa_system(new_pg_gpa5)
        new_pg_score, b = judge_gpa_system(new_pg_score)

        da['研究生4.0绩点'][i] = new_pg_gpa4
        da['研究生4.3绩点'][i] = new_pg_gpa4_3
        da['研究生5.0绩点'][i] = new_pg_gpa5
        da['研究生均分'][i] = new_pg_score
        da['研究生原始成绩'][i] = da['研究生成绩和算法、排名'][i]

da = da.drop(['本科成绩和算法、排名', '研究生成绩和算法、排名'], axis=1)
da.to_csv('./data/new_applicants.csv')