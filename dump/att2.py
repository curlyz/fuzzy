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

class Controller (QWidget):
	def __init__(self,parent=None):
		super(Controller, self).__init__(parent)

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

		# addManuBtn = QPushButton('Add Manufacturer')
		# addManuBtn.clicked.connect(self.addManufacturer)
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
		# self.controlLayout.addWidget(addManuBtn)
		self.controlLayout.addWidget(importProjectBtn)
		self.controlLayout.addWidget(calculateItemBtn)
		self.controlLayout.addWidget(exportItemBtn)

		self.setLayout(self.mainLayout)

		self.intFlag = False
		self.manufacturers = []
		self.criteriaWeight = {}

		self.tree.itemClicked.connect(self.onSingleClick)
		self.tree.doubleClicked.connect(self.onDoubleClick)
		
	def onSliderUpdate(self):
		pass

	def onSingleClick(self,evt):
		pass

	def onDoubleClick(self,evt):
		pass


	def actionAddManufacturer(self):
		pass

	def removeManufacturer(self):
		pass

	def clearSlider(self):
		layout = self.parameterLayout
		while layout.count():
			child = layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

	def recursiveImportNode(self,topNode,QTopNode=None):
		self.criteriaWeight[topNode.name] = []
		if topNode.level == 0  :
			newNode = QTreeWidgetItem([topNode.name])
			self.tree.addTopLevelItem(newNode)
			for node in topNode.child :
				self.recursiveImportNode(node,QTopNode=newNode)

		else :
			newNode = QTreeWidgetItem([topNode.name])
			QTopNode.addChild(newNode)
			# for childNode in topNode.child :
			# 	if childNode == 'ATLS' :
			# 		return
			# 	self.recursiveImportNode(childNode,QTopNode = newNode)
			for index in range(len(topNode.child)):
				childNode = topNode.child[index]
				if childNode == 'ATLS':
					newNode = QTreeWidgetItem([self.manufacturers[index]])
					return

				self.recursiveImportNode(childNode,QTopNode=newNode)

	def importItem(self):
		if False :
			dlg = FileDialog()
			path = dlg.response
		path = r'C:\Users\Curly\Desktop\fuzzy\QBL03_code\QBL03\Manufacturer.txt'
		self.tree.clear()

		topNode , allNode = toEvn(path)
		# Get the manufacturer count
		manufacturersCount = 0
		for node,data in allNode.items():
			count =  data.child.count('ATLS')
			if count > 0 :
				manufacturersCount = count
				break

		self.manufacturers = ManufacturerDialog(manufacturersCount)
		self.manufacturers.show()
		# self.manufacturers = ['Someone'] * len(topNode.matrix[0])
		self.clearSlider()
		for i in range(len(self.manufacturers)):
			slider = LabeledSlider(self.manufacturers[i])
			slider.slider.valueChanged.connect(self.onSliderUpdate)
			self.parameterLayout.addWidget(slider)

		self.recursiveImportNode(topNode)
		self.tree.expandAll()

	def newProject(self):
		self.clearSlider()
		self.manufacturers = []
		self.criteriaWeight = {}
		self.tree.clear()

	def exportItem(self):
		print(self.exportTree())
		pass

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

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	controller = Controller()
	controller.show()
	sys.exit(app.exec_())