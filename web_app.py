import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.title('Estimate Data Scientist Salary in US')

df = pd.read_csv('DS_salary_cleaned.csv')
model = joblib.load('model.pkl')

# function that convert categorical variable into one hot encoding vector
def list2vec(target_list,target_variable):
    target_list = np.sort(target_list)
    return np.equal(target_variable,target_list).astype(int)
    

st.subheader('Company Features:')

sector = st.selectbox('Sector', options = df['Sector'].unique())
sector_vec = list2vec(df['Sector'].unique(),sector)

ownership = st.selectbox('Type of ownership', options = df['Type of ownership'].unique())
ownership_vec = list2vec(df['Type of ownership'].unique(),ownership)

num_competitor = st.number_input('Number of Competitors', step = 1, min_value = 0, value = 0)


st.subheader('Job Features:')

job_state = st.selectbox("Job location", options = df["job_state"].unique())
job_state_vec = list2vec(df['job_state'].unique(),job_state)

same_state = st.radio("Is the job location the same as headquarters? (0 for No, 1 for Yes)", options=[0, 1])
description_length = st.slider('Job description character length', min_value = 0, max_value = 10000, step = 1000)

job_title = st.selectbox("Job title, na means not specified", options = df["job_simp"].unique())
job_title_vec = list2vec(df['job_simp'].unique(),job_title)

seniority = st.selectbox("Job seniority, na means not specified", options = df["seniority"].unique())
seniority_vec = list2vec(df['seniority'].unique(),seniority)


st.subheader('Skills required by the job:')

python_yn = st.radio("Python (0 for No, 1 for Yes)", options=[0, 1])
sql_yn = st.radio("SQL (0 for No, 1 for Yes)", options=[0, 1])
excel_yn = st.radio("Excel (0 for No, 1 for Yes)", options=[0, 1])
aws_yn = st.radio("AWS (0 for No, 1 for Yes)", options=[0, 1])
nlp_yn = st.radio("Natural language processing NLP (0 for No, 1 for Yes)", options=[0, 1])


# organize all inputs into vector for model to read
features = [num_competitor,same_state,python_yn,sql_yn,excel_yn,aws_yn,nlp_yn,
            description_length] + list(ownership_vec) +list(sector_vec) + \
            list(job_state_vec) + list(job_title_vec) +list(seniority_vec)
            
features2read = np.array(features).reshape(1, -1)

if st.button('Estimate Salary'):
    estimation = model.predict(features2read)
    st.balloons()
    st.success(f'Your estimated salary is {int(round(estimation[0]))} K US$')