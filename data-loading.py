# %%
import numpy as np
import pandas as pd
import os
dates = pd.date_range("20210601", periods=6)
dates
# %%
rows = 6
df = pd.DataFrame(
    {
        "A": [1.02] * rows, 
        "B": pd.date_range("20210601", periods=rows),
        "C": pd.Series(3, index=list(range(rows)), dtype="float32"),
        "D": np.array([3] * rows, dtype="float32")        
    }
)
df.dtypes
df.describe()
df.head(6)
# %%
# df["20210601":"20210602"]
#df.sort_index(axis=1, ascending=False)

df["E"] = ["one", "one", "two", "three", "four", "three"]
# df.head(3)
r = df[df["E"].isin(["one","four"])]
r
# %%
# os.getcwd()
import numpy as np
import pandas as pd
import os
df = pd.read_csv("items.csv")
df.head(10)