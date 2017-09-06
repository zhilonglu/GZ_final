
path = "C:\\Users\\NLSDE\\Desktop\\gz\\"
with open(path+"allTrainData.csv","w") as f:
    with open(path+"gy_contest_link_traveltime_training_data.txt") as f1:#第一阶段数据
        f1.readline()
        lines = f1.readlines()
        for line in lines:
            if "2016-06" not in line:#预测的时间段不考虑在范围内
                f.write(line)
        f1.close()
    with open(path+"gy_contest_traveltime_training_data_second.txt") as f1:#第二阶段数据
        f1.readline()
        lines = f1.readlines()
        for line in lines:
            if "2017-03" in line:#
                f.write(line)
        f1.close()
    with open(path + "quaterfinal_gy_cmp_training_traveltime.txt") as f1:#决赛阶段数据
        f1.readline()
        lines = f1.readlines()
        for line in lines:
            f.write(line)
        f1.close()