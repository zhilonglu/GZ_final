import datetime
import os
path = "C:\\Users\\NLSDE\\Desktop\\gz\\"
dirName = "C:\\Users\\NLSDE\\Desktop\\gz\\html\\"
timeMin_zao =[]
timeDay_zao = []
timeDay_zao_dict = {}
timeId_zao = []
timeId_zao_dict = {}
startTime = datetime.datetime.strptime("08:00:00", "%H:%M:%S")
for i in range(0, 62, 2):
    endTime = startTime + datetime.timedelta(minutes=i)
    timeMin_zao.append(datetime.datetime.strftime(endTime, "%H:%M:%S"))
startDay = datetime.datetime.strptime("2017-06-01", "%Y-%m-%d")
for i in range(0, 30, 1):
    endDay = startDay + datetime.timedelta(days=i)
    timeDay_zao.append(datetime.datetime.strftime(endDay, "%Y-%m-%d"))
for i in range(len(timeDay_zao)):
    timeDay_zao_dict[timeDay_zao[i]] = i
for i in range(len(timeDay_zao)):
    for j in range(len(timeMin_zao)-1):
        timeId_zao.append("["+timeDay_zao[i]+" "+timeMin_zao[j]+","+timeDay_zao[i]+" "+timeMin_zao[j+1]+")")
for i in range(len(timeId_zao)):
    timeId_zao_dict[timeId_zao[i]] = i
YDict = {}
with open(path+"sv_TrueYFill_zao.txt") as f:
    f_all=f.read()
    lines=f_all.split("\n")
    for line in lines:
        ls=line.split("#")
        if(len(ls)==4):
            YDict[(ls[0],ls[1],ls[2])]=float(ls[3])
Y_validDict={}
with open(path+"sv_rnnv4_zao.txt") as f:
    f_all=f.read()
    lines=f_all.split("\n")
    for line in lines:
        ls=line.split("#")
        if(len(ls)==4):
            Y_validDict[(ls[0], ls[1], ls[2])] = float(ls[3])
link_mape = {}
with open(path+"all_mape.csv","w") as f:
    for key in YDict:
        mape = round(abs(YDict[key]-Y_validDict[key])/YDict[key],3)
        f.write(",".join(map(str,key))+str(mape)+"\n")
        link = key[0]
        day = key[1]
        row = timeDay_zao_dict[day]
        time_interval = key[2]
        col = timeId_zao_dict[time_interval]%30
        if link not in link_mape:
            link_mape[link] = []
        temp_data = []
        temp_data.append(row)
        temp_data.append(col)
        temp_data.append(mape)
        link_mape[link].append(temp_data)
def writeLink():
    with open(path+"link_value.csv","w") as f:
        for key in link_mape:
            values = link_mape[key]
            f.write(key+":")
            for v in values:
                f.write("["+",".join(map(str,v))+"],")
            f.write("\n")
def readMape():
    writeLink()
    html_dict = {}
    with open(path + "link_value.csv") as f:
        lines = f.readlines()
        for line in lines:
            link = line.split(":")[0]
            value = line.split(":")[1][0:-2]
            html_dict[link] = value
    return html_dict
def changeFile():#修改文件的后缀
    li=os.listdir(dirName)
    for filename in li:
        newname = filename
        newname = newname.split(".")
        if newname[-1]=="txt":
            newname[-1]="html"
            newname = ".".join(newname)
            filename = dirName+filename
            newname = dirName+newname
            os.rename(filename,newname)
def writeHTML():
    html_dict = readMape()
    for link in html_dict:
        with open(dirName + link+".txt", "w") as f1:
            with open(path+"sample.txt") as f2:
                all = f2.readlines()
                for line in all:
                    if "var data" in line:
                        line = "var data="+"["+html_dict[link]+"]"
                    elif "text:" in line:
                        line = "text:"+"'"+link+"',"
                    f1.write(line+"\n")
if __name__ == '__main__':
    writeHTML()
    changeFile()