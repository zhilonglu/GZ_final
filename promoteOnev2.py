'''
Created on 2017-9-5

@author: Administrator
'''
from datetime import datetime
import os
import numpy as np
import tensorflow as tf
import gc
from sklearn.model_selection import KFold
import json
import threading
from time import ctime,sleep
tf.set_random_seed(1234)
def listmap(o,p):
    return list(map(o,p))

def loadPath():
    with open("consv_zhong_all.json") as f: #修改1
        config=json.loads(f.read())
        return config["datapath"],config["sharepath"],config["rootpath"],config["tensorfile"],config["startdate"],config["days"]

datapath,sharepath,rootpath,tensorfile,startdate,days=loadPath()

print(loadPath())

def build_nnnb(hiddennum,inputnum,outputnum):
    x=tf.placeholder(tf.float32, [None,inputnum])
    yTrue=tf.placeholder(tf.float32,[None,outputnum])
    keep_prob=tf.placeholder(tf.float32)
    nodenums=[inputnum]+hiddennum+[outputnum]
    hiddens=[]
    drops=[x]
    Ws=[]
    for i in range(len(nodenums)-1):
        Wi=tf.Variable(tf.ones([nodenums[i],nodenums[i+1]]))
#         if(i==len(nodenums)-2):
#             Wi=tf.Variable(tf.ones([nodenums[i],nodenums[i+1]]))
#         else:
#             Wi=tf.Variable(tf.truncated_normal([nodenums[i],nodenums[i+1]],mean=0, stddev=0.1))
        Wi=tf.maximum(Wi, 0)
        #Wi=tf.minimum(Wi, 1)
        Ws.append(Wi)
        tf.add_to_collection(tf.GraphKeys.WEIGHTS,Wi)
        #bi= tf.Variable(tf.ones(nodenums[i+1]))
        if i<len(nodenums)-2:
            print("softplus")
            #hiddeni = tf.nn.relu(tf.add(tf.matmul(drops[i],Wi),bi))
            hiddeni = tf.nn.softplus(tf.matmul(drops[i],Wi))
            hiddens.append(hiddeni)
            dropi=tf.nn.dropout(hiddeni,keep_prob)
            drops.append(dropi)
        else:
            #y=tf.add(tf.matmul(drops[i],Wi),bi)
            y=tf.matmul(drops[i],Wi)
    lossfun=tf.reduce_mean(tf.abs(tf.subtract(y/yTrue,1)))
    return (x,y,yTrue,Ws,keep_prob,lossfun)

def splitData(tensor,n_output,n_pred):
    n_known=tensor.shape[0]-n_pred
    n_input=tensor.shape[1]-n_output
    knownX = tensor[0: n_known, 0: n_input]
    knownY = tensor[0: n_known, n_input: n_input + n_output]
    preX = tensor[n_known: n_known+n_pred, 0: n_input]
    return (knownX,knownY,preX)

def train_nnnb(taskname,tensors,nnnb,times,keep,lr,outputs):
    npx,npx_test,npy,npy_test,preX=tensors
    x,y,yTrue,Ws,keep_prob,lossfun=nnnb
    regularizer=tf.contrib.layers.l2_regularizer(0.1)
    l2_loss=tf.contrib.layers.apply_regularization(regularizer)
    train_step=tf.train.AdamOptimizer(learning_rate=lr).minimize(lossfun+l2_loss)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        #lostsumloss=10000
        #lossup=0
        for i in range(times):
            sess.run(train_step,feed_dict={x:npx,yTrue:npy,keep_prob:keep})
            #print(sess.run(Ws,feed_dict={x:npx,yTrue:npy,keep_prob:keep}))
            loss1=sess.run(lossfun,feed_dict={x:npx,yTrue:npy,keep_prob:1})
            loss2=sess.run(lossfun,feed_dict={x:npx_test,yTrue:npy_test,keep_prob:1})
            #if loss1+loss2>lostsumloss:
            #    lossup+=1
            #if lossup>1500:
            #    break
            #lostsumloss=loss1+loss2
        print(taskname,":",loss1,loss2)
        preY_valid = sess.run(y, feed_dict={x: npx_test, keep_prob: 1})
        #np.savetxt(path + "preY_valid.csv", preY_valid.reshape(-1, 1), fmt="%.8f", delimiter=',')
        # test
        preY_test = sess.run(y, feed_dict={x: preX, keep_prob: 1})
        #np.savetxt(path + "preY_test.csv", preY_test.reshape(-1, 1), fmt="%.8f", delimiter=',')
        if outputs is None:
            outputs=preY_test.reshape(-1, 1)
        else:
            outputs=np.c_[outputs, preY_test.reshape(-1, 1)]
    del sess
    gc.collect()
    return outputs

