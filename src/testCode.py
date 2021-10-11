import pandas as pd
import numpy as np

# 数据预处理
data = pd.read_excel("..//res//data_gov.xls")
data.drop(data.columns[0], axis=1,inplace=True)
data.dropna(axis=0, how="all",inplace=True)
# 去除nan值较多的行
droped_row_ind = []
for index,row in data.iterrows():
    if row.isnull().sum()>5:
        data.drop(index,inplace=True)
        droped_row_ind.append(index)
        continue
    ave_now = row.dropna().mean()
data.reset_index(drop=True,inplace=True)
# 补全nan值
data.interpolate(method="linear",axis=1,inplace=True)
data.fillna(method="backfill",axis=1,inplace=True)

# 计算协方差矩阵与标准差
data_cov = data.T.cov()
data_std = data.std(axis=1)
# 转为numpy矩阵,并取标准差矩阵的逆
data_mat = np.transpose(data.values)
cov_mat = data_cov.values
std_inv = np.matrix(data_std).I
# 计算R
R_pre = np.dot(np.transpose(std_inv), cov_mat)
R = np.dot(R_pre, std_inv)

# 标准化矩阵
# 计算数据
mean_list = data.mean(axis=1)
mean_table = np.tile(mean_list,(data_mat.shape[0],1))
std_list = np.transpose(data_std)
std_table = np.tile(std_list,(data_mat.shape[0],1))
# 数据标准化
data_std_mat = (data_mat-mean_table)/std_table



print("done")
