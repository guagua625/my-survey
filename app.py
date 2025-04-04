import pandas as pd
import numpy as np
from random import choices, sample
from faker import Faker
from openpyxl.utils import get_column_letter

# 初始化工具
fake = Faker('zh_CN')

# ================== 数据分布配置 ==================
question_config = {
    # 基本信息
    "1.您是孩子的:": ["母亲", "父亲", "祖父母/外祖父母", "其他亲属"],
    "2.您的年龄:": ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
    "3.您的最高学历:": ["初中及以下", "高中/中专", "大专", "本科", "硕士及以上"],
    "4.您的职业类型:": ["公务员/事业单位", "教师", "企业职员", "自由职业", "全职家长", "个体户", "其他"],
    "5.家庭月收入（包括所有成员）:": ["3000元及以下", "3000-5000元", "5000-8000元", "8000-12000元", "12000元及以上"],
    "6.家庭结构:": ["核心家庭", "三代同堂", "单亲家庭", "其他"]
}

distributions = {
    # 基本信息分布（权重百分比）
    "1.您是孩子的:": [68, 25, 5, 2],
    "2.您的年龄:": [3, 7, 40, 30, 20],
    "3.您的最高学历:": [5, 20, 25, 45, 5],
    "4.您的职业类型:": [10, 15, 35, 10, 25, 5, 15],
    "5.家庭月收入（包括所有成员）:": [20, 20, 40, 20, 10],
    "6.家庭结构:": [65, 25, 8, 2]
}

# ================== 生成函数 ==================
def generate_survey_data(num_records):
    data = []
    
    for _ in range(num_records):
        record = {}
        
        # 生成基础信息
        record["序号"] = len(data) + 1
        record["提交答卷时间"] = fake.date_time_between(start_date="-30d").strftime("%Y/%m/%d %H:%M:%S")
        record["所用时间"] = randint(60, 600)
        record["来源"] = choices(["微信", "手机提交"], weights=[80, 20])[0]
        record["来源详情"] = "N/A"
        record["来自IP"] = fake.ipv4() + f"({fake.province()}-{fake.city()})"
        
        # 生成问卷答案
        generate_basic_info(record)
        generate_education_views(record)
        generate_parenting_methods(record)
        generate_anxiety_data(record)
        
        data.append(record)
    
    df = pd.DataFrame(data)
    return format_excel(df)

def generate_basic_info(record):
    """生成基础信息部分"""
    for q in question_config:
        options = question_config[q]
        weights = distributions.get(q, [1]*len(options))
        record[q] = choices(options, weights=weights)[0]

def generate_education_views(record):
    """生成教育观念部分"""
    # 能力培养偏好（多选）
    abilities = weighted_choice(
        ["知识学习", "创造力", "规则意识", "情绪管理", "运动能力", "艺术兴趣", "其他"],
        [35, 52, 48, 45, 28, 15, 4],
        max_choices=3
    )
    for opt in ["知识学习", "创造力", "规则意识", "情绪管理", "运动能力", "艺术兴趣", "其他"]:
        record[f"1 ({opt})"] = 1 if opt in abilities else 0

def weighted_choice(options, weights, max_choices=3):
    return sample([opt for opt in options for _ in range(weights[options.index(opt)])[:max_choices]

def format_excel(df):
    """格式化Excel输出"""
    writer = pd.ExcelWriter("survey_data.xlsx", engine='openpyxl')
    df.to_excel(writer, index=False)
    
    # 设置自适应列宽
    worksheet = writer.sheets['Sheet1']
    for col in df.columns:
        max_length = max(df[col].astype(str).map(len).max(), len(col))
        worksheet.column_dimensions[get_column_letter(df.columns.get_loc(col)+1)].width = max_length + 2
    
    writer.save()
    return df

# ================== 执行生成 ==================
if __name__ == "__main__":
    df = generate_survey_data(312)
    print("问卷数据生成完成，保存至 survey_data.xlsx")
