import pandas as pd
import numpy as np
from collections import defaultdict

# 初始化随机种子保证可重复性
np.random.seed(2023)

# 定义基础参数
n = 120  # 样本量

# ========== 1. 定义数据结构与生成规则 ==========
data = defaultdict(list)

# ---------------------------
# 一、基本信息（1-7题）
# ---------------------------
# 问题1：身份
roles = ["母亲"]*82 + ["父亲"]*30 + ["祖父母/外祖父母"]*6 + ["其他亲属"]*2
np.random.shuffle(roles)
data["身份"] = roles

# 问题2：年龄（与身份逻辑关联）
age_rules = {
    "母亲": np.random.choice(
        ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
        p=[0.02, 0.12, 0.45, 0.35, 0.06]
    ),
    "父亲": np.random.choice(
        ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
        p=[0.01, 0.10, 0.35, 0.40, 0.14]
    ),
    "祖父母/外祖父母": ["41岁及以上"]*6,
    "其他亲属": np.random.choice(["31-35岁", "36-40岁"], size=2)
}
data["年龄"] = [age_rules[role]() if callable(age_rules[role]) else age_rules[role].pop() 
            for role in data["身份"]]

# 问题3：学历（与年龄逻辑关联）
def generate_education(age):
    if "41" in age:
        return np.random.choice(["初中及以下", "高中/中专", "大专"], p=[0.4, 0.4, 0.2])
    elif "36-40" in age:
        return np.random.choice(["高中/中专", "大专", "本科"], p=[0.3, 0.4, 0.3])
    else:
        return np.random.choice(
            ["初中及以下", "高中/中专", "大专", "本科", "硕士及以上"],
            p=[0.05, 0.20, 0.25, 0.45, 0.05]
        )
data["学历"] = [generate_education(age) for age in data["年龄"]]

# 问题4：职业类型（与身份关联）
def generate_occupation(role):
    if role == "母亲":
        return np.random.choice(
            ["企业职员", "全职家长", "教师", "自由职业"],
            p=[0.35, 0.40, 0.15, 0.10]
        )
    elif role == "父亲":
        return np.random.choice(
            ["企业职员", "公务员/事业单位", "个体户", "创业者"],
            p=[0.45, 0.30, 0.20, 0.05]
        )
    else:
        return "其他"
data["职业类型"] = [generate_occupation(role) for role in data["身份"]]

# 问题5：家庭月收入（与职业关联）
income_map = {
    "企业职员": ["5000-8000元", "8000-12000元"],
    "全职家长": ["3000-5000元", "5000-8000元"],
    "公务员/事业单位": ["8000-12000元", "12000元及以上"],
    "个体户": ["5000-8000元", "12000元及以上"],
    "创业者": ["12000元及以上"],
    "其他": ["3000元及以下", "3000-5000元"]
}
data["家庭月收入"] = [
    np.random.choice(income_map[occ]) if occ in income_map 
    else np.random.choice(["3000元及以下", "3000-5000元"])
    for occ in data["职业类型"]
]

# 问题6：家庭结构（与身份关联）
def generate_family(role):
    if role in ["祖父母/外祖父母"]:
        return "三代同堂"
    else:
        return np.random.choice(
            ["核心家庭", "三代同堂", "单亲家庭"],
            p=[0.70, 0.25, 0.05]
        )
data["家庭结构"] = [generate_family(role) for role in data["身份"]]

# 问题7：孩子年龄（与家庭结构关联）
def generate_child_age(family):
    if family == "三代同堂":
        return np.random.choice(["3-4周岁", "4-5周岁"], p=[0.6, 0.4])
    else:
        return np.random.choice(
            ["0-2周岁", "3-4周岁", "4-5周岁", "5-6周岁", "6周岁及以上"],
            p=[0.05, 0.40, 0.30, 0.20, 0.05]
        )
data["孩子年龄"] = [generate_child_age(fam) for fam in data["家庭结构"]]

# ---------------------------
# 二、家长教育观念现状（8-21题）
# ---------------------------
# 问题8：能力培养（多选，最多3项）
def generate_q8(education):
    base_options = ["创造力", "规则意识", "情绪管理", "知识学习", "运动能力"]
    weights = {
        "本科":        [0.70, 0.30, 0.45, 0.20, 0.15],
        "硕士及以上":   [0.75, 0.25, 0.40, 0.15, 0.10],
        "大专":        [0.50, 0.50, 0.40, 0.30, 0.20],
        "高中/中专":   [0.30, 0.60, 0.35, 0.40, 0.25],
        "初中及以下":   [0.20, 0.65, 0.30, 0.50, 0.20]
    }
    selected = np.random.choice(
        base_options, 
        size=np.random.randint(1,4), 
        p=weights.get(education, [0.3]*5),
        replace=False
    )
    return ";".join(selected)
data["能力培养"] = [generate_q8(edu) for edu in data["学历"]]

# 问题9：长期期待（多选）
# （生成逻辑类似，需根据教育程度调整权重）

# ...（其余问题的生成逻辑类似，需根据论文统计结果设置权重）

# ========== 2. 创建DataFrame ==========
df = pd.DataFrame(data)

# ========== 3. 验证数据一致性 ==========
def validate_column(col, expected):
    actual = df[col].value_counts(normalize=True).to_dict()
    for key in expected:
        assert abs(actual.get(key,0) - expected[key]) < 0.02, f"{col} 验证失败"

validate_column("身份", {"母亲":0.68, "父亲":0.25, "祖父母/外祖父母":0.05, "其他亲属":0.02})
validate_column("学历", {"本科":0.45, "大专":0.25, "高中/中专":0.20, "初中及以下":0.05, "硕士及以上":0.05})

# ========== 4. 导出Excel ==========
df.to_excel("simulated_survey_data.xlsx", index=False)

print("数据生成完成！文件保存为 simulated_survey_data.xlsx")
