import pandas as pd
import numpy as np
import readRes

data = readRes.getBusinessData()
ser_name_list = ["Date","Date as Text","Domestic Currency (CNY).6","Chongqing_USD","Chongqing_EUR"]

# 读取ser_name_list中包括的列
data = readRes.getSelected(data,ser_name_list)


print("done")
