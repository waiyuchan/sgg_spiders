from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt


x = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90,
     89, 88, 87, 86, 85, 84, 83, 82, 81, 80,
     79, 78, 77, 76, 75, 74, 73, 72, 71, 70,
     69, 68, 67, 66, 65, 64, 63, 62, 61, 60]

y = [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
     3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
     2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
     1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, ]


x = np.array(x)
y = np.array(y)
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)
model = linear_model.LinearRegression()
model.fit(x, y)

print(model.intercept_, '\n', model.coef_)


def test(s):
    y = 0.09233449 * s - 4.85017422
    return y





y_ = [test(s) for s in x]
plt.plot(x, y)
plt.plot(x, y_)
plt.show()