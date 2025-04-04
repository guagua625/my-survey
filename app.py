import pandas as pd
import numpy as np
from random import choices, sample, randint
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
        record["来自IP"] = fake.ipv4() + "(广东-潮州)"  # 固定为潮州IP
        
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
    """根据权重生成多选选项"""
    total = sum(weights)
    if total == 0:
        return []
    normalized = [w / total for w in weights]
    selected = []
    for _ in range(max_choices):
        selected_opt = choices(options, weights=normalized, k=1)[0]
        selected.append(selected_opt)
    return list(set(selected))  # 去重确保每个选项只出现一次

def generate_parenting_methods(record):
    """生成教育方法部分"""
    # 长期发展期待（多选）
    expectations = weighted_choice(
        ["考上名牌大学", "有稳定的高收入工作", "具备良好的道德品质", 
         "身心健康，快乐成长", "拥有独立自主的能力", "发展广泛的兴趣爱好或特长"],
        [30, 25, 65, 78, 58, 20],
        max_choices=3
    )
    for opt in ["考上名牌大学", "有稳定的高收入工作", "具备良好的道德品质", 
                "身心健康，快乐成长", "拥有独立自主的能力", "发展广泛的兴趣爱好或特长"]:
        record[f"2 ({opt})"] = 1 if opt in expectations else 0

    # 儿童观评分
    record["3.游戏是幼儿学习的主要方式，应与知识学习同等重要。"] = randint(1,5)
    record["4.孩子天生具有好奇心，家长应鼓励其自由探索。"] = randint(1,5)
    record["5. 在学前期提前学习小学知识会抑制孩子的创造力。"] = randint(1,5)

def generate_anxiety_data(record):
    """生成焦虑相关数据"""
    # 教育焦虑程度
    record["13.您是否经常因孩子的教育问题感到焦虑?"] = randint(1,5)
    
    # 焦虑来源（多选）
    anxiety_sources = weighted_choice(
        ["孩子表现不如同龄人", "兴趣班选择困难", "家庭教育时间不足", "幼小衔接压力"],
        [12, 35, 48, 62],
        max_choices=3
    )
    for opt in ["孩子表现不如同龄人", "兴趣班选择困难", "家庭教育时间不足", "幼小衔接压力"]:
        record[f"14 ({opt})"] = 1 if opt in anxiety_sources else 0

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
