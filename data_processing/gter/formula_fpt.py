from sklearn import linear_model
import numpy as np


"""
# 拟合出4.3绩点转百分制公式
x = [100, 99, 98, 97, 96, 95,
     94, 93, 92, 91, 90,
     89, 88, 87, 86, 85,
     84, 83, 82,
     81, 80, 79, 78,
     77, 76, 75,
     74, 73, 72,
     71, 70, 69, 68,
     67, 66, 65,
     64,
     63, 62, 61,
     60]
y = [4.3, 4.3, 4.3, 4.3, 4.3, 4.3,
     4.0, 4.0, 4.0, 4.0, 4.0,
     3.7, 3.7, 3.7, 3.7, 3.7,
     3.3, 3.3, 3.3,
     3.0, 3.0, 3.0, 3.0,
     2.7, 2.7, 2.7,
     2.3, 2.3, 2.3,
     2.0, 2.0, 2.0, 2.0,
     1.7, 1.7, 1.7,
     1.5,
     1.3, 1.3, 1.3,
     1.0]

x = np.array(x)
y = np.array(y)
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)
model = linear_model.LinearRegression()
model.fit(x, y)

print(model.intercept_, '\n', model.coef_)
"""


# 测试
def test(s):
    y = 0.0861324 * s - 3.9466899
    return y


x = [100, 95, 93, 90, 88, 85, 82, 77, 75, 72]
for i in range(0, len(x)-1):
    gpa = test(x[i])
    gpa = round(gpa, 2)
    print(gpa)
