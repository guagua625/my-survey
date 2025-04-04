import streamlit as st
import pandas as pd
from random import choices, sample, randint

# 配置数据分布（完全匹配你的表格）
distributions = {
    # 基本信息
    "家长身份": ["母亲", "父亲", "祖父母/外祖父母", "其他亲属"],
    "身份分布": [0.68, 0.25, 0.05, 0.02],
    
    "年龄": ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
    "年龄分布": [0.03, 0.07, 0.40, 0.30, 0.20],
    
    "学历水平": ["初中及以下", "高中/中专", "大专", "本科", "硕士及以上"],
    "学历分布": [0.05, 0.20, 0.25, 0.45, 0.05],
    
    "职业类型": ["公务员/事业单位", "教师", "企业职员", "自由职业", "全职家长", "个体户", "其他"],
    "职业分布": [0.10, 0.15, 0.35, 0.10, 0.25, 0.05, 0.15],
    
    "家庭月收入": ["3000元及以下", "3000-5000元", "5000-8000元", "8000-12000元", "12000元及以上"],
    "收入分布": [0.20, 0.20, 0.40, 0.20, 0.10],
    
    "家庭结构": ["核心家庭", "三代同堂", "单亲家庭", "其他"],
    "家庭结构分布": [0.65, 0.25, 0.08, 0.02],
    
    # 教育观念
    "能力培养偏好": ["创造力", "规则意识", "情绪管理", "知识学习", "运动能力", "艺术兴趣", "其他"],
    "能力分布": [0.52, 0.48, 0.45, 0.35, 0.28, 0.15, 0.04],
    
    "长期发展期待": [
        "身心健康，快乐成长", "具备良好的道德品质", "拥有独立自主的能力",
        "考上名牌大学", "有稳定的高收入工作", "发展广泛的兴趣爱好或特长", "其他"
    ],
    "期待分布": [0.78, 0.65, 0.58, 0.30, 0.25, 0.20, 0.05],
    
    # 评分题分布
    "游戏重要性": [0.02, 0.04, 0.14, 0.35, 0.45],  # 1-5分分布
    "自由探索": [0.01, 0.03, 0.10, 0.30, 0.56],
    "提前学习抑制创造力": [0.15, 0.25, 0.30, 0.20, 0.10],
    "学科知识融入游戏": [0.05, 0.10, 0.20, 0.25, 0.40],
    "每日专注互动": [0.05, 0.10, 0.20, 0.20, 0.45],
    "教育焦虑程度": [0.05, 0.10, 0.25, 0.30, 0.30]
}

def generate_rating(dist):
    return choices([1,2,3,4,5], weights=dist)[0]

def generate_data(num_records):
    data = []
    for _ in range(num_records):
        record = {}
        
        # 生成基本信息
        record["家长身份"] = choices(distributions["家长身份"], weights=distributions["身份分布"])[0]
        record["年龄"] = choices(distributions["年龄"], weights=distributions["年龄分布"])[0]
        record["学历水平"] = choices(distributions["学历水平"], weights=distributions["学历分布"])[0]
        record["职业类型"] = choices(distributions["职业类型"], weights=distributions["职业分布"])[0]
        record["家庭月收入"] = choices(distributions["家庭月收入"], weights=distributions["收入分布"])[0]
        record["家庭结构"] = choices(distributions["家庭结构"], weights=distributions["家庭结构分布"])[0]
        
        # 生成教育观念数据
        # 多选题：能力培养偏好（选3项）
        abilities = choices(
            distributions["能力培养偏好"],
            weights=distributions["能力分布"],
            k=3
        )
        record["能力培养偏好"] = "|".join(abilities)
        
        # 多选题：长期发展期待（选3项）
        expectations = choices(
            distributions["长期发展期待"],
            weights=distributions["期待分布"],
            k=3
        )
        record["长期发展期待"] = "|".join(expectations)
        
        # 生成评分题
        record["游戏重要性评分"] = generate_rating(distributions["游戏重要性"])
        record["自由探索评分"] = generate_rating(distributions["自由探索"])
        record["提前学习抑制创造力评分"] = generate_rating(distributions["提前学习抑制创造力"])
        record["学科知识融入游戏认同度"] = generate_rating(distributions["学科知识融入游戏"])
        record["每日专注互动时间"] = generate_rating(distributions["每日专注互动"])
        record["教育焦虑程度"] = generate_rating(distributions["教育焦虑程度"])
        
        data.append(record)
    return pd.DataFrame(data)

# 网页界面
st.title("家长教育问卷数据生成器")
st.markdown("根据论文要求精确生成数据分布")

num_records = st.number_input("要生成多少份数据？", min_value=1, value=312)

if st.button("生成数据"):
    df = generate_data(num_records)
    st.write("生成数据预览：")
    st.dataframe(df.head())
    
    # 导出CSV
    csv = df.to_csv(index=False, encoding='utf-8-sig')  # 解决中文乱码
    st.download_button(
        label="下载CSV文件",
        data=csv,
        file_name='问卷数据.csv',
        mime='text/csv'
    )
