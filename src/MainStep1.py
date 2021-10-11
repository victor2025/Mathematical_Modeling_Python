import readRes

if __name__ == '__main__':
    data_buss = readRes.getBusinessData("data_world")
    data_gov,data_gov_std,_ = readRes.getGovData("data_gov")


    print("done")
