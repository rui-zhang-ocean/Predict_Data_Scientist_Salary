# Project Summary

* Built [a web app](https://estimate-data-scientist-salary.herokuapp.com/) that estimates data science job salaries to help with job offer negotiation.
* Scraped 900+ job posts from glassdoor using Python and Selenium.
* Engineered features from job description text to quantify skillsets (Python, SQL, Excel, etc) most desirable by employers, job locations, job titles and seniorities.
* Conducted exploratory data analysis (EDA) using histogram, barplot, boxplot, heatmap and pivot_table.
* Compared Multiple Linear Regression, Lasso Regression (optimized alpha) and Random Forest (optimized with GridSearchCV) models, among which Random Forest performs best, with mean absolute error ~ $12K.
* Built web app with Streamlit and deployed with Heroku.

## Web Application Demo

[![Demo](https://github.com/rui-zhang-ocean/Estimate_Data_Scientist_Salary/blob/master/figs/web_app_demo.gif)](https://estimate-data-scientist-salary.herokuapp.com/)

## Resources

* Python Version: 3.8.3
* Tools: pandas, numpy, sklearn, matplotlib, seaborn, selenium, joblib, streamlit, Heroku 
* Project idea inspired by [Ken Jee](https://www.youtube.com/channel/UCiT9RITQ9PW6BhXK0y2jaeg)
* Selenium scraper tutorial credits to [Ömer Sakarya](https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905)
* Streamlit and Heroku turotial credits to [Sohaib Ahmad](https://towardsdatascience.com/deploy-streamlit-on-heroku-9c87798d2088) and [Chanin Nantasenamat](https://www.youtube.com/watch?v=zK4Ch6e1zq8)

## 0_collect_data

To scrape 900+ job postings from glassdoor.com with Selenium, for each job, I got:

* Job title 
* Salary Estimate
* Job Description
* Rating
* Company
* Location
* Company Headquarters
* Company Size
* Company Founded Year
* Type of Ownership
* Industry
* Sector
* Revenue
* Competitors

## 1_clean_data

To clean the data and engineer new features, steps include:

* Parsed mininum and maximum salary from the range string, calculated its average
* Converted hourly salary to annually
* Discarded data without salary
* Extracted from job description text on following skills:
  * Python
  * SQL
  * Excel
  * AWS
  * NLP
* Made new columns including:
  * company state
  * if job location is equal to head quarter location
  * company age in years
  * simplified job titles with categories of `data scientist`, `data engineer`, `analyst`, etc
  * seniority (`junior` or `senior` or `na`)
  * length of job description
  * number of competitors

## 2_exploratory_data_analysis

I conducted exploratory data analysis (EDA) using histogram, heatmap, barplot, boxplot, pivot_table and word cloud. A few highlighted points and figures/tables are as below:

![alt text](https://github.com/rui-zhang-ocean/data_scientist_salary/blob/master/figs/histogram.png "histogram") 
* Average salary deviates from the normal distribution with slight positive skewness

![alt text](https://github.com/rui-zhang-ocean/data_scientist_salary/blob/master/figs/heatmap.png "heatmap") 
* Older companies tend to have more competitors and longer job description

![alt text](https://github.com/rui-zhang-ocean/data_scientist_salary/blob/master/figs/boxplot_python_yn.png "boxplot_python")![alt text](https://github.com/rui-zhang-ocean/data_scientist_salary/blob/master/figs/boxplot_excel_yn.png "boxplot_excel")
* Jobs requiring `Python` typically pays more, and jobs requiring `Excel` typically pays less

job_simp         | avg_salary  
---------------- | -----------
director         | 168.61
machine learning | 126.43
data scientist   | 117.56
data engineer    | 105.40
na               | 87.97
manager          | 84.02
analyst          | 66.12
* Top three best paid data positions are director, machine learning and data scientist.

 skill    | Total	|Percent
--------- | ------|-------
python_yn	|392	   |0.5283
excel_yn	 |388	   |0.5229
sql_yn	   |380	   |0.5121
aws_yn	   |176	   |0.2372
spark_yn	 |167	   |0.2251
nlp_yn	   |40	    |0.0539
* Over half of the positions require one of the three skills: `Python`, `Excel` and `SQL`.

python_yn|	0 	| 1	
---------| ---| ---
junior	  |2	  | 3
na	      |252	| 265
senior	  |96	 | 124
* `Python` is more often needed in senior positions compared to generic (non-specific seniority) positions.

## 3_build_model

Pre-processings include transformation of categorical variables into dummy variables (one hot encoding), and splitting of the data into train and tests sets with a test size of 20%.

The dataset outliers aren't particularly bad, and considering the sparsity of the data, and many categorical columns with one hot encoding, I tried three different models and  used Mean Absolute Error for evaluation. Cross validation were used as well. Models are:

* Multiple Linear Regression – Baseline estimate
* Lasso Regression – Normalized regression could effectively reduce over-fitting caused by OLS regression
* Random Forest – Good fit considering the sparsity and one hot encoding of categorical data

I performed optimization for `alpha` in Lasso Regression and `n_estimators`, `criterion` and `max_features` in Random Forest with GridsearchCV, both obtained improvement on validation sets. 

Results:

Models                     | Validation sets | Validation sets after optimization | Test sets
-------------------------- | ----------------| -----------------------------------|---------
Multiple Linear Regression | 20.96           | N/A                                | 17.75
Lasso Regression           | 21.51           | 20.02                              | 18.05
Random Forest              | 15.96           | 15.32                              | 11.85

The Random Forest model outperformed the other approaches on test sets, with a MAE of ~ $12K.

## 4_deploy_web_app

The optimized Random Forest model is pickled using Joblib, with that a web app is created using Streamlit and deployed with Heroku. It can be accessed [here](https://estimate-data-scientist-salary.herokuapp.com/). 

## 5_future_steps

* Over half of job posts didn't specify seniority on the job title, if we could extract years of experience requirement from job description, that would be a good indicator of seniority. Or we could use a new feature `years of experience required`.
* The skills extraction could be improved by applying NLP techniques, i.e. check `tokens` from description text, by doing that we can capture skill with shorter name, such as R
* Play with different models or ensemble approach, set up workflow pipeline to make that an automated process
* Continue scraping job posts data to organize into database, allow users to choose which years data to use for the estimation. From a practical purpose, only using the most recent data can reflect the most recent job market variation.
