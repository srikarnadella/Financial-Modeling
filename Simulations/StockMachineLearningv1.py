import quandl
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

quandl.ApiConfig.api_key = 'mJ5muSs_6sYexqwkt7P8'
print()
ticker = input("What stock do you want analysis on (ticker)? ")
dataset_code = f'WIKI/{ticker}'

df = quandl.get(dataset_code)

#print(df.head())


#Measure that reflects the stock's closing price after accounting for corporate actions such as dividends, stock splits, and new stock offerings. 
#Accurate representation of a stock's value over time, as it normalizes the price to make it comparable across different periods.
df = df[['Adj. Close']]
#print(df.head())

#Var that changes how far out to predict in days
forecastLength = 30


#Prediction is the next days value
#Creates an IV DV relationship as close is the IV and the DV is the next days price
df['Prediction'] = df[['Adj. Close']].shift(-forecastLength)

#print(df.head())
#print(df.tail())


#Dataframe -> Numpy array
X = np.array(df.drop(['Prediction'], axis=1))


#Removes the forcaselength rows
X = X[:-forecastLength]
#print(X)

Y = np.array(df['Prediction'])
Y = Y[:-forecastLength]
#print(Y)


#Training and testing split
test_size_var = 0.18
x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size = test_size_var)

#Creating and training the SVM  
svr_rbf = SVR(kernel = 'rbf', C = 1e3, gamma=0.1)

svr_rbf.fit(x_train, y_train)

#Model testing using score method by returning the coeff of determ R^2 of pred (1.0 high 0 low)
svm_conf = svr_rbf.score(x_test, y_test)
print()
print()

print("SVR Conf" , svm_conf)



#Linear Regression Model
#initalize
lr = LinearRegression()
#train
lr.fit(x_train, y_train)
#score
lr_conf = lr.score(x_test, y_test)
print("Linear Regression Conf" , lr_conf)

print()
print()

#now the models are trained we can forecast

#gives the last rows of the forecaselength
X_forecast = np.array(df.drop(['Prediction'], axis = 1))[-forecastLength:]


#Using the trained models it predicts the values
lr_prediction = lr.predict(X_forecast)

svm_prediction = svr_rbf.predict(X_forecast)
     

print("Linear Regression Prediction for next " , forecastLength , " days: " , lr_prediction)
print()
print()
print("SVM  Prediction for next " , forecastLength , " days: " , svm_prediction)