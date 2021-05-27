# -*- coding: utf-8 -*-

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# 加载数据
breast = load_breast_cancer()

# 数据拆分
X_train, X_test, y_train, y_test = train_test_split(
    breast.data, breast.target)

# 数据标准化
std = StandardScaler()
X_train = std.fit_transform(X_train)
X_test = std.transform(X_test)

# 训练预测
lg = LogisticRegression()

lg.fit(X_train, y_train)

y_predict = lg.predict(X_test)

# 查看训练准确度和预测报告
print(lg.score(X_test, y_test))
print(classification_report(
    y_test, y_predict, labels=[0, 1], target_names=["良性", "恶性"]))
