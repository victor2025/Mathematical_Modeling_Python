import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Activation

def load_data(data_arr, sequence_length=20, split=0.8):
    data_all = data_arr.astype(float)
    scaler = MinMaxScaler()
    data_all = scaler.fit_transform(data_all)
    data = []
    print("len(data_all)={}".format(len(data_all)))
    for i in range(len(data_all) - sequence_length - 1):
        print("i={}, (i + sequence_length + 1)={}".format(i, i + sequence_length + 1))
        data.append(data_all[i: i + sequence_length + 1])
    reshaped_data = np.array(data).astype('float64')
    # 对x进行统一归一化，而y则不归一化
    #行全部取，11列中除了最后一列不取
    x = reshaped_data[:, :-1]
    #行全部取，11列中只取最后一列
    y = reshaped_data[:, -1]
    #分割数
    split_boundary = int(reshaped_data.shape[0] * split)
    train_x = x
    # test_x = x[split_boundary:]

    train_y = y
    # test_y = y[split_boundary:]
    print("train_x={}, train_y={}".format(train_x.shape, train_y.shape))
    return train_x, train_y, scaler, data_all

def procData(data_arr, sequence_length=20):
    data_all = data_arr.astype(float)
    scaler = MinMaxScaler()
    data_all = scaler.fit_transform(data_all)
    data = []
    print("len(data_all)={}".format(len(data_all)))
    for i in range(len(data_all) - sequence_length - 1):
        print("i={}, (i + sequence_length + 1)={}".format(i, i + sequence_length + 1))
        data.append(data_all[i: i + sequence_length + 1])
    reshaped_data = np.array(data).astype('float64')
    # 对x进行统一归一化，而y则不归一化
    # 行全部取，11列中除了最后一列不取
    x = reshaped_data[:, :-1]
    # 行全部取，11列中只取最后一列
    y = reshaped_data[:, -1]
    # 分割数
    pred_x = x
    return pred_x

def build_model():
    # input_dim是输入的train_x的最后一个维度，train_x的维度为(n_samples, time_steps, input_dim)
    model = Sequential()
    # model.add(LSTM(input_dim=1, output_dim=50, return_sequences=True))
    #2.2.2 keras
    model.add(LSTM(input_shape=(None, 1), units=100, return_sequences=False))
    print(model.layers)
    # model.add(LSTM(units=100, return_sequences=False))
    # model.add(Dense(output_dim=1))

    model.add(Dense(units=1))
    model.add(Activation('linear'))

    model.compile(loss='mse', optimizer='rmsprop')
    return model


def train_model(train_x, train_y):
    model = build_model()
    # model.fit(train_x, train_y, batch_size=512, nb_epoch=30, validation_split=0.1)
    model.fit(train_x, train_y, batch_size=512, epochs=30, validation_split=0.1)
    print("Model trained")
    return model

def predMain(model,data_all,x_len=400):
    data_now = data_all[-x_len:]
    pred_list = []
    pred_x=procData(data_now)
    pred_y = model.predict(pred_x)
    pred_y = np.reshape(pred_y, (pred_y.size,))
    predict = pred_y
    return predict



def lstmMain(data_arr):
    train_x, train_y, scaler, data_all = load_data(data_arr)
    train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))
    # test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))
    print("train_x.shape={}".format(train_x.shape))
    model = train_model(train_x, train_y)
    predict_y = predMain(model,data_all)

    #返回原来的对应的预测数值
    predict_y = scaler.inverse_transform([[i] for i in predict_y])
    data_all = scaler.inverse_transform(data_all)
    # 作图
    data_ori_len = 100
    fig1 = plt.figure(1)
    plt.plot(range(-data_ori_len,0),data_all[-data_ori_len:],'r-')
    plt.plot(range(1,len(predict_y)+1),predict_y,'g:')
    plt.legend(['true','predict'])
    plt.title("Chongqing_USD Predict")
    plt.xlabel("Date/day")
    plt.ylabel("Price/USD")
    plt.show()