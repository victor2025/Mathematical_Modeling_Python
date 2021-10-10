import pandas as pd
import numpy as np

data = pd.read_excel("..//res//env_year.xls")
data = data.drop(data.columns[0], axis=1)
data = data.dropna(axis=0, how="all")
data_mat_pre = data.values
data_mat = np.transpose(data_mat_pre)

data_ave = np.average(data_mat,axis=1)
print("done")
