import pandas as pd
df = pd.read_csv('DS_salary_raw.csv')

# remove second column
df = df.drop(['Unnamed: 0'],axis=1)

# salary parsing
# remove rows without salary info
df = df[df['Salary Estimate'] != '-1']

# add columns indicating if hourly paid
df['hourly'] = df['Salary Estimate'].str.lower().str.contains('per hour').astype(int)

# remove unnecessry strings and extract min, max and average salary
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0]).str.replace('$','').str.replace('K','').str.replace('Per Hour','')
df['min_salary'] = salary.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = salary.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary + df.max_salary)/2

# company name
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

# location by state and if head quarter in the same location
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1]).str.replace(' ','')
#df['job_state'].value_counts()
df['same_state'] = df.apply(lambda x: 1 if x['Location'] == x['Headquarters'] else 0, axis = 1)

# age
df['age'] = df['Founded'].apply(lambda x: 2020 - int(x) if int(x) > 0 else int(x))

# job description keywords selection
skills = ['python','sql','excel','aws','spark','nlp','rstudio']

for skill in skills:
    df[skill + '_yn'] = df['Job Description'].apply(lambda x: 1 if skill in x.lower() else 0)
    #print(df[skill + '_yn'].value_counts())

#df.to_csv('DS_salary_cleaned.csv',index = False)

