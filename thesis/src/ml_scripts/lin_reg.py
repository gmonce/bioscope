import numpy as np
from sklearn import datasets
from sklearn import linear_model


# The diabetes dataset consists of 10 physiological variables (age, sex, weight, blood pressure) measure on 442 patients, and an indication of disease progression after one year:
diabetes=datasets.load_diabetes()
# Creo los corpus de entrenamiento y testeo, tomando 20 para testear
diabetes_X_train=diabetes.data[:-20]
diabetes_X_test=diabetes.data[-20:]
diabetes_y_train=diabetes.target[:-20]
diabetes_y_test=diabetes.target[-20:]


regr=linear_model.LinearRegression()
regr.fit(diabetes_X_train,diabetes_y_train)

# Imprimo los coeficientes
print "Coeficientes del clasificador: ", regr.coef_

# Imprimo el mean square error
print "Mean squared error:", np.mean((regr.predict(diabetes_X_test)-diabetes_y_test)**2)

# 
print "Score:",regr.score(diabetes_X_test,diabetes_y_test)







