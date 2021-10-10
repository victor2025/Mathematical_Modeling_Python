# 读取数据并进行数据预处理
import pandas as pd

# 初始设定
base_dir = "..//res//"
file_name = "data_cn"
file_path = base_dir+file_name+".csv"
ser_name_list = ["Shenzhen_USD","Shenzhen_EUR","Shanghai_USD","Shanghai_EUR","Beijing_USD","Beijing_EUR","Guangdong_USD","Guangdong_EUR","Tianjin_USD","Tianjin_EUR","Hubei_USD","Hubei_EUR","Chongqing_USD","Chongqing_EUR","Fujian_USD"]
# 预处理函数
def preProcess(file_path):
    # 读取csv数据,去除最小有用数据
    data = pd.read_csv(file_path,sep=";")
    data=data.dropna(axis=1,how="all")

    # 去除无用行
    ind_min = data._ixs(1,1).__len__()
    for index,item in data.iteritems():
        if(index in ser_name_list):
            item_null = item.isnull()
            for ind_row in range(0,item.__len__()-1):
                if(not item_null[ind_row]):
                    break
            ind_min = min(ind_row,ind_min)
    data = data.drop(data.index[0:ind_min])
    return data


# 保存为xlsx文件
data = preProcess(file_path)
data.to_excel(base_dir+file_name+".xlsx",index=False)
print("Conversion completed")