import pandas as pd
import numpy as np
import readRes

data = readRes.getBussinessData()
ser_name_list = ["Date","Date as Text","Domestic Currency (CNY).6","Chongqing_USD","Chongqing_EUR"]

# 读取ser_name_list中包括的列
data = readRes.getSelected(data,ser_name_list)
# 读取特定年份的数据
data["Date"] = pd.to_datetime(data["Date"])
data.set_index("Date",inplace=True)
# 处理特定年份的数据
data_list = {}
ave_list = []
start_year = data.index.min().year
end_year = data.index.max().year
for ind in range(start_year,end_year+1):
    temp_df = data.loc[str(ind)]
    # 存入字典
    temp_dic = {ind:temp_df}
    data_list.update(temp_dic)
    # 计算平均值
    ser_name = ["Chongqing_USD"]
    buss_now_df = readRes.getSelected(temp_df,ser_name)
    buss_now_df.replace("#VALUE!",None,inplace=True)
    buss_now_arr = buss_now_df.dropna(how="any").values.astype("float")
    if(buss_now_arr.size==0):
        ave_now = 0
    else:
        ave_now = np.mean(buss_now_arr)
    ave_list.append(ave_now)

print("done")
