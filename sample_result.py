import datetime
import json
import os
datapath = "C:\\Users\\NLSDE\\Desktop\\gz\\"
linkid = []
with open(datapath+"gy_contest_link_info.txt") as f:
    f.readline()
    lines = f.readlines()
    for line in lines:
        attrs = line.split(";")
        linkid.append(attrs[0])
timeDay=[]
time_interval = ["08:00:00","15:00:00","18:00:00"]
day_during = ['zao','zhong','wan']
startDate = "2017-06-01"
days = 30
startDay = datetime.datetime.strptime(startDate,"%Y-%m-%d")
for i in range(0,int(days),1):
    endDay = startDay + datetime.timedelta(days=i)
    timeDay.append(datetime.datetime.strftime(endDay,"%Y-%m-%d"))
print(timeDay)
# for s in range(len(time_interval)):
#     timeMin = []
#     timeId = []
#     startTime = datetime.datetime.strptime(time_interval[s],"%H:%M:%S")
#     for i in range(0,62,2):
#         endTime = startTime + datetime.timedelta(minutes=i)
#         timeMin.append(datetime.datetime.strftime(endTime,"%H:%M:%S"))
#     for i in range(len(timeDay)):
#         for j in range(len(timeMin)-1):
#             timeId.append(timeDay[i]+"#"+"["+timeDay[i]+" "+timeMin[j]+","+timeDay[i]+" "+timeMin[j+1]+")")
#     with open(datapath+day_during[s]+".txt","w") as f:
#         for link in linkid:
#             for tm in timeId:
#                 f.write(link+"#"+tm+"#"+str(0)+"\n")
