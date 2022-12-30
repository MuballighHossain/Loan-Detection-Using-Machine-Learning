# -*- coding: utf-8 -*-
"""loan_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hab-9FcO8gP4wU01lvQHa-zbiXsxjjeY

#Start
"""

# Importing the required Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk

# Mounting Drive to the Colab Notebook
from google.colab import drive
drive.mount('/content/drive')

# We will read our CSV file from our Google Drive and store it in a variable called df
df = pd.read_csv('/content/drive/MyDrive/BRAC/Thesis/Loan/Dataset/Better/application_data.csv')

#Toufique Runs
# df = pd.read_csv('/content/drive/MyDrive/Coding/437 Project/application_data.csv')

#Viewing the shape and structure of our dataset/ counting rows and columns of the data set
df.shape

#Viewing a portion of the dataset to learn more about it
df.head(10)

"""#Preprocessing Begins"""

# Counting the empty columns
df.isna().sum()

df.describe()

df['HOUSETYPE_MODE'].unique()

df['CODE_GENDER'].unique()

df['NAME_TYPE_SUITE'].unique()

df['NAME_INCOME_TYPE'].unique()

"""# Rows 1-30 Toufique"""

# loan_df = df[['SK_ID_CURR', 'TARGET', 'NAME_CONTRACT_TYPE', 'CODE_GENDER',
#        'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN',
#        'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE',
#        'NAME_TYPE_SUITE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE',
#        'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE',
#        'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_EMPLOYED',
#        'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'OWN_CAR_AGE',
#        'FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE',
#        'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL', 'OCCUPATION_TYPE',
#        'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT']]

df.isnull().sum().sum()

df['NAME_CONTRACT_TYPE'].value_counts()

"""# One Hot Encoding"""

!pip install category_encoders #for ONE HOT ENCODING

import category_encoders as ce

#specify that all columns should be shown
pd.set_option('max_columns', None)

#view DataFrame
df

# import modules
# from numpy import isnan
# from sklearn.impute import SimpleImputer

#df['OCCUPATION_TYPE'].isnull().sum()
# df['OCCUPATION_TYPE'].unique()

# df['REGION_RATING_CLIENT'].unique() # ---- checked --- 
# df['REGION_RATING_CLIENT'].isnull().sum() #None

# df['CNT_FAM_MEMBERS'].unique() # ----- includes nan -----
# df['CNT_FAM_MEMBERS'].isnull().sum() #None

# df['NAME_HOUSING_TYPE'].unique() # ----enc-
# df['NAME_HOUSING_TYPE'].isnull().sum() #None

# df['NAME_FAMILY_STATUS'].unique() #----enc-
# df['NAME_FAMILY_STATUS'].isnull().sum()

# df['NAME_EDUCATION_TYPE'].unique() #----enc-
# df['NAME_EDUCATION_TYPE'].isnull().sum() #None

# df['NAME_INCOME_TYPE'].unique() #----enc-
# df['NAME_INCOME_TYPE'].isnull().sum() #None

#df['NAME_TYPE_SUITE'].unique() #----can drop
# df['NAME_INCOME_TYPE'].isnull().sum() #None

# import numpy as np
# flags = np.unique(df[['FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE',
#        'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL',]].values)

uniqueValues = (df['FLAG_MOBIL'].append(df['FLAG_EMP_PHONE'])).unique()
print(uniqueValues)

df.dtypes

# obj_df = loan_df.select_dtypes(include=['object']).copy()
# obj_df.head()

# obj_df[obj_df.isnull().any(axis=1)]

df["CODE_GENDER"].value_counts()

#Removing transgenders
mask = df["CODE_GENDER"] =="XNA"
df = df[~mask]

df["CODE_GENDER"].value_counts()

df["NAME_TYPE_SUITE"].value_counts() #Ordinal

df['NAME_TYPE_SUITE'] = df['NAME_TYPE_SUITE'].str.replace('Spouse, partner', 'Spouse', regex = False) 
df["NAME_TYPE_SUITE"].value_counts()

df["NAME_INCOME_TYPE"].value_counts() #Ordinal / One Hot

df["NAME_EDUCATION_TYPE"].value_counts()  #Ordinal / One Hot

df['NAME_EDUCATION_TYPE'] = df['NAME_EDUCATION_TYPE'].str.replace('Secondary / secondary special', 'Secondary special', regex = False) 
df["NAME_EDUCATION_TYPE"].value_counts()

df["NAME_FAMILY_STATUS"].value_counts() #Ordinal / One Hot

