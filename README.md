# Project Summary

* Created a model that estimates data science job salaries (mean absolute error ~ $12K) to help with job offer negotiation.
* Scraped 1000 job posts from glassdoor using Python and Selenium.
* Engineered features from job description text to quantify skillsets (Python, SQL, Excel, etc) most desirable by employers.
* Conducted exploratory data analysis (EDA) using histogram, barplot, boxplot, heatmap and pivot_table.
* Compared Multiple Linear Regression (baseline), Lasso Regression (optimized alpha) and Random Forest (optimized with GridSearchCV) models, among which Random Forest performs best.

## Resources

* Python Version: 3.8.3
* Packages: pandas, numpy, sklearn, matplotlib, seaborn, selenium
* Scraper Github: https://github.com/arapfaik/scraping-glassdoor-selenium

## 0_collect_data

To scrape 1000 job postings from glassdoor.com with Selenium, for each job, we got:

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
* Extracted from job description text if following skillsets are mentioned:
  * Python
  * Rstudio
  * SQL
  * Excel
  * AWS
  * Spark
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

I conducted exploratory data analysis (EDA) using histogram, correlation heatmap, barplot, boxplot, pivot_table and word cloud. A few highlighted points and figures/tables are as below:

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
* Random Forest – Good fit considering the sparsity and one hot encoding of the data

I performed optimization for `alpha` in Lasso Regression and `n_estimators`, `criterion` and `max_features` in Random Forest with GridsearchCV, both obtained improvement on validation sets. 

Results:

Models                     | Validation sets | Validation sets after optimization | Test sets
-------------------------- | ----------------| -----------------------------------|---------
Multiple Linear Regression | 22.27           | N/A                                | 303045468.79
Lasso Regression           | 21.57           | 20.10                              | 18.70
Random Forest              | 15.81           | 15.33                              | 12.49

The Random Forest model outperformed the other approaches on the validation and test sets. It is worth noting that Multiple Linear Regression performs reasonably well on validation sets but horrible for test sets, which is a typical over-fitting case, that also justified the use of Lasso Regression.


## 4_future_steps

* Imputation of missing values
* Try different models or ensemble approach
* Productionize the model into a web page, ideally anyone can input job information and get salary estimate as return
