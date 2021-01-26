import numpy
from sklearn.linear_model import LinearRegression

#restructuring data
data = numpy.genfromtxt('data.csv', delimiter=',')[:-51, :]
data = numpy.delete(data, 0, 0)
demvote = data[:, 3]
columns = [4, 5, 6, 7, 8]
variables = data[:, columns].reshape(-1, 5)

regression = LinearRegression()
regression.fit(variables, demvote)

current = numpy.genfromtxt('data.csv', delimiter=',')[-51:, :]
print(regression.coef_)
print(regression.intercept_)
print(regression.predict(current[:, columns].reshape(-1, 5)))
print(regression.score(variables, demvote))
