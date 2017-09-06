import datetime
import os
import numpy as np
path = "C:\\Users\\NLSDE\\Desktop\\gz\\"
timeInterval = ["zao", "zhong", "wan"]
def initVariable():
    timeMin_zao = []
    timeMin_zhong = []
    timeMin_wan = []
    timeDay = []
    linkid = []
    timeMin = {}
    #day
    startDay = datetime.datetime.strptime("2016-03-01", "%Y-%m-%d")
    for i in range(0,92,1):
        endDay = startDay + datetime.timedelta(days=i)
        timeDay.append(datetime.datetime.strftime(endDay,"%Y-%m-%d"))
    startDay = datetime.datetime.strptime("2016-07-01", "%Y-%m-%d")
    for i in range(0, 31, 1):
        endDay = startDay + datetime.timedelta(days=i)
        timeDay.append(datetime.datetime.strftime(endDay, "%Y-%m-%d"))
    startDay = datetime.datetime.strptime("2017-03-01", "%Y-%m-%d")
    for i in range(0, 153, 1):
        endDay = startDay + datetime.timedelta(days=i)
        timeDay.append(datetime.datetime.strftime(endDay, "%Y-%m-%d"))
    #min
    startTime = datetime.datetime.strptime("06:00:00", "%H:%M:%S")
    for i in range(0, 180, 2):
        endTime = startTime + datetime.timedelta(minutes=i)
        timeMin_zao.append(datetime.datetime.strftime(endTime, "%H:%M:%S"))
    startTime = datetime.datetime.strptime("13:00:00", "%H:%M:%S")
    for i in range(0, 180, 2):
        endTime = startTime + datetime.timedelta(minutes=i)
        timeMin_zhong.append(datetime.datetime.strftime(endTime, "%H:%M:%S"))
    startTime = datetime.datetime.strptime("16:00:00", "%H:%M:%S")
    for i in range(0, 180, 2):
        endTime = startTime + datetime.timedelta(minutes=i)
        timeMin_wan.append(datetime.datetime.strftime(endTime, "%H:%M:%S"))
    timeMin["zao"] = timeMin_zao
    timeMin["zhong"] = timeMin_zhong
    timeMin["wan"] = timeMin_wan
    #link
    with open(path + "gy_contest_link_info.txt") as f:
        f.readline()
        lines = f.readlines()
        for line in lines:
            attrs = line.split(";")
            linkid.append(attrs[0])
    # print(timeDay)
    return timeMin,linkid,timeDay,linkid
def readData(infile,tm):
    timeMin, linkid, timeDay, linkid = initVariable()
    data_dir = {}
    for i in linkid:
        for j in timeDay:
                data_dir[(i,j)] = []
    with open(path+infile) as f:
            f.readline()#skip the header
            all = f.readlines()
            for i in range(len(all)):
                values = all[i].split(";")
                idx_linkid = values[0]
                idx_timeDay = values[1]
                idx_timeMin = values[2].split(" ")[1].split(",")[0]
                volume = float(values[3].replace("\n",""))
                if idx_timeMin in timeMin[tm] and idx_linkid in linkid:
                    data_dir[(idx_linkid,idx_timeDay)].append((idx_timeMin,volume))
    return linkid,timeMin[tm],data_dir
def fileTotesnor_first(linkid,timeMin,data_dir,tm):
    outTensor ={}
    for i in linkid:
        outTensor[i]=[]
    for i in data_dir:
        tempList = []
        tempMin=[]
        for j in data_dir[i]:
            tempMin.append(j[0])
        for k in list(set(timeMin)-set(tempMin)):#补全缺失时间段的数据为0
            data_dir[i].append((k,0))
        sortedList = sorted(data_dir[i])
        for k in sortedList:
            tempList.append(k[1])
        outTensor[i[0]].append((i[1],tempList))
    if not os.path.exists(path+"tensorDataAll\\"):
        os.mkdir(path+"tensorDataAll\\")
    for i in outTensor:
        outputPath = path+"tensorDataAll\\"+str(i)
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        sortedList = sorted(outTensor[i])
        with open(outputPath+"\\tensor"+tm+".csv","w") as f:
            for k in sortedList:
                f.write(",".join(map(str, k[1])) + "\n")
def fillupFirst(tensorpath,interval):
    files = os.listdir(tensorpath)
    #填补成tensor_fill文件
    for i in files:
        with open(tensorpath+i+ "\\tensor_fill_"+interval+".csv","w") as f1:
            with open(tensorpath+i+ "\\tensor"+interval+".csv") as f2:
                all = f2.readlines()
                for j in range(len(all)):
                    str_list = list(map(float,all[j].replace("\n","").split(",")))
                    for k in range(1,len(str_list)-1):
                        if str_list[k]==0:
                            if 0 in [str_list[k - 1], str_list[k + 1]]:#若有0取最大的
                                str_list[k] = max(str_list[k - 1], str_list[k + 1])
                            else:#若没0取最小的
                                str_list[k] = min(str_list[k - 1], str_list[k + 1])  # 相邻两个元素取最小
                    if str_list[len(str_list)-1]==0:
                        str_list[len(str_list) - 1] = str_list[len(str_list) - 2]
                    for m in range(len(str_list)-2,0,-1):
                        if str_list[m]==0:
                            if 0 in [str_list[m - 1], str_list[m + 1]]:
                                str_list[m] = max(str_list[m - 1], str_list[m + 1])
                            else:
                                str_list[m] = min(str_list[m - 1], str_list[m + 1])  # 相邻两个元素取最小
                    if str_list[0]==0:
                        str_list[0] = str_list[1]
                    f1.write(",".join(list(map(str,str_list)))+"\n")
def fillupSecond(tensorpath,interval):
    files = os.listdir(tensorpath)
    for i in files:
        global_min = 0
        isFirst = True
        tensor_fill = np.loadtxt(tensorpath+i+ "\\tensor_fill_"+interval+".csv", delimiter=',')
        for j in range(tensor_fill.shape[0]):
            temp = findMinExceptZero(tensor_fill[j,:])
            if isFirst and temp !=0:
                global_min = temp
                isFirst = False
            elif temp<global_min and temp !=0:
                global_min = temp
        for row in range(tensor_fill.shape[0]):
            for col in range(tensor_fill.shape[1]):
                if tensor_fill[row][col] ==0:
                    tensor_fill[row][col] = global_min
        os.remove(tensorpath+i+ "\\tensor_fill_"+interval+".csv")
        np.savetxt(tensorpath+i+ "\\tensor_fill_"+interval+".csv",tensor_fill,fmt="%.4f",delimiter=',')
#找出数组中最小的非0元素
def findMinExceptZero(a):
    tmp = sorted(a)
    for i in tmp:
        if i != 0:
            return i
    return 0
if __name__ == '__main__':
    initVariable()
    for tm in timeInterval:
        linkid, timeMin, data_dir = readData("allTrainData.csv",tm)
        fileTotesnor_first(linkid,timeMin,data_dir,tm)
        tensorpath = path+"tensorDataAll\\"
        fillupFirst(tensorpath,tm)
        fillupSecond(tensorpath,tm)