mask = df["NAME_FAMILY_STATUS"] =="Unknown"
df = df[~mask]
df['NAME_FAMILY_STATUS'] = df['NAME_FAMILY_STATUS'].str.replace('Single / not married', 'Single', regex = False) 
df["NAME_FAMILY_STATUS"].value_counts()

df["NAME_HOUSING_TYPE"].value_counts() #Ordinal / One Hot

df['NAME_HOUSING_TYPE'] = df['NAME_HOUSING_TYPE'].str.replace('House / apartment', 'House', regex = False) 
df["NAME_HOUSING_TYPE"].value_counts() #ONE HOT

df["OCCUPATION_TYPE"].value_counts()

flag_encoded = {"FLAG_OWN_CAR":     {"Y": 1, "N": 0},
                "FLAG_OWN_REALTY": {"Y": 1, "N": 0}}

df = df.replace(flag_encoded)
df.head()

df["NAME_CONTRACT_TYPE"].value_counts()

flag_encoded = {"NAME_CONTRACT_TYPE":     {"Cash loans": 1, "Revolving loans": 0}}

df = df.replace(flag_encoded)
df.head()

gender_encoded = {"CODE_GENDER":     {"M": 1, "F": 0}}
df = df.replace(gender_encoded)
df.head()

#Dropping Unneceary column
df.drop(['NAME_TYPE_SUITE'], axis = 1, inplace = False)

#Replacing NaN Values -- Method 1 --- 
df.OCCUPATION_TYPE.fillna("None", inplace = True)

## Replacing NaN Values -- Method 2 ---

# from sklearn.impute import SimpleImputer
# imputer = SimpleImputer(strategy = 'Most Frequent')
# imputer = SimpleImputer(strategy = 'constant', fill_value = 'missing')
# imputer.fit_transform('data')

df["OCCUPATION_TYPE"].value_counts()

"""Encoding Part"""

from sklearn.preprocessing import OrdinalEncoder

ord_enc = OrdinalEncoder()
df["OCCUPATION_TYPE"] = ord_enc.fit_transform(df[["OCCUPATION_TYPE"]])
df[[ "OCCUPATION_TYPE"]]

ord_enc = OrdinalEncoder()
df["NAME_TYPE_SUITE"] = ord_enc.fit_transform(df[["NAME_TYPE_SUITE"]])
df[[ "NAME_TYPE_SUITE"]]

df["NAME_INCOME_TYPE"] = ord_enc.fit_transform(df[["NAME_INCOME_TYPE"]])
df[[ "NAME_INCOME_TYPE"]]

df["NAME_EDUCATION_TYPE"] = ord_enc.fit_transform(df[["NAME_EDUCATION_TYPE"]])
df[[ "NAME_EDUCATION_TYPE"]]

df["NAME_FAMILY_STATUS"] = ord_enc.fit_transform(df[["NAME_FAMILY_STATUS"]])
df[[ "NAME_FAMILY_STATUS"]]

ord_enc = OrdinalEncoder()
df["WEEKDAY_APPR_PROCESS_START"] = ord_enc.fit_transform(df[["WEEKDAY_APPR_PROCESS_START"]])
df[[ "WEEKDAY_APPR_PROCESS_START"]]

ord_enc = OrdinalEncoder()
df["ORGANIZATION_TYPE"] = ord_enc.fit_transform(df[["ORGANIZATION_TYPE"]])
df[[ "ORGANIZATION_TYPE"]]

# !pip install category_encoders #for ONE HOT ENCODING
# import category_encoders as ce
encoder = ce.OneHotEncoder(cols = 'NAME_HOUSING_TYPE', use_cat_names = True)
df = encoder.fit_transform(df)

pd.set_option('display.max_columns', None)
df.head()

df.head()

"""# Rows 31-60 Sadid
# Rows 61-90 Muba
# Rows 91-124 Masroor

#Sadid (61-90)

almost all of the later ones are numerical floating normalized values
"""

df.iloc[:, 28:70]=df.iloc[:, 28:70].fillna(-1)
df['OCCUPATION_TYPE'].replace({-1:"None"})
df['ORGANIZATION_TYPE'].replace({-1:"None"})

df['OCCUPATION_TYPE'].value_counts()

"""# Masroor SPACE (91-124)

"""

df['WALLSMATERIAL_MODE'].fillna('None', inplace = True)

df['WALLSMATERIAL_MODE'].head(15)

