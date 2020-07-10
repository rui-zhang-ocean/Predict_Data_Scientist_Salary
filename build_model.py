import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('DS_salary_cleaned.csv')

# choose modeled columns
df_model = df[['avg_salary','Rating','Size','Type of ownership','Industry',
               'Sector','Revenue','num_competitor','hourly', 'job_state',
               'same_state','age','python_yn','sql_yn','excel_yn','aws_yn',
               'nlp_yn', 'job_simp','seniority','description_length']]

# one hot encoding for categorical variables
df_dum = pd.get_dummies(df_model)

# train test split
from sklearn.model_selection import train_test_split
X = df_dum.drop('avg_salary',axis = 1)
y = df_dum.avg_salary.values
[X_train, X_test, y_train, y_test] = train_test_split(X, y, test_size=0.2, random_state = 1)

# multiple linear regression using stats and sklearn
import statsmodels.api as sm

X_sm = sm.add_constant(X_train)
model = sm.OLS(y_train,X_sm)
model.fit().summary()

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

lm = LinearRegression()
lm.fit(X_train,y_train)

np.mean(-1 * cross_val_score(lm,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3))

lm_Lasso = Lasso()
np.mean(-1 * cross_val_score(lm_Lasso,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3))

# loop to check out optimized alpha in Lasso model
alpha = []
error = []

for i in np.arange(0.01,1,0.01):
    alpha.append(i)
    lm_Lasso = Lasso(alpha = i)
    error.append(np.mean(-1 * cross_val_score(lm_Lasso,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3)))

plt.plot(alpha,error)

optimal_alpha = alpha[np.argmin(error)]

lm_Lasso_opt = Lasso(alpha = optimal_alpha)
lm_Lasso_opt.fit(X_train,y_train)


# random forest model
rf = RandomForestRegressor()
rf.fit(X_train,y_train)
np.mean(-1 * cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3))

# tune RF model with GridsearchCV
parameters = {'n_estimators': range(10,200,10),
              'criterion': ('mse', 'mae'),
              'max_features': ('auto','sqrt', 'log2')}

gs = GridSearchCV(rf, parameters, scoring = 'neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

# test all 3 methods
tpred_lm = lm.predict(X_test)
tpred_lml = lm_Lasso_opt.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)


