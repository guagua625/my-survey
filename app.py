import pandas as pd
import numpy as np
from random import choices, sample, randint

# ======================
# 数据生成配置
# ======================
N = 120  # 总样本量

# 1. 基础信息分布配置
base_dist = {
    "家长身份": ["母亲", "父亲", "祖父母/外祖父母", "其他亲属"],
    "身份分布": [0.68, 0.25, 0.05, 0.02],
    
    "年龄分组": ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
    "年龄分布": [0.03, 0.12, 0.40, 0.30, 0.15],
    
    "家庭月收入": ["3000元及以下", "3000-5000元", "5000-8000元", "8000-12000元", "12000元及以上"],
    "收入分布": [0.20, 0.10, 0.40, 0.20, 0.10]
}

# 2. 教育观念配置
edu_config = {
    # 问题8：能力培养偏好（多选，最多3项）
    "能力培养": {
        "options": ["知识学习", "创造力", "规则意识", "情绪管理", "运动能力", "艺术兴趣", "其他"],
        "weights": [0.35, 0.52, 0.48, 0.45, 0.28, 0.15, 0.04],
        "max_choices": 3
    },
    
    # 问题10-12：评分题分布（1-5分）
    "游戏重要性评分": [0.02, 0.04, 0.14, 0.35, 0.45],  # 完全不同意(1分)到完全同意(5分)
    "提前学习反向评分": [0.15, 0.25, 0.30, 0.20, 0.10]  # 需要反向计分
}

# ======================
# 核心数据生成函数
# ======================
def generate_respondent():
    """生成单个受访者数据"""
    record = {}
    
    # 1. 生成基础信息
    record["家长身份"] = choices(base_dist["家长身份"], weights=base_dist["身份分布"])[0]
    record["年龄"] = choices(base_dist["年龄分组"], weights=base_dist["年龄分布"])[0]
    record["家庭月收入"] = choices(base_dist["家庭月收入"], weights=base_dist["收入分布"])[0]
    
    # 2. 生成教育观念数据
    # 问题8：多选处理
    selected = np.random.choice(
        edu_config["能力培养"]["options"],
        size=randint(1, edu_config["能力培养"]["max_choices"]),
        p=np.array(edu_config["能力培养"]["weights"])/sum(edu_config["能力培养"]["weights"]),
        replace=False
    )
    for opt in edu_config["能力培养"]["options"]:
        record[f"Q8_{opt}"] = 1 if opt in selected else 0
    
    # 问题10：正向评分
    record["Q10_评分"] = choices([1,2,3,4,5], weights=edu_config["游戏重要性评分"])[0]
    
    # 问题12：反向计分处理
    raw_score = choices([1,2,3,4,5], weights=edu_config["提前学习反向评分"])[0]
    record["Q12_评分"] = 6 - raw_score  # 反向计分转换
    
    return record

# ======================
# 批量生成数据
# ======================
data = [generate_respondent() for _ in range(N)]
df = pd.DataFrame(data)

# ======================
# 数据验证模块
# ======================
def validate_data(df):
    """数据质量验证"""
    print("=== 数据验证报告 ===")
    
    # 1. 基础分布验证
    print("\n1. 家长身份分布:")
    print(df["家长身份"].value_counts(normalize=True).round(2))
    
    print("\n2. 年龄分布:")
    print(df["年龄"].value_counts(normalize=True).round(2))
    
    # 2. 多选题验证
    q8_cols = [c for c in df.columns if c.startswith("Q8_")]
    print("\n3. 能力培养多选比例:")
    print(df[q8_cols].mean().sort_values(ascending=False).round(2))
    
    # 3. 评分题验证
    print("\n4. 游戏重要性评分分布:")
    print(df["Q10_评分"].value_counts(normalize=True).sort_index().round(2))
    
    print("\n5. 提前学习反向评分验证:")
    print("原始分布:", df["Q12_评分"].value_counts(normalize=True).sort_index().round(2))
    print("理论反向分布:", dict(zip([5,4,3,2,1], edu_config["提前学习反向评分"])))

validate_data(df)

# ======================
# 数据导出
# ======================
df.to_csv("questionnaire_data.csv", index=False, encoding="utf_8_sig")
print("\n=== 数据已生成并保存为 questionnaire_data.csv ===")
