import streamlit as st
import pandas as pd
import numpy as np
from random import choices, randint
from faker import Faker
from io import BytesIO

# 初始化模拟数据生成器
fake = Faker('zh_CN')

# 配置数据分布（完整匹配你的表格）
distributions = {
    # 基本信息
    "家长身份": ["母亲", "父亲", "祖父母/外祖父母", "其他亲属"],
    "身份分布": [0.68, 0.25, 0.05, 0.02],
    
    "年龄": ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
    "年龄分布": [0.03, 0.07, 0.40, 0.30, 0.20],
    # ... 其他分布配置保持不变，需补充完整
}

def generate_ip(province):
    """生成指定省份的模拟IP地址"""
    ip_pool = {
        '广东': ['119.123.', '120.230.', '112.96.'],
        '湖北': ['59.174.', '59.172.'],
        '江苏': ['49.82.', '180.98.'],
        '其他': ['123.123.', '124.124.']
    }
    base = ip_pool.get(province, ip_pool['其他'])[randint(0,1)] 
    return base + f"{randint(1,255)}.{randint(1,255)}"

def generate_data(num_records):
    data = []
    for i in range(1, num_records+1):
        record = {
            # 固定字段
            "序号": i,
            "提交答卷时间": fake.date_time_between(start_date="-30d", end_date="now").strftime("%Y/%m/%d %H:%M:%S"),
            "所用时间": randint(30, 1800),
            "来源": choices(["微信", "手机提交"], weights=[0.8,0.2])[0],
            "来源详情": "N/A",
            "来自IP": generate_ip(choices(["广东", "湖北", "江苏", "其他"], weights=[0.6,0.1,0.2,0.1])[0]) + f"({fake.province()})",
            
            # 单选题（示例）
            "1.您是孩子的:": choices([1,2,3,4], weights=[0.68,0.25,0.05,0.02])[0],
            "2.您的年龄:": choices([1,2,3,4,5], weights=[0.03,0.07,0.40,0.30,0.20])[0],
            # ... 补充其他单选题
            
            # 多选题（示例）
            "1.您认为幼儿阶段应优先培养以下哪些能力?( 知识学习)": int("知识学习" in choices),
            "1 ( 创造力)": int("创造力" in choices),
            # ... 补充其他多选题
        }
        
        # 生成模拟开放题
        record["(1)20.您目前最大的育儿困惑是什么?___"] = choices([
            "无", "如何平衡学习与兴趣", "孩子沉迷手机", "教育方法选择"], 
            weights=[0.3,0.3,0.2,0.2])[0]

        data.append(record)
    
    # 创建完全匹配示例的DataFrame
    columns = [
        '序号', '提交答卷时间', '所用时间', '来源', '来源详情', '来自IP',
        '1.您是孩子的:', '2.您的年龄:', '3.您的最高学历:', '4.您的职业类型:',
        # ... 完全按照示例文件列顺序排列
    ]
    df = pd.DataFrame(data)[columns]
    return df

# 网页界面
st.title("专业级问卷数据生成器")
num = st.number_input("生成记录数", min_value=1, value=26)

if st.button("生成数据"):
    df = generate_data(num)
    
    # 导出Excel
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        # 设置列宽
        worksheet = writer.sheets['Sheet1']
        worksheet.column_dimensions['A'].width = 8  # 序号列宽
        # ... 其他列宽设置
    
    st.download_button(
        label="下载Excel文件",
        data=excel_buffer.getvalue(),
        file_name='问卷数据.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    st.dataframe(df)
