from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys
from qtObject import *
from dataParser import *
from collections import defaultdict
import time
# PATH = "C:/Users/Curly/Desktop/fuzzy/expert1.txt"

def rand():
	import random
	return random.randrange(10)

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
	def __init__(self):
		super(Controller,self).__init__(None)
		self.mainLayout = QVBoxLayout()
		self.interfaceLayout = QHBoxLayout()
		self.controlLayout = QHBoxLayout()
		self.mainLayout.addLayout(self.interfaceLayout)
		self.mainLayout.addLayout(self.controlLayout)
		self.setMinimumHeight(500)
		self.setFixedWidth(700)
		self.treeLayout = QVBoxLayout()
		self.tree = QTreeWidget()
		self.treeLayout.addWidget(self.tree)


		# @QWidget *central = new QWidget;
		# QScrollArea *scroll = new QScrollArea;
		# QVBoxLayout *g = new QVBoxLayout(central);
		# scroll->setWidget(central);
		# scroll->setWidgetResizable(true);
		# vbox2->addWidget(scroll);@
		# self.parameterLayout = QVBoxLayout()
		# self.scrollArea = QScrollArea(self)
		
		#Container Widget        
		#Layout of Container Widget
		# for _ in range(20):
		# 	btn = QPushButton("test")
		# 	layout.addWidget(btn)
		# widget.setLayout(sel)

		#Scroll Area Properties
		# self.groupSliderLayout = QGroupBox()
		# self.groupSliderLayout.setLayout(self.parameterLayout)
		
		# scroll = QScrollArea()
		# scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		# scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		# scroll.setWidgetResizable(False)
		# scroll.setWidget(self.groupSliderLayout)
		

			# @QWidget *central = new QWidget;
			# QScrollArea *scroll = new QScrollArea;
			# QVBoxLayout *g = new QVBoxLayout(central);
			# scroll->setWidget(central);
			# scroll->setWidgetResizable(true);
			# vbox2->addWidget(scroll);@

			# then i add my buttons to g

		# widget = QWidget()
		# scroll = QScrollArea()
		# self.sliderLayout = QVBoxLayout()
		# scroll.setWidget(widget)
		# scroll.setWidgetResizable(True)
		# self.parameterLayout.addWidget(scroll)
		# for i in range(30):
		# 	self.sliderLayout.addWidget(LabeledSlider())
		# self.parameterLayout.addWidget(scroll)
		
		#Scroll Area Layer add 
		# vLayout = QVBoxLayout(self)
		# vLayout.addWidget(scroll)
		

		# self.scrollArea.setWidget(self)
		# self.scrollArea.setWidgetResizable(True)

		# SCROLL PARAMETER LAYOUT
		self.parameterLayout = QVBoxLayout()
		scrollarea = QScrollArea(self)
		scrollarea.setWidgetResizable(True)
		inner = QFrame(scrollarea)
		inner.setLayout(self.parameterLayout)
		scrollarea.setWidget(inner)
		scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		


		# self.parameterLayout.addWidget(QLabel('Hey There'))
		self.interfaceLayout.addLayout(self.treeLayout)
		self.interfaceLayout.addWidget(scrollarea)

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

		configManufacturerBtn = QPushButton('Edit Manufacturer')
		configManufacturerBtn.clicked.connect(self.configManufacturer)


		

		self.controlLayout.addWidget(addItemBtn)
		self.controlLayout.addWidget(newProjectBtn)
		self.controlLayout.addWidget(deleteItemBtn)
		# self.controlLayout.addWidget(addManuBtn)
		self.controlLayout.addWidget(importProjectBtn)
		self.controlLayout.addWidget(configManufacturerBtn)
		self.controlLayout.addWidget(calculateItemBtn)
		# self.controlLayout.addWidget(exportItemBtn)

		self.setLayout(self.mainLayout)

		self.intFlag = False
		self.manufacturers = []
		self.criteriaWeight = {}

		self.tree.itemClicked.connect(self.onSingleClick)
		self.tree.doubleClicked.connect(self.onDoubleClick)

	def configManufacturer(self):
		form = ManufacturerForm(1 , [])
		form.exec_()
		print("List = " , form.response)


	def onSliderUpdate(self):
		if self.intFlag :
			return
		
		selectedItems = self.tree.selectedItems()
		if selectedItems == None or len(selectedItems) == 0 :
			return

		criteria = self.criteriaWeight[selectedItems[0].text(0)]

		items = (self.parameterLayout.itemAt(i).widget() for i in range(self.parameterLayout.count())) 

		
		for widget in items:
			criteria[widget.name] = widget.getValue()

		self.debug(self.criteriaWeight)

	def debug(self,d):
		with open('debug.json','w') as f :
			f.write(str(d))
		

	def onSingleClick(self,evt):
		print('onSingleClick' , str(evt))
		if True :
			name = evt.text(0)
			cr = self.criteriaWeight[name]
			with open('click.json','w') as  f:
				f.write(str(cr))

		
		self.showListSlider(evt.text(0))	
		

		# Get the child widget
		count = evt.childCount()
		for index in range(count):
			print('\t\tchild' , evt.child(count))

	def onDoubleClick(self,evt):
		print('onDoubleClick')

	def removeManufacturer(self):
		print('removeManufacturer')

	

	def clearSlider(self):
		layout = self.parameterLayout
		while layout.count():
			child = layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

	def recursiveImportNode(self,topNode,QTopNode=None):
		print('currentTopNode' , topNode)
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
				if childNode.name.startswith('ATLS'):
					# newNode = QTreeWidgetItem([self.manufacturers[index]])
					return

				self.recursiveImportNode(childNode,QTopNode=newNode)

	def importItem(self):
		if True :
			dlg = FileDialog()
			path = dlg.response
		#path = r'C:\Users\Curly\Desktop\fuzzy\QBL03_code\QBL03\Manufacturer.txt'
		self.tree.clear()

		topNode , allNode = toEvn(path)
		# Get the manufacturer count
		manufacturersCount = 0
		for node,data in allNode.items():
			if 'ATLS' in str(data.child):
				manufacturersCount = len(data.matrix)
				break

		# self.manufacturers = ManufacturerDialog(manufacturersCount)
		# self.manufacturers.show()

		# Default naem
		# self.manufacturers = ['Someone'] * len(topNode.matrix[0])

		# for i in range(len(self.manufacturers)):
		# 	slider = LabeledSlider(self.manufacturers[i])
		# 	slider.slider.valueChanged.connect(self.onSliderUpdate)
		# 	self.parameterLayout.addWidget(slider)

		nameForm = ManufacturerForm(manufacturersCount , [])
		nameForm.exec_()
		print('SET NAME ' , nameForm.response)
		self.manufacturers = nameForm.response

		self.criteriaWeight = allNode
		self.recursiveImportNode(topNode)
		self.tree.expandAll()


	def showListSlider(self,item):
		print('showListSlider')
		criteria = self.criteriaWeight[item]
		print('\t',criteria.sliderList())
		#DEBUG
		if len(criteria.sliderList()) == 0 :
			with open('node.json','w') as f :
				for n,d in self.criteriaWeight.items():
					f.write(n+'\t'+str(d)+'\n')
		self.clearSlider()
		for slider in criteria.sliderList():
			newSlider = LabeledSlider(name=slider,manufacturers=self.manufacturers)
			newSlider.slider.valueChanged.connect(self.onSliderUpdate)
			self.intFlag = True
			newSlider.setValue(criteria[slider])
			self.intFlag = False
			self.parameterLayout.addWidget(newSlider)
		self.resize(10,10)
		self.resize(10,10)
		

	def newProject(self):
		self.clearSlider()
		self.manufacturers = []
		self.criteriaWeight = {}
		self.tree.clear()

		numManufacturer = numManufacturerForm()
		print('count'  ,  numManufacturer.response)
		for index in range(numManufacturer.response):
			newData = {
				'Level' : -1,
				'Child' : [],
				'Matrix' : []
			}
			newNode = NodeData('ATLS' + str(index) , newData)
			self.criteriaWeight['ATLS' + str(index)] = newNode
			print('addManufacturer' , 'ATLS' + str(index) , newNode)
		print(str(self.criteriaWeight))
		nameForm = ManufacturerForm(numManufacturer.response , [])

		

		nameForm.exec_()
		print('SET NAME ' , nameForm.response)
		self.manufacturers = nameForm.response

		

	def exportItem(self):
		print(self.exportTree())
		pass

	def calculateItem(self):
		
		with open('temporary.json','w') as f :
			f.write( criteriaDumps(self.criteriaWeight) )

		exec(open('main.py').read())

		

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
				newItem = QTreeWidgetItem([dialogue.response])
				self.tree.addTopLevelItem(newItem)
				newData = {
					'Level' :0,
					'Child' : [] , #TODO
					'Matrix': []
				}
				newNode = NodeData(dialogue.response , newData)
				self.criteriaWeight[dialogue.response] = newNode

			
			return
		else :
			print('addItemDiaglog')
			dialogue = Dialogue()
			print('return' , dialogue.response)
			newItem = QTreeWidgetItem([dialogue.response])
			selected[0].addChild(newItem)
			self.tree.expandItem(selected[0])
			self.criteriaWeight[dialogue.response] = [4] * len(self.manufacturers)
		
		newData = {
			'Level' : self.criteriaWeight[selected[0].text(0)].level + 1,
			'Child' : ['ATLS'+str(index) for index in range(len(self.manufacturers))] , #TODO
			'Matrix': [	[4]*len(self.manufacturers) for _ in range(len(self.manufacturers))]

		}

		if True :
			with open('scope.json' ,'w') as f :
				for node , data in self.criteriaWeight.items():
					f.write(str(node)+'\t'+str(data) + '\n')
		newNode = NodeData(
			name = dialogue.response,
			data = newData,
			scope = self.criteriaWeight,
			isManufacturer = True

		)

		newNode.parent = self.criteriaWeight[selected[0].text(0)]

		self.criteriaWeight[dialogue.response] = newNode
		
		# self.criteriaWeight[selected[0].text(0)].child = [newNode]
		# self.criteriaWeight[selected[0].text(0)].matrix = [[4]]
		selectedItem = selected[0]
		selectedNode = self.criteriaWeight[selectedItem.text(0)]
		if selectedItem.childCount() == 1 : 
			selectedNode.child = [newNode]
		else :
			selectedNode.child.append(newNode)

		
		dimension = len(selectedNode.child)
		selectedNode.matrix = [ [4]*dimension for i in range(dimension)]

		self.debug(self.criteriaWeight)

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
				
		self.tree.clearFocus()

		self.deleteNodeTree(selected[0].text(0))

	def deleteNodeTree(self,name,currentList=None):
		print('progressDelete' , name , currentList)
		if currentList == None :
			listDelete = []
			self.deleteNodeTree(name,listDelete)
			print('DELETE ' , listDelete)

			# Find the parent node
			parentNode = None
			childNodeIndex = None
			for node,data in self.criteriaWeight.items():
				for i in range(len(data.child)) :
					if data.child[i].name == name :
						childNodeIndex = i
						parentNode = data
						break

			parentNode.child.pop(childNodeIndex)
			parentNode.matrix.pop(childNodeIndex)
			# Get the index of this node
			# Delete this node from parent.child
			
			
			# Delete that from the dictionary
			for _name in listDelete :
				print('delete' , _name)
				
				for node,data in self.criteriaWeight.items():
					try :
						for i in range(len(data.child)):
							if data.child[i].name == _name :
								data.child.pop(i)
								print('\n'*100)
								break
					except :
						pass

				del self.criteriaWeight[_name]
			

		else :
			try :
				for child in self.criteriaWeight[name].child :
					self.deleteNodeTree(child.name,currentList)

				if 'ATLS' in name :
					return
				currentList.append(name)
			except :
				pass

	

			
			



if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	controller = Controller()
	controller.show()
	sys.exit(app.exec_())