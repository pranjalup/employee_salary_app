import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# 🎯 PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Employee Salary & Job Role Dashboard",
    layout="wide"
)

# -----------------------------
# 🧾 EMPLOYEE DATA
# -----------------------------
data = pd.DataFrame({
    "EMPLOYEE_ID": [101, 102, 103, 104, 105, 106],
    "NAME": ["RAJ", "STRIVERS", "KSHITHIZ", "RISHI", "UTKARSH", "ALEKH"],
    "JOB_ROLE": [
        "Data Analyst", "Data Scientist", "Web Developer",
        "HR Manager", "Software Engineer", "ML Engineer"
    ],
    "SALARY": [40000, 90000, 55000, 70000, 65000, 95000],
    "EXPERIENCE": [1, 3, 2, 5, 4, 3]
})

# -----------------------------
# 🏠 SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filter Options")

roles = st.sidebar.multiselect("Select Job Role(s):", data["JOB_ROLE"].unique())
if roles:
    data = data[data["JOB_ROLE"].isin(roles)]

min_exp, max_exp = st.sidebar.slider("Filter by Experience (Years):", 0, 10, (0, 10))
data = data[(data["EXPERIENCE"] >= min_exp) & (data["EXPERIENCE"] <= max_exp)]

# -----------------------------
# 📊 DASHBOARD METRICS
# -----------------------------
st.title("💼 Employee Salary & Job Role Dashboard")

col1, col2, col3 = st.columns(3)

avg_salary = data["SALARY"].mean()
max_salary = data["SALARY"].max()
min_salary = data["SALARY"].min()

col1.metric("Average Salary", f"₹{avg_salary:,.0f}")
col2.metric("Highest Salary", f"₹{max_salary:,.0f}")
col3.metric("Lowest Salary", f"₹{min_salary:,.0f}")

# -----------------------------
# 📋 DISPLAY DATA
# -----------------------------
st.subheader("📋 Employee Data")
st.dataframe(data, use_container_width=True)

# -----------------------------
# 📈 GROUP ANALYSIS
# -----------------------------
st.subheader("📊 Average Salary by Job Role")
role_avg_salary = data.groupby("JOB_ROLE")["SALARY"].mean().sort_values(ascending=False)
st.bar_chart(role_avg_salary)

# -----------------------------
# 🧠 CORRELATION ANALYSIS
# -----------------------------
correlation = data["SALARY"].corr(data["EXPERIENCE"])
st.subheader("📈 Correlation between Salary and Experience")
st.write(f"**Correlation Value:** {correlation:.2f}")

# -----------------------------
# 🏅 TOP EMPLOYEE
# -----------------------------
highest_salary = data[data["SALARY"] == data["SALARY"].max()]
st.subheader("🏅 Employee with Highest Salary")
st.table(highest_salary)