df['WALLSMATERIAL_MODE'].value_counts()

import category_encoders as ce

encoder = ce.OneHotEncoder(cols = 'WALLSMATERIAL_MODE', use_cat_names = True)

df = encoder.fit_transform(df)

"""To verify the one hot encoding"""

#specify that all columns should be shown
pd.set_option('max_columns', None)

#view DataFrame
df

df['EMERGENCYSTATE_MODE'].unique()

df['EMERGENCYSTATE_MODE'].fillna('None', inplace = True)

encoder = ce.OneHotEncoder(cols = 'EMERGENCYSTATE_MODE', use_cat_names = True)

df = encoder.fit_transform(df)

df.columns.values

# cols = ['OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE',
#        'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE']
# # df[cols] = [df[x].replace({'None':-1}) for x in cols]
# df[cols] = df[cols].replace({-1:"None"})
# df[cols]
df['OBS_30_CNT_SOCIAL_CIRCLE'].fillna('-1', inplace = True)
df['OBS_30_CNT_SOCIAL_CIRCLE'].isnull().sum()

df['DEF_30_CNT_SOCIAL_CIRCLE'].fillna('-1', inplace = True)
df['DEF_30_CNT_SOCIAL_CIRCLE'].isnull().sum()

df['OBS_60_CNT_SOCIAL_CIRCLE'].fillna('-1', inplace = True)
df['OBS_60_CNT_SOCIAL_CIRCLE'].isnull().sum()

df['DEF_60_CNT_SOCIAL_CIRCLE'].fillna('-1', inplace = True)
df['DEF_60_CNT_SOCIAL_CIRCLE'].isnull().sum()

df = df.dropna(axis = 0, subset = ['DAYS_LAST_PHONE_CHANGE'])

df['DAYS_LAST_PHONE_CHANGE'].isnull().sum()

df['AMT_REQ_CREDIT_BUREAU_HOUR'].fillna('-1', inplace = True)
df['AMT_REQ_CREDIT_BUREAU_HOUR'].isnull().sum()

df['AMT_REQ_CREDIT_BUREAU_DAY'].fillna('-1', inplace = True)
df['AMT_REQ_CREDIT_BUREAU_DAY'].isnull().sum()

df['AMT_REQ_CREDIT_BUREAU_WEEK'].fillna('-1', inplace = True)
df['AMT_REQ_CREDIT_BUREAU_WEEK'].isnull().sum()

df['AMT_REQ_CREDIT_BUREAU_MON'].fillna('-1', inplace = True)
df['AMT_REQ_CREDIT_BUREAU_MON'].isnull().sum()

df['AMT_REQ_CREDIT_BUREAU_QRT'].fillna('-1', inplace = True)
df['AMT_REQ_CREDIT_BUREAU_QRT'].isnull().sum()

df['AMT_REQ_CREDIT_BUREAU_YEAR'].fillna('-1', inplace = True)
df['AMT_REQ_CREDIT_BUREAU_YEAR'].isnull().sum()

"""#Muballigh Columns (61-90) """

from sklearn.impute import SimpleImputer
impute = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=-1)

# Imputing 'APARTMENTS_MODE'
impute.fit(df[['APARTMENTS_MODE']])

df['APARTMENTS_MODE'] = impute.transform(df[['APARTMENTS_MODE']])

df['APARTMENTS_MODE'].head(15)

# Imputing 'BASEMENTAREA_MODE'
impute.fit(df[['BASEMENTAREA_MODE']])
df['BASEMENTAREA_MODE'] = impute.transform(df[['BASEMENTAREA_MODE']])
print(df['BASEMENTAREA_MODE'].isnull().sum()) # checking if 'BASEMENTAREA_MODE' has any empty values
df['BASEMENTAREA_MODE'].head(15)

# Imputing Columns 59 to 85
impute.fit(df.iloc[:,59:85])
df.iloc[:,59:85] = impute.transform(df.iloc[:,59:85])
df.iloc[:,59:85].head(10)

# Imputing 'NONLIVINGAREA_MEDI'
impute.fit(df[['NONLIVINGAREA_MEDI']])
df['NONLIVINGAREA_MEDI'] = impute.transform(df[['NONLIVINGAREA_MEDI']])
df['NONLIVINGAREA_MEDI'].head(15)

# Imputing 'TOTALAREA_MODE'
impute.fit(df[['TOTALAREA_MODE']])
df['TOTALAREA_MODE'] = impute.transform(df[['TOTALAREA_MODE']])
df['TOTALAREA_MODE'].head(15)

