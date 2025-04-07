# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from random import choices, sample, randint

# ================== 数据配置 ==================
QUESTION_CONFIG = {
    # 基本信息
    "Q1_身份": {
        "options": ["母亲", "父亲", "祖父母/外祖父母", "其他亲属"],
        "weights": [68, 25, 5, 2]
    },
    "Q2_年龄": {
        "options": ["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"],
        "weights": [3, 12, 40, 30, 15]
    },
    # 其他问题配置...
}

# ================== 核心函数 ==================
def generate_single_choice(options, weights, n):
    """生成单选题数据"""
    return [choices(options, weights=weights, k=1)[0] for _ in range(n)]

def generate_multi_choice(options, weights, n, max_choices=3):
    """生成多选题数据"""
    data = []
    for _ in range(n):
        selected = []
        valid_options = list(enumerate(options))
        valid_weights = weights.copy()
        
        for _ in range(randint(1, max_choices)):
            if sum(valid_weights) == 0:
                break
            idx = choices(range(len(valid_options)), 
                        weights=valid_weights)[0]
            selected.append(valid_options[idx][1])
            # 移除已选选项
            valid_weights.pop(idx)
            valid_options.pop(idx)
        data.append("|".join(selected))
    return data

def generate_ratings(distribution, n):
    """生成评分题数据"""
    return choices([1,2,3,4,5], weights=distribution, k=n)

# ================== 网页界面 ==================
def main():
    st.set_page_config(
        page_title="家长教育观念数据生成系统",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 侧边栏控制
    with st.sidebar:
        st.header("⚙️ 控制面板")
        num_records = st.number_input("生成数据量", 
                                    min_value=1, 
                                    max_value=1000,
                                    value=120)
        generate_btn = st.button("🚀 生成数据", type="primary")
    
    # 主界面
    st.title("📊 家长教育观念问卷数据生成系统")
    st.markdown("根据潮州市X幼儿园研究数据分布自动生成问卷星格式数据")
    
    if generate_btn:
        # 生成数据
        df = pd.DataFrame()
        
        # 示例：生成家长身份数据
        df["家长身份"] = generate_single_choice(
            options=QUESTION_CONFIG["Q1_身份"]["options"],
            weights=QUESTION_CONFIG["Q1_身份"]["weights"],
            n=num_records
        )
        
        # 生成其他字段...
        
        # 显示数据
        st.success(f"成功生成 {num_records} 条数据！")
        st.dataframe(df.head())
        
        # 下载按钮
        csv = df.to_csv(index=False, encoding="utf_8_sig").encode()
        st.download_button(
            label="⬇️ 下载CSV文件",
            data=csv,
            file_name="questionnaire_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
