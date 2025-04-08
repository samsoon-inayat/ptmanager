# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 13:22:05 2025

@author: inayas1
"""

import pandas as pd
import streamlit as st

# Load data
file_path = '/mnt/data/Tasks_Management.xlsx'
file_path = r'G:\My Drive\Tasks_Management.xlsx'
xls = pd.ExcelFile(file_path)

# Load sheets
tasks_df = pd.read_excel(xls, sheet_name='Tasks')
progress_df = pd.read_excel(xls, sheet_name='Progress')
categories_df = pd.read_excel(xls, sheet_name='Categories')

# Pull separate category lists
task_types_list = categories_df['Types of Tasks'].dropna().tolist()
priority_list = categories_df['Priority'].dropna().tolist()
status_list = categories_df['Status'].dropna().tolist()

# Generate new Task ID
def generate_new_task_id(tasks_df):
    if tasks_df.empty:
        return "T001"
    last_id = tasks_df['Task_ID'].iloc[-1]
    number = int(last_id[1:]) + 1
    return f"T{number:03d}"

# Streamlit App
st.title("Task and Progress Manager")

tab1, tab2 = st.tabs(["Add Task", "Add Progress"])

with tab1:
    st.header("Add New Task")
    task_name = st.text_input("Task Name")
    selected_task_types = st.multiselect("Select Task Types", task_types_list)
    priority = st.selectbox("Select Priority", priority_list)
    status = st.selectbox("Select Status", status_list)
    start_date = st.date_input("Start Date")
    due_date = st.date_input("Due Date")
    primary_owner = st.text_input("Primary Owner")
    collaborators = st.text_input("Collaborators")
    responsibility_breakdown = st.text_area("Responsibility Breakdown")
    description = st.text_area("Description")

    if st.button("Submit Task"):
        new_task_id = generate_new_task_id(tasks_df)
        task_type_fields = {task_type: "✅" if task_type in selected_task_types else "❌" for task_type in task_types_list}
        
        new_task = {
            "Task ID": new_task_id,
            "Task Name": task_name,
            **task_type_fields,
            "Priority": priority,
            "Status": status,
            "Start Date": start_date,
            "Due Date": due_date,
            "Primary Owner": primary_owner,
            "Collaborators": collaborators,
            "Responsibility Breakdown": responsibility_breakdown,
            "Description": description
        }
        tasks_df = pd.concat([tasks_df, pd.DataFrame([new_task])], ignore_index=True)
        st.success(f"Task {new_task_id} added successfully!")

with tab2:
    st.header("Add Progress")
    progress_task_id = st.selectbox("Select Task ID", tasks_df['Task_ID'])
    update_date = st.date_input("Update Date", key="progress_date")
    updated_by = st.text_input("Updated By")
    progress_summary = st.text_area("Progress Summary")
    next_steps = st.text_area("Next Steps")
    brainstorming = st.text_area("Brainstorming Ideas")
    challenges = st.text_area("Challenges Faced")
    completion_percentage = st.slider("Completion Percentage", 0, 100, 0)
    time_spent = st.number_input("Time Spent (hours)", min_value=0.0)

    if st.button("Submit Progress"):
        new_progress_id = f"P{len(progress_df) + 1:03d}"
        new_progress = {
            "Progress ID": new_progress_id,
            "Task ID": progress_task_id,
            "Update Date": update_date,
            "Updated By": updated_by,
            "Progress Summary": progress_summary,
            "Next Steps (Owner-Specific)": next_steps,
            "Brainstorming Ideas": brainstorming,
            "Challenges Faced": challenges,
            "Completion Percentage (%)": completion_percentage,
            "Time Spent (hrs)": time_spent
        }
        progress_df = pd.concat([progress_df, pd.DataFrame([new_progress])], ignore_index=True)
        st.success(f"Progress {new_progress_id} added successfully!")

# Save updated Excel
with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
    tasks_df.to_excel(writer, sheet_name='Tasks', index=False)
    progress_df.to_excel(writer, sheet_name='Progress', index=False)
    categories_df.to_excel(writer, sheet_name='Categories', index=False)
