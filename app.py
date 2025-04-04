# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from random import choices, sample, randint

# 1. 配置问卷问题和选项
questions = {
    # 基本信息
    "Q1_身份": ["母亲", "父亲", "祖父母", "其他亲属"],
    "Q2_年龄": ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
    "Q3_学历": ["初中及以下", "高中/中专", "大专", "本科", "硕士及以上"],
    
    # 教育观念
    "Q4_能力培养": ["知识学习", "创造力", "规则意识", "情绪管理", "运动能力", "艺术兴趣"],
    "Q5_教育方法": ["耐心讲道理", "共同讨论", "批评责备", "冷处理"],
}

# 2. 设置论文中的精确数据分布
distributions = {
    # 基本信息分布（百分比）
    "Q1_身份": [68, 25, 5, 2],  # 母亲68%，父亲25%...
    "Q2_年龄": [3, 7, 40, 30, 20],
    "Q3_学历": [5, 20, 25, 45, 5],
    
    # 多选题分布（选择概率）
    "Q4_能力培养": [35, 52, 48, 45, 28, 15],  # 对应选项顺序
    "Q5_教育方法": [65, 58, 12, 8],  # 百分比
}

# 3. 数据生成核心函数
def generate_data(num=312):
    data = []
    for _ in range(num):
        record = {}
        
        # 生成单选题
        for q in ["Q1_身份", "Q2_年龄", "Q3_学历"]:
            record[q] = choices(questions[q], weights=distributions[q])[0]
        
        # 生成多选题（最多选3项）
        record["Q4_能力培养"] = "|".join(sample(
            questions["Q4_能力培养"],
            counts=distributions["Q4_能力培养"],
            k=randint(1, 3)  # 随机选1-3项
        ))
        
        # 生成教育方法选择
        record["Q5_教育方法"] = choices(
            questions["Q5_教育方法"],
            weights=distributions["Q5_教育方法"]
        )[0]
        
        data.append(record)
    return pd.DataFrame(data)

# 4. 创建网页界面
st.set_page_config(page_title="论文问卷数据生成器", layout="wide")
st.title("📝 家长教育观念问卷数据生成系统")
st.write("根据您论文中的分布要求自动生成问卷星格式数据")

# 侧边栏控制
with st.sidebar:
    st.header("控制面板")
    num = st.number_input("生成数据量", min_value=1, value=312)
    btn = st.button("生成数据", type="primary")

# 主界面
if btn:
    df = generate_data(num)
    st.success(f"成功生成 {num} 条数据！")
    
    # 显示数据预览
    st.dataframe(df.head())
    
    # 下载CSV文件
    csv = df.to_csv(index=False, encoding="utf_8_sig")  # 中文编码
    st.download_button(
        label="下载CSV文件",
        data=csv,
        file_name="问卷数据.csv",
        mime="text/csv"
    )
