# 相关分析函数
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
# import statsmodels.api as sm


def plotData(data1, data2):
    plt.scatter(data1, data2, color="r")
    plt.show()


def getPCA(x_train,n_com):
    # 创建模型
    pca = PCA(n_components=n_com)
    # 训练模型
    pca.fit(x_train)
    # 返回降维后数据
    x_pca = pca.transform(x_train)
    return x_pca

def pcaCorr(x_data,y_data):
    x_data_t = x_data.transpose()
    phi = np.dot(x_data_t, x_data)
    evalue, fvector = np.linalg.eig(phi)
    # 处理特征值和特征向量
    evalue = np.real(evalue)
    evalue[evalue<1e-4]=0
    fvector = np.real(fvector)
    # 获取主成分矩阵
    ind_prin = evalue>evalue.mean()
    n_com = ind_prin.sum()
    x_pca = getPCA(x_data,n_com)
    # 获取phi矩阵
    phi = fvector.copy()
    # 获取z矩阵
    z = np.dot(x_data, phi)
    z1 = z[:,ind_prin]
    # 获取alpha_hat_1
    z1_t_z1 = np.dot(z1.transpose(),z1)
    z1_t_z1_inv = np.linalg.inv(z1_t_z1)
    alpha_hat_1 = np.dot(np.dot(z1_t_z1_inv,z1.transpose()),y_data)
    # 获取beta_hat
    beta_hat_pre = np.concatenate((alpha_hat_1,np.zeros(len(evalue)-n_com)),axis=0)
    beta_hat = np.dot(phi,beta_hat_pre)
    # 获取alpha_hat_0
    alpha_hat_0 = y_data.mean()
    return beta_hat


