# -*- coding:utf-8 -*-

import pickle
from sklearn.svm import SVC
from sklearn import datasets

# 定义分类器
svm = SVC()
# 加载iris数据集
iris = datasets.load_iris()
# 读取特征
X = iris.data
print(X)
# 读取分类标签
y = iris.target
print(y)
# 训练模型
svm.fit(X, y)
# 保存成python支持的文件格式pickle, 在当前目录下可以看到svm.pickle
with open('svm.pickle', 'wb') as fw:
    pickle.dump(svm, fw)

# 加载svm.pickle
with open('svm.pickle', 'rb') as fr:
    new_svm = pickle.load(fr)
    print(X[0:1])    # 切片，取索引为0的第一行，从第一个索引到第二个索引切片，不包括第二个索引
    print(new_svm.predict(X[0:1]))


