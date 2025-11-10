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
# 🧾 INITIAL EMPLOYEE DATA
# -----------------------------
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame({
        "EMPLOYEE_ID": [101, 102, 103, 104, 105, 106],
        "NAME": ["RAJ", "STRIVERS", "KSHITHIZ", "RISHI", "UTKARSH", "ALEKH"],
        "JOB_ROLE": [
            "Data Analyst", "Data Scientist", "Web Developer",
            "HR Manager", "Software Engineer", "ML Engineer"
        ],
        "SALARY": [40000, 90000, 55000, 70000, 65000, 95000],
        "EXPERIENCE": [1, 3, 2, 5, 4, 3]
    })

data = st.session_state["data"]

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
# ➕ ADD EMPLOYEE FEATURE
# -----------------------------
st.sidebar.header("➕ Add New Employee")

with st.sidebar.form("add_employee_form", clear_on_submit=True):
    emp_id = st.number_input("Employee ID", min_value=1, step=1)
    name = st.text_input("Name")
    job_role = st.text_input("Job Role")
    salary = st.number_input("Salary (₹)", min_value=0, step=1000)
    experience = st.number_input("Experience (Years)", min_value=0, step=1)

    submitted = st.form_submit_button("Add Employee")

    if submitted:
        if name and job_role:
            new_entry = pd.DataFrame({
                "EMPLOYEE_ID": [emp_id],
                "NAME": [name.upper()],
                "JOB_ROLE": [job_role.title()],
                "SALARY": [salary],
                "EXPERIENCE": [experience]
            })
            st.session_state["data"] = pd.concat([st.session_state["data"], new_entry], ignore_index=True)
            st.success(f"✅ Employee '{name}' added successfully!")
        else:
            st.warning("⚠️ Please fill all required fields (Name and Job Role).")

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

# -----------------------------
# 💾 DOWNLOAD DATA
# -----------------------------
st.subheader("⬇️ Download Filtered Data")
csv = data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name="employee_data.csv",
    mime="text/csv"
)
