import csv
import random
from random import choices, sample
from itertools import chain

# ==================== 基础配置 ====================
SAMPLE_SIZE = 120  # 总样本量
OUTPUT_FILE = "questionnaire_data.csv"  # 输出文件名

# ==================== 数据生成规则配置 ====================
CONFIG = {
    # ========== 基本信息部分 ==========
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
    # ...其他基本信息题类似配置
    
    # ========== 教育观念部分 ==========
    "Q8_能力培养偏好": {
        "options": ["创造力", "规则意识", "情绪管理", "知识学习", "运动能力", "艺术兴趣", "其他"],
        "weights": [0.52, 0.48, 0.45, 0.35, 0.28, 0.15, 0.04],
        "max_choices": 3,  # 最多选3项
        "type": "multi"
    },
    "Q10_游戏重要性": {
        "options": ["1", "2", "3", "4", "5"],
        "weights": [0.02, 0.04, 0.14, 0.35, 0.45],
        "type": "score"
    },
    # ...其他题目类似配置
    
    # ========== 影响因素部分 ==========
    "Q25_自媒体使用时间": {
        "options": ["<1小时", "1-3小时", "3-5小时", ">5小时"],
        "weights": [0.30, 0.40, 0.20, 0.10],
        "type": "single"
    }
}

# ==================== 核心数据生成函数 ====================
def generate_row():
    row = {}
    
    # 生成基本信息
    row["Q1_家长身份"] = choices(
        CONFIG["Q1_家长身份"]["options"],
        weights=CONFIG["Q1_家长身份"]["weights"]
    )[0]
    
    # 生成多选题（示例：Q8能力培养偏好）
    selected = []
    for _ in range(CONFIG["Q8_能力培养偏好"]["max_choices"]):
        option = choices(
            CONFIG["Q8_能力培养偏好"]["options"],
            weights=CONFIG["Q8_能力培养偏好"]["weights"]
        )[0]
        if option not in selected:
            selected.append(option)
    row["Q8_能力培养偏好"] = "|".join(selected)
    
    # 生成评分题（示例：Q10游戏重要性）
    row["Q10_游戏重要性"] = choices(
        CONFIG["Q10_游戏重要性"]["options"],
        weights=CONFIG["Q10_游戏重要性"]["weights"]
    )[0]
    
    # 生成其他题目数据...
    
    return row

# ==================== 生成完整数据集 ====================
def generate_dataset():
    headers = list(CONFIG.keys())
    data = [generate_row() for _ in range(SAMPLE_SIZE)]
    
    # 写入CSV文件
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"成功生成{SAMPLE_SIZE}条数据，已保存至：{OUTPUT_FILE}")

# ==================== 执行生成 ====================
if __name__ == "__main__":
    generate_dataset()
