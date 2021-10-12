# 读取数据并进行数据预处理
import pandas as pd
import numpy as np


def dataInitBuss(base_dir, file_name):
    # 初始设定
    file_path = base_dir + file_name + ".csv"
    ser_name_list = ["Shenzhen_USD", "Shenzhen_EUR", "Shanghai_USD", "Shanghai_EUR", "Beijing_USD", "Beijing_EUR",
                     "Guangdong_USD", "Guangdong_EUR", "Tianjin_USD", "Tianjin_EUR", "Hubei_USD", "Hubei_EUR",
                     "Chongqing_USD", "Chongqing_EUR", "Fujian_USD"]
    return file_path, ser_name_list


# 读取
def preProcessBuss(file_path, name_list):
    # 读取csv数据,去除最小有用数据
    data = pd.read_csv(file_path, sep=";")
    data = data.dropna(axis=1, how="all")
    # 去除无用行
    ind_min = data._ixs(1, 1).__len__()
    for index, item in data.iteritems():
        if (index in name_list):
            item_null = item.isnull()
            for ind_row in range(0, item.__len__() - 1):
                if (not item_null[ind_row]):
                    break
            ind_min = min(ind_row, ind_min)
    data = data.drop(data.index[0:ind_min])
    return data


def getBussinessData(file_name="data_cn"):
    base_dir = "..//res//"
    file_path, name_list = dataInitBuss(base_dir, file_name)
    data = preProcessBuss(file_path, name_list)
    # 保存为csv文件
    # data.to_csv(base_dir+file_name+"_converted.csv",index=False,sep=',')
    print("\n---商业数据读取完成")
    return data


def getGovData(file_name="data_gov"):
    base_dir = "..//res//"
    # 载入数据
    data = pd.read_excel(base_dir + file_name + ".xls")
    data.drop(data.columns[0], axis=1, inplace=True)
    data.dropna(axis=0, how="all", inplace=True)
    # 截取2013年之后的数据
    for index, item in data.iteritems():
        if (int(index) < 2013):
            data.drop(index, axis=1, inplace=True)
    # 去除nan值较多的行
    droped_row_ind = []
    for index, row in data.iterrows():
        if row.isnull().sum() > 5:
            data.drop(index, inplace=True)
            droped_row_ind.append(index)
            continue
        ave_now = row.dropna().mean()
    data.reset_index(drop=True, inplace=True)
    # 补全nan值
    data.interpolate(method="linear", axis=1, inplace=True)
    data.fillna(method="backfill", axis=1, inplace=True)
    # 计算协方差矩阵与标准差
    data_cov = data.T.cov()
    data_std = data.std(axis=1)
    # 转为numpy矩阵,并取标准差矩阵的逆
    data_mat = np.transpose(data.values)
    cov_mat = data_cov.values
    std_inv = np.matrix(data_std).I
    # 计算R
    r_pre = np.dot(np.transpose(std_inv), cov_mat)
    r = np.dot(r_pre, std_inv)
    # 标准化矩阵
    # 计算数据
    mean_list = data.mean(axis=1)
    mean_table = np.tile(mean_list, (data_mat.shape[0], 1))
    std_list = np.transpose(data_std)
    std_table = np.tile(std_list, (data_mat.shape[0], 1))
    # 数据标准化
    data_std_mat = (data_mat - mean_table) / std_table
    print("\n---政府数据读取与标准化完成")
    # 返回值：原始数据array,标准化数据array,r
    return data_mat, data_std_mat


def getBussAve(ser_name=["Chongqing_USD"]):
    data = getBussinessData()
    ser_name_list = ["Date", "Date as Text", "Domestic Currency (CNY).6", "Chongqing_USD", "Chongqing_EUR"]
    # 读取ser_name_list中包括的列
    data = getSelected(data, ser_name_list)
    buss_data = data
    # 读取特定年份的数据
    data["Date"] = pd.to_datetime(data["Date"])
    data.set_index("Date", inplace=True)
    # 处理特定年份的数据
    data_list = {}
    ave_list = []
    start_year = data.index.min().year
    end_year = 2019
    for ind in range(start_year, end_year + 1):
        temp_df = data.loc[str(ind)]
        # 存入字典
        temp_dic = {ind: temp_df}
        data_list.update(temp_dic)
        # 计算平均值
        buss_now_df = getSelected(temp_df, ser_name)
        buss_now_df.replace("#VALUE!", None, inplace=True)
        buss_now_arr = buss_now_df.dropna(how="any").values.astype("float")
        if (buss_now_arr.size == 0):
            ave_now = 0
        else:
            ave_now = np.mean(buss_now_arr)
        ave_list.append(ave_now)
    ave_list = np.array(ave_list)
    ave_std = (ave_list - ave_list.mean()) / np.std(ave_list)
    # 返回平均值
    return ave_list, ave_std


def getClearBuss(ser_name=["Chongqing_USD"]):
    data = getBussinessData()
    data = getSelected(data, ser_name)
    data.reset_index(drop=True, inplace=True)
    # 截取最后1000个点
    data_cut = data.loc[len(data) - 1000:len(data)]
    data_cut.reset_index(drop=True, inplace=True)
    #
    data_cut = pd.to_numeric(data_cut["Chongqing_USD"], errors='coerce')
    data_cut.interpolate(method="linear", inplace=True)
    data_cut.dropna(how="any",inplace=True)
    data_cut_mat = np.array(pd.DataFrame(data_cut))
    return data_cut_mat


def getSelected(data_ori, ser_name_list):
    data = data_ori.copy();
    # 读取ser_name_list中包括的列
    for index, item in data.iteritems():
        if (index not in ser_name_list):
            data.drop(index, axis=1, inplace=True)
    return data
