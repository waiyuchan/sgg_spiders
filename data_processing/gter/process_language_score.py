# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:11:12 2020

@author: zmddzf
"""

import pandas as pd
import re
import jieba

def preprocess(sent):
    # 标点符号
    punctuation_pattern = "[\`\~\!\@\#\$\^\&\*\(\)\（\）\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\【】\，\、\。\·\；\：\‘\“\”\'\\n\[A-Za-z0-9]"
    # 表情符号
    emoji_pattern = u'[\uD800-\uDBFF][\uDC00-\uDFFF]'
    # 开始清洗
    sent = re.sub(punctuation_pattern, '', sent)
    sent = re.sub(emoji_pattern, '', sent)
    sent = " ".join(jieba.cut(sent))  # 分词
    return sent

# 读取待处理数据
offers = pd.read_csv('../../gter_spider/data/offer.csv')
applicants = pd.read_csv('../../gter_spider/data/applicants.csv')

# 保留2016年以及之后的数据
offers['通知时间'] = pd.to_datetime(offers['通知时间'])
offers = offers.set_index('通知时间')
offers = offers[2016:]

offers = offers.set_index('入学年份')
offers = offers[offers.index>=2016]

applicants = applicants[applicants.aid.isin(offers.aid)].replace(pd.NA, '')

offers = offers.set_index('aid')
applicants = applicants.set_index('aid')


# 拆分成绩
ielts = applicants.IELTS.str.extract('Overall: (.*?),                     R: (.*?) /                    L: (.*?) /                    S: (.*?) /                    W: (.*?)$').replace(pd.NA, '')
ielts.columns = ['IELTS_Overall', 'IELTS_R', 'IELTS_L', 'IELTS_S', 'IELTS_W']

toefl = applicants.TOEFL.str.extract('Overall: (.*?),                     R: (.*?) /                    L: (.*?) /                    S: (.*?) /                    W: (.*?)$').replace(pd.NA, '')
toefl.columns = ['TOEFL_Overall', 'TOEFL_R', 'TOEFL_L', 'TOEFL_S', 'TOEFL_W']

gre = applicants.GRE.str.extract('Overall: (.*?),                     V: (.*?) /                    Q: (.*?) /                    AW: (.*?)$').replace(pd.NA, '')
gre.columns = ['GRE_Overall', 'GRE_V', 'GRE_Q', 'GRE_AW']

gmat = applicants.GMAT.str.extract('Overall: (.*?),                     Q: (.*?) /                    V: (.*?)$').replace(pd.NA, '')
gmat.columns = ['GMAT_Overall', 'GMAT_Q', 'GMAT_V']

lsat = applicants.LSAT.str.extract('(\d*)').replace(pd.NA, '')
lsat.columns = ['LSAT']

# 文本清洗
applicants['其他说明'] = applicants.apply(lambda x:preprocess(x['其他说明']),axis=1)

# 拼接与整理
del applicants['IELTS'], applicants['TOEFL'], applicants['GMAT'], applicants['GRE'], applicants['LSAT']
applicants = applicants.join(ielts).join(toefl).join(gre).join(gmat).join(lsat)

# offer数据进行清洗
offers = offers.replace(pd.NA, '')
offers['专业'] = offers.apply(lambda x: eval(x['专业'])[0], axis=1)

# 保存数据
applicants.to_csv('./data/applicants.csv')
offers.to_csv('./data/offers.csv')





