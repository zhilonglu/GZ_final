#合并几个文件成一个文件
path = "C:\\Users\\NLSDE\\Desktop\\icdm\\final_tables\\"

#根据不同的比例集成最终结果
def weightedEnsemble(a):
    if len(a)==2:
        return a[0]*0.1+a[1]*0.9
    elif len(a)==3:
        return a[0]*0.1+a[1]*0.05+a[2]*0.85
    elif len(a)==4:
        return a[0]*0.9+a[1]*0.05+a[2]*0.05+a[3]*0.05
#集成所有输入，并得出最终的一个输出
def integer(files,outputfile):
    result_dict=[]
    for idx in range(len(files)):
        result_dict.append({})
        with open(path+files[idx]) as f1:
            all = f1.readlines()
            for i in range(len(all)):
                values = all[i].replace("\n","").split("#")
                result_dict[idx][(values[0],values[1],values[2])] = float(values[3])
    with open(path+outputfile,"w") as f4:
        for i in result_dict[0]:
            tempList = []
            for j in range(len(files)):
                tempList.append(result_dict[j][i])
            f4.write("#".join(i)+"#"+str(weightedEnsemble(tempList))+"\n")
outputfile = ["zhu_zao909.txt","zhu_zhong909.txt","zhu_wan909.txt"]
knn_input = ["knn_link_zao909_seg1.txt","knn_link_zhong909_seg1.txt","knn_link_wan909_seg1.txt"]
int_input = ["int_zao.txt","int_zhong.txt","int_wan.txt"]
bp_input = ["bpv2_zao_seg1.txt","bpv2_zhong_seg1.txt","bpv2_wan_seg1.txt"]
for i in range(3):
    integer([knn_input[i],bp_input[i],int_input[i]],outputfile[i])


