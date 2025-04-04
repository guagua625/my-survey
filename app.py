import streamlit as st
import pandas as pd
from random import choices

# 问题配置
questions = {
    "家长身份": ["母亲", "父亲", "祖父母/外祖父母", "其他亲属"],
    "年龄": ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
    "学历水平": ["初中及以下", "高中/中专", "大专", "本科", "硕士及以上"],
}

# 数据分布
distributions = {
    "家长身份": [68, 25, 5, 2],  # 百分比去掉%号，如68代表68%
    "年龄": [3, 7, 40, 30, 20],
    "学历水平": [5, 20, 25, 45, 5],
}

def generate_data(num=312):
    data = []
    for _ in range(num):
        row = {}
        # 生成基本信息
        for key in questions:
            row[key] = choices(questions[key], weights=distributions[key])[0]
        data.append(row)
    return pd.DataFrame(data)

# 网页界面
st.title('家长教育问卷数据生成器')
num = st.number_input('要生成多少份数据?', value=312)
if st.button('生成'):
    df = generate_data(num)
    st.write(df.head())
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('下载CSV', data=csv, file_name='data.csv')
