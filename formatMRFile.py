import os
path = "C:\\Users\\NLSDE\\Desktop\\icdm\\final_tables\\"
#将MR生成的文件转化成提交需要的格式
def changeFormat(input_file):
    for i in range(len(input_file)):
        with open(path+"temp.txt","w") as f1:
            with open(path+input_file[i]+".txt") as f:
                lines = f.readlines()
                for line in lines:
                    attrs = line.replace("\n","").replace("\"","").split(",")
                    f1.write(attrs[0]+"#"+attrs[1]+"#"+attrs[2]+","+attrs[3]+"#"+attrs[4]+"\n")
            f.close()
        f1.close()
        os.remove(path+input_file[i]+".txt")
        os.rename(path+"temp.txt",path+input_file[i]+".txt")
#主要是分为seg1和seg2
def splitSeg(input_file):
    for i in range(len(input_file)):
        with open(path+input_file[i]+"_seg1.txt","w") as f1:
            with open(path+input_file[i]+".txt") as f:
                lines = f.readlines()
                for line in lines:
                    attrs = line.split("#")
                    if attrs[1] <='2017-07-15':
                        f1.write(line)

if __name__ == '__main__':
    # input_file = ["bpv2_zao","bpv2_zhong","bpv2_wan"]
    input_file = ["knn_link_zao909","knn_link_zhong909","knn_link_wan909"]
    changeFormat(input_file)
    splitSeg(input_file)

