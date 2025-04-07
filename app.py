import csv
import random
from random import choices, sample
from itertools import chain

# ==================== 基础配置 ====================
SAMPLE_SIZE = 120  # 总样本量
OUTPUT_FILE = "questionnaire_data.csv"  # 输出文件名

# ==================== 完整数据生成规则配置 ====================
CONFIG = {
    # ==================== 基本信息部分 ====================
    "Q1_家长身份": {
        "options": ["母亲", "父亲", "祖父母/外祖父母", "其他亲属"],
        "weights": [0.68, 0.25, 0.05, 0.02],
        "type": "single"
    },
    "Q2_年龄": {
        "options": ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
        "weights": [0.03, 0.12, 0.40, 0.30, 0.15],
        "type": "single"
    },
    "Q3_学历": {
        "options": ["初中及以下", "高中/中专", "大专", "本科", "硕士及以上"],
        "weights": [0.05, 0.20, 0.25, 0.45, 0.05],
        "type": "single"
    },
    "Q4_职业类型": {
        "options": ["公务员/事业单位", "教师", "企业职员", "自由职业", "全职家长", "个体户", "其他"],
        "weights": [0.10, 0.15, 0.35, 0.10, 0.25, 0.05, 0.00],
        "type": "single"
    },
    "Q5_家庭月收入": {
        "options": ["3000元及以下", "3000-5000元", "5000-8000元", "8000-12000元", "12000元及以上"],
        "weights": [0.20, 0.10, 0.40, 0.20, 0.10],
        "type": "single"
    },
    "Q6_家庭结构": {
        "options": ["核心家庭", "三代同堂", "单亲家庭", "其他"],
        "weights": [0.65, 0.25, 0.08, 0.02],
        "type": "single"
    },
    "Q7_孩子年龄": {
        "options": ["0-2周岁", "2-3周岁", "3-4周岁", "4-5周岁", "5-6周岁", "6周岁及以上"],
        "weights": [0.00, 0.00, 0.40, 0.30, 0.20, 0.10],  # 根据修正后分布
        "max_choices": 3,
        "type": "multi"
    },
    
    # ==================== 教育观念部分 ====================
    "Q8_能力培养偏好": {
        "options": ["知识学习", "创造力", "规则意识", "情绪管理", "运动能力", "艺术兴趣", "其他"],
        "weights": [0.35, 0.52, 0.48, 0.45, 0.28, 0.15, 0.04],
        "max_choices": 3,
        "type": "multi"
    },
    "Q9_长期发展期待": {
        "options": ["考上名牌大学", "有稳定的高收入工作", "具备良好的道德品质", 
                   "身心健康，快乐成长", "拥有独立自主的能力", "发展广泛的兴趣爱好或特长", "其他"],
        "weights": [0.30, 0.25, 0.65, 0.78, 0.58, 0.20, 0.05],
        "type": "multi"
    },
    "Q10_游戏重要性": {
        "options": ["1", "2", "3", "4", "5"],
        "weights": [0.02, 0.04, 0.14, 0.35, 0.45],
        "type": "score"
    },
    # ...（其他题目配置详见完整代码）
}

# ==================== 核心数据生成函数 ====================
def generate_question(q_config):
    if q_config["type"] == "single":
        return choices(q_config["options"], weights=q_config["weights"])[0]
    
    elif q_config["type"] == "multi":
        selected = []
        remaining_weights = q_config["weights"].copy()
        for _ in range(q_config.get("max_choices", 3)):
            if sum(remaining_weights) == 0:
                break
            idx = choices(range(len(remaining_weights)), weights=remaining_weights)[0]
            selected.append(q_config["options"][idx])
            remaining_weights[idx] = 0  # 避免重复选择
        return "|".join(selected)
    
    elif q_config["type"] == "score":
        return choices(q_config["options"], weights=q_config["weights"])[0]
    
    else:
        return ""

# ==================== 生成完整数据集 ====================
def generate_dataset():
    headers = list(CONFIG.keys())
    data = []
    
    for _ in range(SAMPLE_SIZE):
        row = {}
        for q_id, q_config in CONFIG.items():
            row[q_id] = generate_question(q_config)
        data.append(row)
    
    # 写入CSV文件
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"成功生成{SAMPLE_SIZE}条数据，已保存至：{OUTPUT_FILE}")

# ==================== 执行生成 ====================
if __name__ == "__main__":
    generate_dataset()