def runtask(taskname):
    tensorss=[["tensor_fill_zao.csv","tensor_fill_zhong.csv"],["tensor_fill_zhong.csv","tensor_fill_wan.csv"],["tensor_fill_wan.csv"]]
    zzw=1
    tensors=tensorss[zzw]
    outputs=None
    inpath=rootpath+taskname+"\\"
    tensor=np.loadtxt(inpath+tensors[0],delimiter=',') #修改2
    knownX,knownY,preX=splitData(tensor,30,days) #修改4, -16还是-31 [0:-31,:]
    if(len(tensors)==2):
        tensor2=np.loadtxt(inpath+tensors[1],delimiter=',') #修改3
        knownX2,_,preX2=splitData(tensor2,30,days)  #修改5
        knownX=np.c_[knownX,knownX2]                        #修改6
        preX=np.c_[preX,preX2]                              #修改7
    #trueY=tensor[0:-31,:][-days::,-30::].reshape(-1,1)
    print(knownX.shape,knownY.shape,preX.shape)
    inputnum=knownX.shape[1]
    outputnum=knownY.shape[1]
    nnnb=build_nnnb([120], inputnum, outputnum)
    #kf = KFold(n_splits=int(knownX.shape[0]))
    for i in range(1):
        kf = KFold(n_splits=4)
        for train_index, valid_index in kf.split(knownX):
            print("taskname:",taskname,"i:",i)
            tensors = knownX[train_index], knownX[valid_index],knownY[train_index], knownY[valid_index], preX
            outputs=train_nnnb(taskname,tensors,nnnb,int(3e4),0.88,3e-4,outputs)
            #np.savetxt(path+"validYtrue.csv",knownY[valid_index].reshape(-1, 1), fmt="%.8f",delimiter=',')
    #np.savetxt(inpath + "outputs.csv", outputs, fmt="%.8f", delimiter=',')
#     outputsmedian=np.median(outputs,1).reshape(-1,1)
#     outputsmean=np.mean(outputs,1).reshape(-1,1)
#     print(np.mean(abs(outputsmean-trueY)/trueY))
#     print(np.mean(abs(outputsmedian-trueY)/trueY))
    sharetaskpath=sharepath+taskname+"\\"
    if not os.path.exists(sharetaskpath):
        os.makedirs(sharetaskpath)
    np.savetxt(sharetaskpath+ "outputsmedian_wan.csv", np.median(outputs,1), fmt="%.8f", delimiter=',')
    np.savetxt(sharetaskpath+ "outputsmean_wan.csv", np.mean(outputs,1), fmt="%.8f", delimiter=',')


r=10  #修改8
print(r)
allTask=os.listdir(rootpath)
allTask=allTask[0+12*r:12+12*r] #修改9
# allTask=["4377906283525800514"]

while(len(allTask)>0):
    if(len(allTask)>1):
        cutasks=allTask[0:1]
        allTask=allTask[1::]
    else:
        cutasks=allTask
        allTask=[]
    threads = []
    for taskname in cutasks:
        threads.append(threading.Thread(target=runtask,args=(taskname,)))
    
    for t in threads:
        t.setDaemon(True)
        t.start()
    
    for t in threads:
        t.join()