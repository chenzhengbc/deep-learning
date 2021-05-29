# %%
from numpy.core.defchararray import startswith
import pandas as pd
import numpy as np
from pandas.io.stata import value_label_mismatch_doc

df = pd.DataFrame({
    'a': ['one', 'two', 'three', 'four', 'six', 'three'],
    'b': ['x', 'y', 'y', 'x', 'y', 'x'],
    'c': np.random.randn(6)
})
df
# %%
criterion1 = df['a'].map(lambda x: x.startswith('t'))
criterion2 = df['c'].map(lambda x: x > 0.5)
df[criterion1 & criterion2]

# %%
df = pd.DataFrame({
    'vals': [1, 2, 3, 4],
    'ids': ['a', 'b', 'f', 'n'],
    'id2': ['e', 'f', 'a', 'h']
})
df
values = ['a', 'b', 1, 2]
df.isin(values)
df
# %%

values = {'ids': ['a'], 'id2': ['e']}
df.isin(values)

# %%
abc = ['王薇'] + ['刘敏']
abc
# %%
test1 = pd.DataFrame(
    {'班级': [1, 2, 2, 1], '姓名': [['王薇'], ['刘敏'], ['陈芳'], ['袁芬']]})
# test2
test2 = test1.groupby(['班级']).sum()
test2
test3 = test1[['姓名']]
test3
