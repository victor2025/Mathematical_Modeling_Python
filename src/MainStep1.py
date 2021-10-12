import readRes
import corrCompare

if __name__ == '__main__':
    data_gov,data_gov_std = readRes.getGovData()
    data_buss_ave,data_buss_std = readRes.getBussAve()
    # 主成分回归
    beta_hat = corrCompare.pcaCorr(data_gov_std,data_buss_std)

    print("done")
