# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:48:25 2019

@author: USER
"""
from const import fuzzyTable
class classnode:#cho 1 node
    def __init__(self):
        self.name=""
        self.parent=""
        self.level=-1
        self.child=-1
        self.matrix=[]
        self.weight=[]
    def __repr__(self):
        return '(node) ' + str(self.name) + str(self.matrix) +  '\n'

def readdata(name):
    f = open(name,'r')
    lines = f.readlines()
    lengthfile=len(lines)-1
    mylist=[]
    for i in range(0,lengthfile):
        mylist.append(classnode())
    for j in range(0,lengthfile):
        k=j+1
        data1=lines[k].split(';')       
        mylist[j].name=data1[0]
        mylist[j].parent=data1[1]
        mylist[j].level=int(data1[2])
        mylist[j].child=readchild(data1[3])
        temp=data1[4].strip('\n')
        mylist[j].matrix=matrix(temp)
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
    # Return a fuzzy list of list instead of string
    for i in range(len(temp)):
        for u in range(len(temp[i])):
            temp[i][u] = fuzzyTable[temp[i][u]]
    return temp

# Matrix now return fuzzy number
# def matrix(rawdata):
#     temp = []
#     sub1 = []
#     sub2=''
#     for i in range(0, len(rawdata)):
#         if rawdata[i] == '{' :
#             temp = []
            
#         elif rawdata[i] == '[' :
#             sub1 = []
            
#         elif rawdata[i] == '(' :
#             sub2 = ''
            
#         elif rawdata[i] == ')':
            
#             sub1.append(sub2)
            
#         elif rawdata[i] == ']':
#             temp.append(sub1)
            
#         elif rawdata[i] == '}':
#             continue
            
#         elif rawdata[i] ==',':
#             continue
#         else:
#             b = rawdata[i] #remember to put int()
#             sub2+=b
#     return temp

def convert_value_from_dict(dic,filedata):  #dictionary, x la abs
    for i in filedata:
        for j in i.matrix:
            for k in range(0, len(j)):
                for l in dic:
                    print ( 'com' , l , j[k])
                    if l == j[k]:
                        val = dic[l]
                        j[k] = val

def geometric_mean(mang_fuzzy):
    re = 0
    if (len(mang_fuzzy) == 1):
        re = mang_fuzzy[0]
        result = re**1/float(len(mang_fuzzy))
    else:
        for i in range(0, len(mang_fuzzy)-1):
            if i == 0:
                re = mang_fuzzy[i]*mang_fuzzy[i+1]
                # re = mulfuzzy(mang_fuzzy[i],mang_fuzzy[i+1])
            else:
                # re = mulfuzzy(re,mang_fuzzy[i+1])
                re = re*mang_fuzzy[i+1]
        result = re**1/float(len(mang_fuzzy))
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
        # s = sumfuzzy(s,temp)
        s = s+temp
    #print(s)
    for j in mem:
        weight = j / s
        # weight = divfuzzy(j,s)
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

def sumproduct(mang1,matrix):
    result = []
    for i in range(0, len(matrix)):
        temp = (0,0,0)
        for j in range(0, len(mang1)):
            temp = temp + (mang1[j] * matrix[i][j])
            # temp = sumfuzzy(temp,mulfuzzy(mang1[j],matrix[i][j]))
        result.append(temp)
    return result
        



def node_calculation(node,refine_data):
    x = find(node, refine_data)
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
    print(consistency)
