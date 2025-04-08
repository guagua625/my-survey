import streamlit as st
import pandas as pd
import numpy as np

# 设置页面标题和布局
st.set_page_config(page_title="家长教育问卷模拟数据生成器", layout="wide")

# --------------------------
# 数据生成函数（完整版）
# --------------------------
def generate_data(sample_size=120):
    np.random.seed(42)
    parent_ids = [f"P{str(i+1).zfill(3)}" for i in range(sample_size)]
    
    # 1. 基本信息 (Q1-Q7)
    q1 = np.random.choice(["母亲"]*68 + ["父亲"]*25 + ["祖父母"]*5 + ["其他亲属"]*2, size=sample_size)
    q2 = np.random.choice(["25岁及以下", "26-30岁", "31-35岁", "36-40岁", "41岁及以上"], 
                         size=sample_size, p=[0.03, 0.15, 0.40, 0.30, 0.12])
    q3 = np.random.choice(["初中及以下", "高中/中专", "大专", "本科", "硕士及以上"], 
                         size=sample_size, p=[0.05, 0.20, 0.25, 0.45, 0.05])
    q4 = np.random.choice(["公务员/事业单位", "教师", "企业职员", "自由职业", "全职家长", "个体户", "创业者", "其他"], 
                         size=sample_size, p=[0.10, 0.15, 0.35, 0.075, 0.25, 0.10, 0.025, 0.025])
    q5 = np.random.choice(["3000元及以下", "3000-5000元", "5000-8000元", "8000-12000元", "12000元及以上"], 
                         size=sample_size, p=[0.20, 0.10, 0.40, 0.20, 0.10])
    q6 = np.random.choice(["核心家庭", "三代同堂", "单亲家庭", "其他"], 
                         size=sample_size, p=[0.65, 0.25, 0.08, 0.02])
    q7 = np.random.choice(["0-2周岁", "2-3周岁", "3-4周岁", "4-5周岁", "5-6周岁", "6周岁及以上"], 
                         size=sample_size, p=[0.05, 0.10, 0.40, 0.30, 0.10, 0.05])

    # 2. 教育目标观 (Q8-Q9)
    def generate_multi_choice(options, counts, max_select=3):
        selected = np.random.choice(list(options.keys()), 
                                   size=np.random.randint(1, max_select+1), 
                                   p=list(options.values()))
        return ", ".join(selected)
    
    q8_options = {"创造力":0.52, "规则意识":0.48, "情绪管理":0.45, "知识学习":0.35, "运动能力":0.28, "艺术兴趣":0.15}
    q8 = [generate_multi_choice(q8_options, 3) for _ in range(sample_size)]
    
    q9_options = {"身心健康":0.78, "道德品质":0.65, "独立能力":0.58, "名牌大学":0.30, "高收入工作":0.25}
    q9 = [generate_multi_choice(q9_options, 3) for _ in range(sample_size)]

    # 3. 儿童观 (Q10-Q12)
    q10 = np.random.choice([1,2,3,4,5], size=sample_size, p=[0.02,0.04,0.14,0.35,0.45])
    q11 = np.random.choice([1,2,3,4,5], size=sample_size, p=[0.01,0.03,0.10,0.30,0.56])
    q12 = np.random.choice([1,2,3,4,5], size=sample_size, p=[0.15,0.25,0.30,0.20,0.10])

    # ...（其他题目按相同逻辑补充完整）

    # 创建DataFrame
    df = pd.DataFrame({
        "家长编号": parent_ids,
        "Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6, "Q7": q7,
        "Q8": q8, "Q9": q9, "Q10": q10, "Q11": q11, "Q12": q12
        # 继续添加其他列...
    })
    return df

# --------------------------
# Streamlit 交互界面
# --------------------------
st.title("📊 幼儿家庭教育调查模拟数据生成器")

# 侧边栏控制
with st.sidebar:
    st.header("⚙️ 控制面板")
    sample_size = st.slider("样本数量", 50, 200, 120, 10)
    st.caption("提示：建议首次使用默认120条样本")

# 主界面操作
if st.button("🚀 生成数据", type="primary"):
    with st.spinner("正在生成数据，请稍候..."):
        df = generate_data(sample_size)
    
    # 显示数据
    st.success(f"成功生成 {sample_size} 条数据！")
    tab1, tab2 = st.tabs(["数据预览", "统计分析"])
    
    with tab1:
        st.dataframe(df.sample(10), use_container_width=True)  # 随机抽样10行
    
    with tab2:
        selected_col = st.selectbox("选择分析列", df.columns[1:])
        st.bar_chart(df[selected_col].value_counts())

    # 下载功能
    st.download_button(
        label="⬇️ 下载CSV文件",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="parent_survey_data.csv",
        mime="text/csv"
    )

# 添加帮助信息
with st.expander("❓ 使用帮助"):
    st.markdown("""
    ### 常见问题解答
    1. **数据生成失败怎么办？**
       - 检查Python版本是否为3.6+
       - 确保已安装依赖库：`pip install streamlit pandas numpy`
    2. **如何验证数据准确性？**
       - 在「统计分析」标签页查看各列的分布比例
       - 导出数据后用Excel筛选计数
    3. **能修改生成规则吗？**
       - 当前版本支持样本量调整，高级规则需修改代码
    """)
