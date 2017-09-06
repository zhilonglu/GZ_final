import os
import datetime
import json


def loadPath():
    # with open("config_zao.json") as f:
    with open("config_zhong.json") as f:
    # with open("config_wan.json") as f:
        config=json.loads(f.read())
        return config["datapath"],config["sharepath"],config["rootpath"],config["tensorfile"],config["startdate"],config["starthour"],config["days"]

datapath,sharepath,rootpath,tensorfile,startdate,starthour,days=loadPath()




timeId=[]
timeDay=[]
timeMin=[]
startDay = datetime.datetime.strptime(startdate,"%Y-%m-%d")
startTime = datetime.datetime.strptime(starthour,"%H:%M:%S")
for i in range(0,days,1):
    endDay = startDay + datetime.timedelta(days=i)
    timeDay.append(datetime.datetime.strftime(endDay,"%Y-%m-%d"))
for i in range(0,62,2):
    endTime = startTime + datetime.timedelta(minutes=i)
    timeMin.append(datetime.datetime.strftime(endTime,"%H:%M:%S"))
for i in range(len(timeDay)):
    for j in range(len(timeMin)-1):
        timeId.append("["+timeDay[i]+" "+timeMin[j]+","+timeDay[i]+" "+timeMin[j+1]+")")


with open(datapath+"svr_zhong_mean.txt", "w") as f1:
        files = os.listdir(sharepath)
        print(",".join(map(lambda _:"\""+_+"\"",files)))
        for i in files:
            files_id = os.listdir(sharepath+i)
            for file in files_id:
                if file=="outputsmean_zao.csv":
                    with open(sharepath+i+"\\"+file) as f2:
                        all = f2.readlines()
                        for j in range(len(all)):
                            value = float(all[j].replace("\n",""))
                            if value<0:
                                value=0
                            f1.write(i+"#"+timeId[j].split(" ")[0][1:]+"#"+timeId[j]+"#"+str(value)+"\n")


with open(datapath+"svr_zhong_median.txt", "w") as f1:
        files = os.listdir(sharepath)
        for i in files:
            files_id = os.listdir(sharepath+i)
            for file in files_id:
                if file=="outputsmedian_zhong.csv":
                    with open(sharepath+i+"\\"+file) as f2:
                        all = f2.readlines()
                        for j in range(len(all)):
                            value = float(all[j].replace("\n",""))
                            if value<0:
                                value=0
                            f1.write(i+"#"+timeId[j].split(" ")[0][1:]+"#"+timeId[j]+"#"+str(value)+"\n")
