from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys
from qtObject import *
from dataParser import *
from collections import defaultdict
PATH = "C:/Users/Curly/Desktop/fuzzy/expert1.txt"


def rand():
	import random
	return random.randrange(10)

import faker

f = faker.Faker()


# from main.py
import function as func
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

mapping = ['one','eqx','wkx','esx','vsx','abx','eqr','wkr','esr','vsr','abr']


class Controller(QWidget):
	def __init__(self, parent=None):
		super(Controller, self).__init__(parent)
		# self.lay = QVBoxLayout(self)
		# tree = QTreeWidget()
		# tree.setHeaderLabel('The Magic Table')
		# tree.setColumnCount(1)
		# self.lay .addWidget(tree)
		# self.sliderCount = 1
		# for i in range(4):
		# 	parent_it = QTreeWidgetItem(["{}-{}".format(i, l) for l in range(2)])
		# 	tree.addTopLevelItem(parent_it)
		# 	for j in range(5):
		# 		it = QTreeWidgetItem(["{}-{}-{}".format(i, j, l) for l in range(2)])
			
		# 		parent_it.addChild(it)
		# tree.expandAll()

		# tree.itemClicked.connect(self.onItemClicked)
		# tree.itemDoubleClicked.connect(self.editName)
		# self.tree = tree
		# global_NodeTree = self.lay

		self.mainLayout = QVBoxLayout()
		self.interfaceLayout = QHBoxLayout()
		self.controlLayout = QHBoxLayout()
		self.mainLayout.addLayout(self.interfaceLayout)
		self.mainLayout.addLayout(self.controlLayout)


		self.treeLayout = QVBoxLayout()
		self.tree = QTreeWidget()
		self.treeLayout.addWidget(self.tree)
		self.parameterLayout = QVBoxLayout()
		# self.parameterLayout.addWidget(QLabel('Hey There'))
		self.interfaceLayout.addLayout(self.treeLayout)
		self.interfaceLayout.addLayout(self.parameterLayout)

		newProjectBtn = QPushButton('New Project')
		newProjectBtn.clicked.connect(self.newProject)

		addItemBtn = QPushButton('New Item')
		addItemBtn.clicked.connect(self.addItem)

		deleteItemBtn = QPushButton('Delete Item')
		deleteItemBtn.clicked.connect(self.deleteItem)

		addManuBtn = QPushButton('Add Manufacturer')
		addManuBtn.clicked.connect(self.addManufacturer)
		removeManuBtn = QPushButton('Remove Manufacturer')
		removeManuBtn.clicked.connect(self.removeManufacturer)

		importProjectBtn = QPushButton('Import')
		importProjectBtn.clicked.connect(self.importItem)

		calculateItemBtn = QPushButton('Calculate')
		calculateItemBtn.clicked.connect(self.calculateItem)

		exportItemBtn = QPushButton('Export')
		exportItemBtn.clicked.connect(self.exportItem)

		self.controlLayout.addWidget(addItemBtn)
		self.controlLayout.addWidget(newProjectBtn)
		self.controlLayout.addWidget(deleteItemBtn)
		self.controlLayout.addWidget(addManuBtn)
		self.controlLayout.addWidget(importProjectBtn)
		self.controlLayout.addWidget(calculateItemBtn)
		self.controlLayout.addWidget(exportItemBtn)

		self.setLayout(self.mainLayout)

		self.intFlag = False
		# Data
		self.manufacturers = []
		self.criteriaWeight = {}
		# 

		if False :
			for i in range(5):
				label = LabeledSlider()
				label.slider.valueChanged.connect(self.onSliderUpdate)
				self.parameterLayout.addWidget(label)
				self.manufacturers.append(f.name())

			

		self.tree.itemClicked.connect(self.onSingleClick)
		self.tree.itemDoubleClicked.connect(self.onDoubleClick)

	def onSliderUpdate(self):
		if self.intFlag :
			return
		t = self.tree.selectedItems()
		if t == None or len(t) == 0 :
			return

		criteria = t[0].text(0)
		print('update' , criteria)

		data = self.criteriaWeight[criteria]
		widgetCount = self.parameterLayout.count()

		for i in range(widgetCount-len(data)):
			data.append(0)
		for index in range(widgetCount):
			widget = self.parameterLayout.itemAt(index).widget()
			data[index] = widget.getValue()
		print('data' , data)
		
		
		
	def onSingleClick(self,evt):
		widgetCount = self.parameterLayout.count()
		print('singleClick' , evt.text(0) , 'count=',widgetCount)
		criteria = evt.text(0)
		if criteria not in self.criteriaWeight:
			self.criteriaWeight[criteria] = [4] * widgetCount
		c = self.criteriaWeight[criteria]
		if len(c) < len(self.manufacturers):
			for _ in range(len(self.manufacturers)-len(c)):
				c.append(4)
		
		for i in range(widgetCount-len(c)):
			c.append(1)
		print('data' , c)
		self.intFlag = True
		for index in range(len(c)):
			widget = self.parameterLayout.itemAt(index).widget()
			print('\t',widget)
			widget.setValue(c[index])
		self.intFlag = False


	# def editName(self,evt):
	# 	print('editname' , evt)
	# 	newName = Dialogue().response
	# 	evt.setText(0,newName)
	def onDoubleClick(self,evt):
		print('doubleClick' , evt)
		evt.setText(0,Dialogue().response)
	def addManufacturer(self):
		q = Dialogue()
		self.manufacturers.append(q.response)
		clearLayout(self.parameterLayout)
		for name in self.manufacturers :
			labelslider = LabeledSlider(name)
			labelslider.slider.valueChanged.connect(self.onSliderUpdate)
			self.parameterLayout.addWidget(labelslider)
	
	def removeManufacturer(self):
		pass

	def clearLayout(self,layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

	


	# @pyqtSlot(QTreeWidgetItem, int)
	# def onItemClicked(self, it, col):
	# 	print('click on ' , self.tree.SelectItems())

	def recursiveImportNode(self,topNode,QTopNode=None):
		self.criteriaWeight[topNode.name] = []
		if topNode.level == 0  :
			newNode = QTreeWidgetItem([topNode.name])
			self.tree.addTopLevelItem(newNode)
			for node in topNode.child :
				self.recursiveImportNode(node,QTopNode=newNode)

		else :
			print('currentLevel' , topNode)
			newNode = QTreeWidgetItem([topNode.name])
			QTopNode.addChild(newNode)
			for childNode in topNode.child :
				print('add' , childNode)
				if childNode == 'ATLS' :
					print('atls')
					return
				
				self.recursiveImportNode(childNode,QTopNode = newNode)

			return

	def deleteItem(self):
		selected = self.tree.selectedItems()
		if selected == None :
			print('no item selected')
			return
		
		for item in selected:
			print('item' , item.parent() , selected)
			if item.parent() == None :
				print('deletetop')
			else :
				(item.parent() or selected).removeChild(item)
				try :
					print('detete' , item.text(0))
					del self.criteriaWeight[item.text(0)]
				except Exception as err:
					print(err)
					pass
		self.tree.clearFocus()
		

	

	def addItem(self):
		selected = self.tree.selectedItems()
		if selected == None or len(selected) == 0 :
			if self.tree.topLevelItemCount() == 0 :
				dialogue = Dialogue()
				newNode = QTreeWidgetItem([dialogue.response])
				self.tree.addTopLevelItem(newNode)
		else :
			print('addItemDiaglog')
			dialogue = Dialogue()
			print('return' , dialogue.response)
			newNode = QTreeWidgetItem([dialogue.response])
			selected[0].addChild(newNode)
			self.tree.expandItem(selected[0])
			self.criteriaWeight[dialogue.response] = [4] * len(self.manufacturers)


	def importItem(self):
		if False :
			dlg = FileDialog()
			path = dlg.response
		path = r'C:\Users\Curly\Desktop\fuzzy\QBL03_code\QBL03\Manufacturer.txt'
		self.tree.clear()

		topNode , allNode = toEvn(path)
		self.manufacturers = ['Someone'] * len(topNode.matrix[0])
		self.clearLayout(self.parameterLayout)
		for i in range(len(self.manufacturers)):
			slider = LabeledSlider(self.manufacturers[i])
			slider.slider.valueChanged.connect(self.onSliderUpdate)
			self.parameterLayout.addWidget(slider)

		self.recursiveImportNode(topNode)
		self.tree.expandAll()
		
	def newItem(self):
		pass

	
	# Recursice
	def exportTree(self,lastNode=None,lastData=None):
		if lastNode == None :
			data = []
			root = self.tree.invisibleRootItem()
			for index in range(root.childCount()):
				obj = root.child(index)
				data.append(obj.text(0))
				self.exportTree(obj,data)
			return data
		else :
			count = lastNode.childCount()
			for index in range(count):
				widget = lastNode.child(index)
				lastData.append(widget.text(0))
				self.exportTree(widget,lastData)

	# This is a small workaround to fix delete parent node not delete child node bug
	# def getListItem(self,listRecursive=None,currentNode=None):
	# 	if listRecursive == None :
	# 		listRecursive = []
	# 		count = self.tree.topLevelItemCount()
	# 		for index in range(count):
	# 			item = self.tree.topLevelItem(index)
	# 			listRecursive.append(item.text(0))
	# 			print('addNodeToItemList' , listRecursive)
	# 			self.getListItem(listRecursive,item)
	# 	else :
	# 		node = QTreeWidgetItem()
	# 		countChildNode = node.
	# 		for node in currentNode.child():
	# 			print(node)

	def calculateItem(self):
		
		# Check each item for 
		# 1 . Item that has not been changed
		# 2 . Item that has a slider update before
		for criteria , data in self.criteriaWeight.items():
			print('manugfuadap'  , len(self.manufacturers))
			for i in range(len(self.manufacturers)-len(data)):
				data.append(4)

		# Remove deleted item
		listNode = self.exportTree()
		listKeys = list(self.criteriaWeight.keys())
		
		for key in listKeys :
			if key not in listNode :
				del self.criteriaWeight[key]
		for key in listNode :
			if key not in listKeys :
				print('Object' , key , 'is not modified')
		# Map slider number to fuzzy
		newDict = {}
		for key,data in self.criteriaWeight.items():
			newData = []
			for i in range(len(data)):
				newData.append(mapping.__getitem__(data[i]))

			newDict[key] = newData


		# for key,data in newJson.items():
		# 	if key not in listNode :
		# 		del newJson[key]
		# 	for i in range(len(data)):
		# 		data[i] = mapping.__getitem__(data[i])

		with open('data.json','w') as f :
			f.write(json.dumps(newDict,indent=4))

	def exportItem(self):
		print(self.exportTree())
		pass

	def newProject(self):
		self.clearLayout(self.parameterLayout)
		self.manufacturers = []
		self.criteriaWeight = {}
		self.tree.clear()



def sliderCountUpdate(value):
	print('slider',value)
	clearLayout(sliderLayout)
	for count in range(value):
		newSlider = LabeledSlider()
		sliderLayout.addWidget(newSlider)


def configManufacturer():
	print('addItemDiaglog')
	dialogue = Dialogue()
	print('return' , dialogue.response)
	newNode = QTreeWidgetItem([dialogue.response])
	global_SelectedNode[0].addChild(newNode)
	treeObject.tree.expandItem(global_SelectedNode[0])

# BUTTON_LABEL = [
# 	['New',newItem],
# 	['Add',addItem],
# 	['Delete',deleteItem],
# 	['Config' , configManufacturer],
# 	['Import',importItem],
# 	['Calculate',calculateItem],
# 	['Export',exportItem]
# ]


global_SelectedNode = None
global_NodeTree = None



if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)

	controller = Controller()

	# mainLayout = Con()
	
	# interfaceLayout = QHBoxLayout()
	# controlLayout = QHBoxLayout()
	# mainLayout.addLayout(interfaceLayout)
	# mainLayout.addLayout(controlLayout)
	# treeLayout = QHBoxLayout()
	# sliderLayout = QVBoxLayout()
	# interfaceLayout.addLayout(treeLayout)
	# rightLayout = QVBoxLayout()
	# interfaceLayout.addLayout(rightLayout)

	# # Add Tree
	# treeObject = Controller()
	# treeLayout.addWidget(treeObject)

	# # Adding widget
	# spinBox = SpinBox()
	
	# spinBoxLayout = QHBoxLayout()
	# spinBoxLayout.addWidget(spinBox)
	# spinBox.sp.valueChanged.connect(sliderCountUpdate)
	# rightLayout.addLayout(spinBoxLayout)
	# rightLayout.addLayout(sliderLayout)
	
	# for i in range(treeObject.sliderCount):
	# 	sliderLayout.addWidget(LabeledSlider())
	
	

	# # Add Controll Button
	# for b in BUTTON_LABEL :
	# 	buttonLabel,function = b
	# 	button = QPushButton()
	# 	button.setText(buttonLabel)
	# 	button.clicked.connect(function)
	# 	controlLayout.addWidget(button)
	


	controller.show()
	sys.exit(app.exec_())