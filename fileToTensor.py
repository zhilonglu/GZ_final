import datetime
import os
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
    startDay = datetime.datetime.strptime("2016-07-01", "%Y-%m-%d")
    for i in range(0,31,1):
        endDay = startDay + datetime.timedelta(days=i)
        timeDay.append(datetime.datetime.strftime(endDay,"%Y-%m-%d"))
    startDay = datetime.datetime.strptime("2017-04-01", "%Y-%m-%d")
    for i in range(0, 122, 1):
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
    print(timeDay)
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
    if not os.path.exists(path+"tensorData1\\"):
        os.mkdir(path+"tensorData1\\")
    for i in outTensor:
        outputPath = path+"tensorData1\\"+str(i)
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        sortedList = sorted(outTensor[i])
        with open(outputPath+"\\tensor"+tm+".csv","w") as f:
            for k in sortedList:
                f.write(",".join(map(str, k[1])) + "\n")
if __name__ == '__main__':
    initVariable()
    # for tm in timeInterval:
    #     linkid, timeMin, data_dir = readData("quaterfinal_gy_cmp_training_traveltime.txt",tm)
    #     fileTotesnor_first(linkid,timeMin,data_dir,tm)