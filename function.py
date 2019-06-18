# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:48:25 2019

@author: USER
"""
import time

class classnode:#cho 1 node
    def __init__(self):
        self.name=""
        self.parent=""
        self.level=-1
        self.child=-1
        self.matrix=[]
        self.weight=[]
        
        
def sumfuzzy(*arg):
    sum1=0
    sum2=0
    sum3=0
    for i in arg:
        sum1+=i[0]
        sum2+=i[1]
        sum3+=i[2]
    result=(round(sum1,4),round(sum2,4),round(sum3,4))
    return result

def mulfuzzy(*arg):
    
    sum1=1
    sum2=1
    sum3=1
    for i in arg:
        sum1*=i[0]
        sum2*=i[1]
        sum3*=i[2]
    result=(round(sum1,4),round(sum2,4),round(sum3,4))
    return result

def subfuzzy(a,b):
    check=(a[1]-b[1])
    sub1=0
    sub2=0   
    sub3=0
    if check >0:
        sub1=a[0]-b[2]
        sub2=a[1]-b[1]    
        sub3=a[2]-b[0]
        result=(round(sub1,4),round(sub2,4),round(sub3,4))
        return result
    else:
        print("Error, please retry!")

def divfuzzy(a,b):
    r1=float(a[0])/float(b[2])
    r2=float(a[1])/float(b[1])    
    r3=float(a[2])/float(b[0])
    result=(round(r1,4),round(r2,4),round(r3,4))
    return result

def invfuzzy(a):
    r1=1/float(a[2])
    r2=1/float(a[1])
    r3=1/float(a[0])
    result=(round(r1,4),round(r2,4),round(r3,4))
    #result=(r1,r2,r3)
    return result

def powfuzzy(a,b):
#    r1=a[0]**float(b)
#    r2=a[1]**float(b)
#    r3=a[2]**float(b)
    r1 = pow(a[0],b)
    r2 = pow(a[1],b)
    r3 = pow(a[2],b)
    result=(round(r1,4),round(r2,4),round(r3,4))
    #result=(r1,r2,r3)
    return result

def readdata(name):
    print('read data' , name)
    f = open(name,'r')
    lines = f.readlines()
    lengthfile=len(lines)-1
    mylist=[]
    for i in range(0,lengthfile):
        mylist.append(classnode())
    for j in range(0,lengthfile):
        k=j+1
        data1=lines[k].split(';')
        #print(data1)
        mylist[j].name=data1[0]
        mylist[j].parent=data1[1]
        mylist[j].level=int(data1[2])
        mylist[j].child=readchild(data1[3])
        temp=data1[4].strip('\n')
        mylist[j].matrix=matrix(temp)
    print(mylist , len(mylist))
    return mylist

#def geometric_mean_fuzzy(matrix):


def readchild(rawdata):
    temp=[]
    temp2=''
    for i in rawdata:
        if i=='{':
            temp=[]
        elif i==',':
            temp.append(temp2)
            temp2=''
            continue
        elif i=='}':
            temp.append(temp2)
            temp2=''
        else:
                temp2+=i
    return temp

# Convert family structure of matrix into nested list
def matrix(rawdata):
    temp = []
    sub1 = []
    sub2=''
    for i in range(0, len(rawdata)):
        if rawdata[i] == '{' :
            temp = []
            
        elif rawdata[i] == '[' :
            sub1 = []
            
        elif rawdata[i] == '(' :
            sub2 = ''
            
        elif rawdata[i] == ')':
            
            sub1.append(sub2)
            
        elif rawdata[i] == ']':
            temp.append(sub1)
            
        elif rawdata[i] == '}':
            continue
            
        elif rawdata[i] ==',':
            continue
        else:
            b = rawdata[i] #remember to put int()
            sub2+=b
    # raise ValueError(rawdata,'\n\n',temp)
    
    return temp

def convert_value_from_dict(dic,filedata):  #dictionary, x la abs
    # raise ValueError(dic,filedata)
    for i in filedata:
        for j in i.matrix:
            for k in range(0, len(j)):
                for l in dic:
                    if l == j[k]:
                        val = dic[l]
                        j[k] = val

def geometric_mean(mang_fuzzy):
    # ([(7.0, 9.0, 9.0), (1.0, 1.0, 1.0), (1.0, 3.0, 5.0)], '\n\n', (1.9129, 3.0, 3.5569))y
    re = 0
    if (len(mang_fuzzy) == 1):
        re = mulfuzzy(mang_fuzzy[0])
        result = powfuzzy(re,1/float(len(mang_fuzzy)))
    else:
        for i in range(0, len(mang_fuzzy)-1):
            if i == 0:
                re = mulfuzzy(mang_fuzzy[i],mang_fuzzy[i+1])
            else:
                re = mulfuzzy(re,mang_fuzzy[i+1])
        result = powfuzzy(re,1/float(len(mang_fuzzy)))
    # print(mang_fuzzy,'\n\n',result)
    # time.sleep(1)
    return result
    

def normalize_expert_matrix(rawdata):
    matrix_line = []
    for i in range(0, len(rawdata[0])):
        matrix = []
        for j in range(0, len(rawdata[0][i].matrix)):
            line = []
            for k in range(0, len(rawdata[0][i].matrix)):
                temp = []
                for l in range(0, len(rawdata)):
                    x = rawdata[l][i].matrix
                    y = x[j][k]
                    temp.append(y)
                #print(temp)
                r = geometric_mean(temp)
                line.append(r)
            matrix.append(line)
        matrix_line.append(matrix)
    #print(matrix_line)    
    return matrix_line
        

def normalize_expert(rawdata):
    combine_data = []
    matrix1 = normalize_expert_matrix(rawdata)
    for i in range(0,len(rawdata[0])):
       nodedata = classnode()
       nodedata.name = rawdata[0][i].name
       nodedata.parent = rawdata[0][i].parent
       nodedata.level = rawdata[0][i].level
       nodedata.child = rawdata[0][i].child
       nodedata.matrix = matrix1[i]
       combine_data.append(nodedata)
    return combine_data



def weight_calculation(matrix):
    result = []
    s = (0,0,0)
    mem = []
    for i in matrix:
        temp = geometric_mean(i)
        #print("temp:", temp)
        mem.append(temp)
        s = sumfuzzy(s,temp)
    #print(s)
    for j in mem:
        weight = divfuzzy(j,s)
        result.append(weight)
    return result


def find(node,refine_data):
    for i in refine_data:
        if i.name == node:
            return i

def transpose_matrix(mat):
    result = []
    for i in range(0,len(mat[0])):
        result_line = []
        for j in range(0,len(mat)):
            result_line.append(mat[j][i])
        result.append(result_line)
    return result
import time
def sumproduct(mang1,matrix):
    print('MATRIX' , len(mang1) , '=' , len(matrix[0]) ,'X' , len(matrix))
    time.sleep(0.1)
    with open('sum.json','w') as f :
        f.write(str(mang1)+'\n'+str(matrix)+'\n')
    result = []
    for i in range(0, len(matrix)):
        temp = (0,0,0)
        for j in range(0, len(mang1)):
            temp = sumfuzzy(temp,mulfuzzy(mang1[j],matrix[i][j]))
        result.append(temp)
    return result
    
        



def node_calculation(node,refine_data):
    
    x = find(node, refine_data)
    if x == None :
        raise ValueError(node , refine_data)
    if x.child == ['ATLS']:
        w1 = x.weight
        return w1
    else:
        mat = []
        for i in x.child:
            w2 = node_calculation(i, refine_data)
            mat.append(w2)
        mat_transpose = transpose_matrix(mat)
        w3 = x.weight
        w4 = sumproduct(w3,mat_transpose)
        return w4
            
def normalize_fuzzy(mangkq):
    result = []
    for i in mangkq:
        x = (i[0] + i[1] + i[2])/3
        result.append(round(x,3))
    return result


def check_consistency(matrix):
    try :
        n = len(matrix)
        list_geomean = []
        for i in range(0, n):
            x = geometric_mean(matrix[i])
            #print(x)
            list_geomean.append(x)
        
        L = []
        M = 0
        U = []
        for i in range(0, n):
            L.append(round((list_geomean[i][1]/list_geomean[i][0]),2))
            M += round(list_geomean[i][1],2)
            U.append(round((list_geomean[i][2]/list_geomean[i][1]),2))
        #print("================")
        
        weight_ind = (min(L),M,min(U))
        #print(weight_ind)
        
        WL = []
        WM = []
        WU = []
        
        for i in range(0, n):
            WL.append(round((weight_ind[0]*list_geomean[i][0]/M),2))
            WM.append(round((list_geomean[i][1]/M),2))
            WU.append(round((weight_ind[2]*list_geomean[i][2]/M),2))
        #print("================")
        
        WLU = []
        WMM = []
        WUL = []
        
        for i in range(0, n):
            temp_WLU = []
            temp_WMM = []
            temp_WUL = []
            for j in range(0, n):
                temp_WLU.append(round((WL[i]/WU[j]),2))
                temp_WMM.append(round((WM[i]/WM[j]),2))
                temp_WUL.append(round((WU[i]/WL[j]),2))
            WLU.append(temp_WLU)
            WMM.append(temp_WMM)
            WUL.append(temp_WUL)
        
        temp = []
        for i in range(0, n):
            for j in range(0, n):
                x = max(abs(WLU[i][j] - matrix[i][j][0]),
                        abs(WMM[i][j] - matrix[i][j][1]),
                        abs(WUL[i][j] - matrix[i][j][2]))
                temp.append(x)
        
        y = max(temp)
        
        
        tester = pow(float(n/2),float(n/(n-2)))
        if (11 >= tester):
            constant = max((11 - pow(11,(2*n-2)/n)),(pow(11,(2*n-2)/n)-11))
        else:
            constant = max((11 - pow(11,(2*n-2)/n)))
        #print(constant)
            
        consistency = round(pow(constant,-1)*y,4)
        return consistency
    except :
        return 0
