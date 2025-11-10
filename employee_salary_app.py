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
# 🏢 EXTRA DATAFRAME FOR MERGE
# -----------------------------
# This could come from another source (e.g., CSV, DB)
department_data = pd.DataFrame({
    "EMPLOYEE_ID": [101, 102, 103, 104, 105, 106],
    "DEPARTMENT": ["Analytics", "Research", "Development", "HR", "Engineering", "AI Lab"]
})

# Merge employee data with department info
merged_data = pd.merge(data, department_data, on="EMPLOYEE_ID", how="left")

# -----------------------------
# 🏠 SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filter Options")

roles = st.sidebar.multiselect("Select Job Role(s):", merged_data["JOB_ROLE"].unique())
filtered_data = merged_data.copy()
if roles:
    filtered_data = filtered_data[filtered_data["JOB_ROLE"].isin(roles)]

min_exp, max_exp = st.sidebar.slider("Filter by Experience (Years):", 0, 10, (0, 10))
filtered_data = filtered_data[
    (filtered_data["EXPERIENCE"] >= min_exp) & (filtered_data["EXPERIENCE"] <= max_exp)
]

# -----------------------------
# ➕ ADD EMPLOYEE SECTION
# -----------------------------
st.sidebar.header("➕ Add New Employee")

with st.sidebar.form("add_employee_form", clear_on_submit=True):
    emp_id = st.number_input("Employee ID", min_value=1, step=1)
    name = st.text_input("Name")
    job_role = st.text_input("Job Role")
    salary = st.number_input("Salary (₹)", min_value=0, step=1000)
    experience = st.number_input("Experience (Years)", min_value=0, step=1)
    dept = st.text_input("Department Name")
    add_button = st.form_submit_button("Add Employee")

    if add_button:
        if name and job_role:
            if emp_id in st.session_state["data"]["EMPLOYEE_ID"].values:
                st.warning("⚠️ Employee ID already exists! Use update section to modify.")
            else:
                new_entry = pd.DataFrame({
                    "EMPLOYEE_ID": [emp_id],
                    "NAME": [name.upper()],
                    "JOB_ROLE": [job_role.title()],
                    "SALARY": [salary],
                    "EXPERIENCE": [experience]
                })
                new_dept = pd.DataFrame({
                    "EMPLOYEE_ID": [emp_id],
                    "DEPARTMENT": [dept if dept else "Not Assigned"]
                })

                # Update both datasets and merge
                st.session_state["data"] = pd.concat([st.session_state["data"], new_entry], ignore_index=True)
                department_data = pd.concat([department_data, new_dept], ignore_index=True)

                st.success(f"✅ Employee '{name}' added successfully!")

                # Update merged view
                merged_data = pd.merge(st.session_state["data"], department_data, on="EMPLOYEE_ID", how="left")
        else:
            st.warning("⚠️ Please fill all required fields (Name and Job Role).")

# -----------------------------
# ✏️ UPDATE EMPLOYEE SECTION
# -----------------------------
st.sidebar.header("✏️ Update Existing Employee")

with st.sidebar.form("update_employee_form", clear_on_submit=True):
    emp_to_update = st.selectbox(
        "Select Employee ID to Update:",
        st.session_state["data"]["EMPLOYEE_ID"]
    )

    selected_emp = st.session_state["data"].loc[
        st.session_state["data"]["EMPLOYEE_ID"] == emp_to_update
    ].iloc[0]

    new_name = st.text_input("Updated Name", value=selected_emp["NAME"])
    new_role = st.text_input("Updated Job Role", value=selected_emp["JOB_ROLE"])
    new_salary = st.number_input(
        "Updated Salary (₹)", min_value=0, step=1000, value=int(selected_emp["SALARY"])
    )
    new_exp = st.number_input(
        "Updated Experience (Years)", min_value=0, step=1, value=int(selected_emp["EXPERIENCE"])
    )
    update_button = st.form_submit_button("Update Employee")

    if update_button:
        st.session_state["data"].loc[
            st.session_state["data"]["EMPLOYEE_ID"] == emp_to_update,
            ["NAME", "JOB_ROLE", "SALARY", "EXPERIENCE"]
        ] = [new_name.upper(), new_role.title(), new_salary, new_exp]
        st.success(f"✅ Employee ID {emp_to_update} updated successfully!")

# -----------------------------
# 📊 DASHBOARD METRICS
# -----------------------------
st.title("💼 Employee Salary & Job Role Dashboard")

col1, col2, col3 = st.columns(3)
avg_salary = filtered_data["SALARY"].mean()
max_salary = filtered_data["SALARY"].max()
min_salary = filtered_data["SALARY"].min()

col1.metric("Average Salary", f"₹{avg_salary:,.0f}" if not np.isnan(avg_salary) else "N/A")
col2.metric("Highest Salary", f"₹{max_salary:,.0f}" if not np.isnan(max_salary) else "N/A")
col3.metric("Lowest Salary", f"₹{min_salary:,.0f}" if not np.isnan(min_salary) else "N/A")

# -----------------------------
# 📋 DISPLAY MERGED DATA
# -----------------------------
st.subheader("📋 Employee Data (with Department)")
st.dataframe(filtered_data, use_container_width=True)

# -----------------------------
# 📈 ANALYSIS & VISUALS
# -----------------------------
if not filtered_data.empty:
    st.subheader("📊 Average Salary by Job Role")
    role_avg_salary = (
        filtered_data.groupby("JOB_ROLE")["SALARY"]
        .mean()
        .sort_values(ascending=False)
    )
    st.bar_chart(role_avg_salary)

if len(filtered_data) > 1:
    correlation = filtered_data["SALARY"].corr(filtered_data["EXPERIENCE"])
    st.subheader("📈 Correlation between Salary and Experience")
    st.write(f"**Correlation Value:** {correlation:.2f}")

# -----------------------------
# 🏅 TOP EMPLOYEE
# -----------------------------
if not filtered_data.empty:
    highest_salary = filtered_data[filtered_data["SALARY"] == filtered_data["SALARY"].max()]
    st.subheader("🏅 Employee with Highest Salary")
    st.table(highest_salary)

# -----------------------------
# 💾 DOWNLOAD DATA
# -----------------------------
st.subheader("⬇️ Download Filtered Data")
csv = filtered_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name="employee_data.csv",
    mime="text/csv"
)
