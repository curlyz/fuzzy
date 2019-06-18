# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:36:52 2019

@author: USER
"""

import function as func
import xlsxwriter
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
name_format =  workbook.add_format({'bold': True, 'font_color': 'red'})
name_format.set_shrink()


dictionary ={
	'one':(1,1,1),
	'eqx':(1,1,3),
	'wkx':(1,3,5),
	'esx':(3,5,7),
	'vsx':(5,7,9),
	'abx':(7,9,9),
	'eqr':func.invfuzzy((1,1,3)),
	'wkr':func.invfuzzy((1,3,5)),
	'esr':func.invfuzzy((3,5,7)),
	'vsr':func.invfuzzy((5,7,9)),
	'abr':func.invfuzzy((7,9,9))
		}



name =['temporary.json']
#name = ['test.txt']



rawdata = []
for i in name:
	filedata = func.readdata(i)
	func.convert_value_from_dict(dictionary,filedata)   
	rawdata.append(filedata)
refine_data = func.normalize_expert(rawdata)

def setColumnWidth(obj):
	for o in obj :
		for i in range(100):
			o.set_column(0,100,width = 20)

worksheet1 = workbook.add_worksheet('Weigth Calculation')
worksheet2 = workbook.add_worksheet('Raw Calculation Step2')
worksheet3 = workbook.add_worksheet('Consistency')
setColumnWidth([worksheet1,worksheet2,worksheet3])
currentRow = 0
currentColumn = 0
for j in refine_data:
	j.weight = func.weight_calculation(j.matrix)
	print("========" ,j.name, "STEP1" )
	worksheet1.write(currentRow,currentColumn,j.name, name_format)
	currentRow+=1
	dimension = len(j.matrix)	
	for y in range(len(j.matrix)):
		for x in range(len(j.matrix[0])):
			try :
				value = '(' + ', '.join([str(f) for f in j.matrix[y][x]]) + ')'
				worksheet1.write(currentRow+x,currentColumn+y,value)
			except :
				raise ValueError(value,x,y,j,j.matrix)
	currentRow += len(j.matrix)
	currentColumn = 0




currentRow = 0
currentColumn = 0	
for j in refine_data:
	print("========" ,j.name, " weight STEP2" )
	print(j.weight)

	worksheet2.write(currentRow,currentColumn,j.name, name_format)
	currentRow+=1
	dimension = len(j.weight)	
	for y in range(len(j.weight)):
		for x in range(len(j.weight[0])):
			worksheet2.write(currentRow+x,currentColumn+y,j.weight[y][x])
	currentRow += len(j.weight)
	currentColumn = 0

currentRow = 0
currentColumn = 0	
for a in refine_data:
	print("======== ",a.name," STEP3")
	r = func.check_consistency(a.matrix)
	worksheet3.write(currentRow,currentColumn,a.name, name_format)
	worksheet3.write(currentRow,currentColumn+1,r)

	currentRow+=1
	

print('NODE CALCULATION')
kq = func.node_calculation('O',refine_data)
print("==========result============")
print("kq ====", kq)
print("kq", func.normalize_fuzzy(kq))
print("==========checking consistency============")




workbook.close()