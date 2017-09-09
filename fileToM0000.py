def writeToM():
    fl = ["BPNN_v2AliyunMR","KNN_AliyunMR","KNN_final_AliyunMR","KNN_v2_AliyunMR"]
    infile_alldata = ["AllDatatensor_fill_zao_all","AllDatatensor_fill_zhong_all","AllDatatensor_fill_wan_all",
                      "AllDatatensor_fill_zao_fe_all", "AllDatatensor_fill_zhong_fe_all", "AllDatatensor_fill_wan_fe_all",
                      "AllDatatensor_fill_zao_link_all", "AllDatatensor_fill_zhong_link_all", "AllDatatensor_fill_wan_link_all"]
    infile_data1 = ["tensor_fill_zao_all","tensor_fill_zhong_all","tensor_fill_wan_all",
                    "tensor_fill_zao_fe_all", "tensor_fill_zhong_fe_all", "tensor_fill_wan_fe_all",
                    "tensor_fill_zao_link_all", "tensor_fill_zhong_link_all", "tensor_fill_wan_link_all"]
    path = "C:\\Users\\NLSDE\\Workspaces\\MyEclipse 2015\\lzl\\KNN_v2_AliyunMR\\warehouse\\buaa_prj\\__tables__\\wc_in\\M000001"
    inpath = "C:\\Users\\NLSDE\\Desktop\\gz\\"
    with open(path,"w") as f1:
        with open(inpath+"AllDatatensor_fill_zao_fe_all.csv") as f:
            lines = f.readlines()
            for line in lines:
                f1.write(line)
def writeFromR():
    inpath = "C:\\Users\\NLSDE\\Workspaces\\MyEclipse 2015\\lzl\\KNN_v2_AliyunMR\\warehouse\\buaa_prj\\__tables__\\wc_out\\R_000000"
    outpath = "C:\\Users\\NLSDE\\Desktop\\icdm\\final_tables\\"
    file = ["knn_link_zao.txt","knn_link_zhong.txt","knn_link_wan.txt"]
    with open(outpath+"knn_link_zao909.txt","w") as f1:
        with open(inpath) as f:
            lines = f.readlines()
            for line in lines:
                f1.write(line)

if __name__ == '__main__':
    # writeToM()
    writeFromR()