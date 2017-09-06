#
#代码主要是在原始的tensor上加上部分特征，尝试效果如何
#加上的特征dayofweek三个特征
#
import datetime
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
# path = "C:\\Users\\NLSDE\\Desktop\\gz\\tensorDataAll\\"
path = "C:\\Users\\NLSDE\\Desktop\\gz\\tensorData1\\"
rootpath = "C:\\Users\\NLSDE\\Desktop\\gz\\"
timeInterval = ['zao','zhong','wan']
timeDay = []
dayofweek = []
#day
# startDay = datetime.datetime.strptime("2016-03-01", "%Y-%m-%d")
# for i in range(0,92,1):
#     endDay = startDay + datetime.timedelta(days=i)
#     timeDay.append(datetime.datetime.strftime(endDay,"%Y-%m-%d"))
startDay = datetime.datetime.strptime("2016-07-01", "%Y-%m-%d")
for i in range(0, 31, 1):
    endDay = startDay + datetime.timedelta(days=i)
    timeDay.append(datetime.datetime.strftime(endDay, "%Y-%m-%d"))
startDay = datetime.datetime.strptime("2017-04-01", "%Y-%m-%d")
for i in range(0, 122, 1):
    endDay = startDay + datetime.timedelta(days=i)
    timeDay.append(datetime.datetime.strftime(endDay, "%Y-%m-%d"))
#day of week编码
for i in range(len(timeDay)):
    dayofweek.append(datetime.datetime.strptime(timeDay[i], "%Y-%m-%d").weekday() + 1)
# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(dayofweek)
# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
#以下是针对单独link训练数据增加特征的代码
def addFeature():
    files = os.listdir(path)
    for tm in timeInterval:
        for file in files:
            templink_id = []
            for i in range(onehot_encoded.shape[0]):
                templink_id.append(file)
            tensor = np.loadtxt(path+file+"\\tensor_fill_"+tm+".csv",delimiter=",")
            scaler = preprocessing.StandardScaler().fit(tensor[:,:60])
            trans_x = scaler.transform(tensor[:,:60])#进行标准化后的x
            trans_y = tensor[:,60:]
            link_id = np.array(templink_id).reshape(-1,1)
            timeDay_id = np.array(timeDay).reshape(-1,1)
            newtensor_link = np.concatenate([link_id,timeDay_id,trans_x,trans_y],axis=1)
            np.savetxt(path + file + "\\tensor_fill_" + tm + "_link.csv", newtensor_link, fmt="%s", delimiter=',')
            newtensor = np.concatenate([link_id,timeDay_id,onehot_encoded,trans_x,trans_y],axis=1)
            np.savetxt(path+file+"\\tensor_fill_"+tm+"_fe.csv",newtensor,fmt="%s",delimiter=',')
def mergrAllFile():
    files = os.listdir(path)
    for tm in timeInterval:
        with open(rootpath + "\\tensor_fill_" + tm + "_link_all.csv","w") as f1:
            for file in files:
                with open(path + file + "\\tensor_fill_" + tm + "_link.csv") as f:
                    lines = f.readlines()
                    for line in lines:
                        f1.write(line)
                f.close()
        with open(rootpath + "\\tensor_fill_" + tm + "_fe_all.csv","w") as f2:
            for file in files:
                with open(path + file + "\\tensor_fill_" + tm + "_fe.csv") as f:
                    lines = f.readlines()
                    for line in lines:
                        f2.write(line)
                f.close()
if __name__ == '__main__':
    mergrAllFile()