df['FONDKAPREMONT_MODE'].fillna('None', inplace = True)

encoder = ce.OneHotEncoder(cols = 'FONDKAPREMONT_MODE', use_cat_names = True)

df = encoder.fit_transform(df)

df['HOUSETYPE_MODE'].fillna('None', inplace = True)

encoder = ce.OneHotEncoder(cols = 'HOUSETYPE_MODE', use_cat_names = True)
df = encoder.fit_transform(df)

df.isnull().sum()

df['LIVINGAPARTMENTS_MEDI'].fillna('-1', inplace = True)
df['LIVINGAPARTMENTS_MEDI'].isnull().sum()

df['LIVINGAREA_MEDI'].fillna('-1', inplace = True)
df['LIVINGAREA_MEDI'].isnull().sum()

df['NONLIVINGAPARTMENTS_MEDI'].fillna('-1', inplace = True)
df['NONLIVINGAPARTMENTS_MEDI'].isnull().sum()

df['FLOORSMIN_MEDI'].fillna('-1', inplace = True)
df['FLOORSMIN_MEDI'].isnull().sum()

df['LANDAREA_MEDI'].fillna('-1', inplace = True)
df['LANDAREA_MEDI'].isnull().sum()

df['OWN_CAR_AGE'].fillna('-1', inplace = True)
df['OWN_CAR_AGE'].isnull().sum()

pd.set_option('display.max_columns', None)
df

df.isnull().sum().sum()

# using dropna() function  
df = df.dropna(axis=0)

df.isnull().values.any()

df.isnull().sum().sum()

# Finding out Correlation between columns
df.iloc[:,1:144].corr()

# Visualizing correlation
fig, ax = plt.subplots(figsize=(100,100))
sns.heatmap(df.iloc[:,1:144].corr(),annot=True, linewidth = 10, ax=ax, fmt='.0%')



temp = df[['TARGET','FLAG_DOCUMENT_3',  'FLAG_DOCUMENT_2' ,  'DAYS_LAST_PHONE_CHANGE',  'EMERGENCYSTATE_MODE_None', 'WALLSMATERIAL_MODE_None', 'WALLSMATERIAL_MODE_Wooden', 'HOUSETYPE_MODE_specific housing', 'HOUSETYPE_MODE_None', 'FONDKAPREMONT_MODE_None', 'REG_CITY_NOT_LIVE_CITY', 'REG_CITY_NOT_WORK_CITY','LIVE_CITY_NOT_WORK_CITY', 'REG_REGION_NOT_LIVE_REGION','REG_REGION_NOT_WORK_REGION', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY', 'FLAG_EMP_PHONE','FLAG_WORK_PHONE', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'DAYS_BIRTH', 'NAME_HOUSING_TYPE_Rented apartment','NAME_HOUSING_TYPE_With parents', 'NAME_TYPE_SUITE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_CONTRACT_TYPE', 'CODE_GENDER', 'CNT_CHILDREN']]

"""# Splitting"""

# -------------------  Splitting Begins Here ------------------------------------------

# Splitting the dataset into independent X and dependent Y
x = temp.drop(['TARGET'],axis=1)
y = df['TARGET']

# Train and Test Split --- > Train : 70%, Test : 30%
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,train_size=0.7, random_state=0)
print("Training dataset shape : ",x_train.shape)
print("Testing dataset shape : ",x_test.shape)
x_train.head()

"""#Scaling"""

# -------------------  Scaling Begins Here ------------------------------------------

# Scaling our data in order to remove biasness or deviance - Feature Scaling
# Method - Min Max Scaling Method
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x_train)

# Transforming
x_train_temp = scaler.transform(x_train)

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

"""# Model Running

#Logistic Regression
"""

# ---------------------------------- Logistic Regression -----------------------------
model_conduct = LogisticRegression()
model_conduct.fit(x_train, y_train) #Training the model
predictions = model_conduct.predict(x_test)
print(predictions)# printing predictions

# Logistic Regression Accuracy Test
LogisticRegressionAccuracyTest = accuracy_score(y_test, predictions)
print("Accuracy of Logistic Regression : ",LogisticRegressionAccuracyTest)

"""#Decision Tree"""

#---------------------- Decision Tree -------------------------------------------
conduct = DecisionTreeClassifier(criterion='entropy',random_state=20)
conduct.fit(x_train, y_train)
y_prediction = conduct.predict(x_test)
DecisionTreeAccuracyTest = accuracy_score(y_prediction,y_test)
print("Accuracy of Decision Tree : ",DecisionTreeAccuracyTest) #Decision Tree Accuracy

