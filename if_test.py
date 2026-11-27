from sklearn.ensemble import IsolationForest  # noqa: I001
# 从 sklearn集成模块导入孤立森林算法
# sklearn（python的库，放了很多算法)
# ensemble（库里面的一个，叫集成）；Isolation Forest就是这类，是一个具体的工具
# from...import... = 只拿这一个工具

import numpy as np

X = np.array([[1], [2], [3], [4], [100]])  # 100 明显是离群点
clf = IsolationForest(contamination=0.2, random_state=42)
clf.fit(X)
print(clf.predict(X))