# -------------------- DT vs LR -----------------------------
fig, ax = plt.subplots()
names = ['Logistic Regression','Decision Tree']
acc =[LogisticRegressionAccuracyTest, DecisionTreeAccuracyTest]
position = [1,2]
ax.bar(position,acc, width=0.7, color="m", bottom=None, align='center')
plt.xticks(position,names)
ax.set_title('Accuracy Comparision of Logistic Regression and Decision Tree')
ax.set_xlabel('Classification')
ax.set_ylabel('Accuracy')

# ---------------------  Support Vector Classifier ---------------------------------
# from sklearn.svm import SVC
# svc = SVC(kernel="linear")
# svc.fit(x_train,y_train)
# accuracy_train_01 = svc.score(x_train,y_train)
# accuracy_test_01 = svc.score(x_test,y_test)
# print("Training accuracy is {:.2f}".format(accuracy_train_01))
# print("Testing accuracy is {:.2f}".format(accuracy_test_01))

# predictions = svc.predict(x_test)
# print(predictions)

"""#Random Forest"""

# --------------------------Random Forest -----------------------------------
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=22)
rfc.fit(x_train, y_train)
accuracy_train_RFC=rfc.score(x_train, y_train)
accuracy_test_RFC=rfc.score(x_test, y_test)
print("Training accuracy is {:.2f}".format(accuracy_train_RFC))
print("Testing accuracy is {:.2f}".format(accuracy_test_RFC))

"""#Neural Network Classifier"""

#-------------------Neural Network Classifier---------------------------------
from sklearn.neural_network import MLPClassifier
nnc=MLPClassifier(hidden_layer_sizes=(7), activation="relu", max_iter=10000)

nnc.fit(x_train, y_train)

accuracy_train_nnc= nnc.score(x_train, y_train)
accuracy_test_nnc= nnc.score(x_test, y_test)
print("Training accuracy is {:.2f}".format(accuracy_train_nnc))
print("Testing accuracy is {:.2f}".format(accuracy_test_nnc))

predictions = nnc.predict(x_test)
print(predictions)

"""#GaussianNB"""

from sklearn.naive_bayes import GaussianNB

# create the model
GNB = GaussianNB()

# train the model on the training data
GNB.fit(x_train, y_train)

# make predictions on the test data
predictions = GNB.predict(x_test)

# compute the accuracy of the predictions
accuracyGNB = accuracy_score(y_test, predictions)

print("Accuracy:", accuracyGNB)

"""#Comparison"""

import math
data = {'Logistic Regression':LogisticRegressionAccuracyTest , 
        'Decision Tree':DecisionTreeAccuracyTest,
        'Random Forest' : accuracy_test_RFC,
        'NNC':accuracy_test_nnc,
        'GNB':accuracyGNB}
attributesUsed = list(data.keys())
scores = list(data.values())
fig = plt.figure(figsize = (10, 5))
plt.bar(attributesUsed, scores, width=0.35, color='m')
plt.xlabel('Classifications: Logitic Regression, Decision Tree, Random Forest, Gaussian Naive Bayes & NNC')
plt.ylabel('Accuracy')
plt.title('Comparison of Accuracy amongst ML Models')
low = min(y)
high = max(y)
plt.ylim([.8, .95])
plt.show()

# ---------------------------Principle Component Analysis------------------------------
temp.keys()

# ------------------ Scaling the values before PCA ------------------------
from sklearn.preprocessing import StandardScaler
scaler= StandardScaler()
xScaledTrain=scaler.fit_transform(x_train)

temp.shape

from sklearn.decomposition import PCA 
pca = PCA(n_components=5)

principal_components= pca.fit_transform(xScaledTrain)
print(principal_components)

pca.explained_variance_ratio_

sum(pca.explained_variance_ratio_)

principal_df = pd.DataFrame(data=principal_components, columns=["principle_component_1", "principle_component_2","3","4","5"])
main_df=pd.concat([principal_df, df[['benign_malignant']]], axis=1)
principal_df.head()

main_df = main_df.dropna(how='any')

xPCA=main_df.drop('benign_malignant',axis=1)
yPCA=main_df[['benign_malignant']]
x_train, x_test, y_train, y_test = train_test_split(xPCA, yPCA,stratify=yPCA, train_size=.8,random_state=42)
main_df.head()