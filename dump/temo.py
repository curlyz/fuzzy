from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys

from dataParser import *
PATH = "C:/Users/Curly/Desktop/fuzzy/expert1.txt"




class TreeParameter(QWidget):
	def __init__(self, parent=None):
		super(TreeParameter, self).__init__(parent)
		self.lay = QVBoxLayout(self)
		tree = QTreeWidget()
		tree.setHeaderLabel('The Magic Table')
		tree.setColumnCount(1)
		self.lay .addWidget(tree)
		self.sliderCount = 1
		for i in range(4):
			parent_it = QTreeWidgetItem(["{}-{}".format(i, l) for l in range(2)])
			tree.addTopLevelItem(parent_it)
			for j in range(5):
				it = QTreeWidgetItem(["{}-{}-{}".format(i, j, l) for l in range(2)])
			
				parent_it.addChild(it)
		tree.expandAll()

		tree.itemClicked.connect(self.onItemClicked)
		tree.itemDoubleClicked.connect(self.editName)
		self.tree = tree
		global_NodeTree = self.lay

	def editName(self,evt):
		print('editname' , evt)
		newName = Dialogue().response
		evt.setText(0,newName)


	@pyqtSlot(QTreeWidgetItem, int)
	def onItemClicked(self, it, col):
		global global_SelectedNode
		
		global_SelectedNode = self.tree.selectedItems()
		print('g' , it, col, it.text(col))

	def recursiveImportNode(self,topNode,QTopNode=None):
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
				

		
  






def dummy(*args, **kwargs):
	print(*args, **kwargs)
	pass

def deleteItem():
	if global_SelectedNode == None :
		print('no item selected')
		return
	root = global_SelectedNode
	for item in global_SelectedNode:
		print('item' , item.parent() , root)
		if item.parent() == None :
			print('deletetop')
		else :
			(item.parent() or root).removeChild(item)
	treeObject.tree.clearFocus()

def addItem():
	if global_SelectedNode == None :
		if treeObject.tree.topLevelItemCount() == 0 :
			dialogue = Dialogue()
			newNode = QTreeWidgetItem([dialogue.response])
			treeObject.tree.addTopLevelItem(newNode)
	else :
		print('addItemDiaglog')
		dialogue = Dialogue()
		print('return' , dialogue.response)
		newNode = QTreeWidgetItem([dialogue.response])
		global_SelectedNode[0].addChild(newNode)
		treeObject.tree.expandItem(global_SelectedNode[0])

def importItem():
	from dataParser import toEvn
	global treeObject
	if False :
		dlg = FileDialog()
		path = dlg.response
	path = r'C:\Users\Curly\Desktop\fuzzy\QBL03_code\QBL03\Manufacturer.txt'
	treeObject.tree.clear()

	topNode , allNode = toEvn(path)
	
	treeObject.recursiveImportNode(topNode)
	treeObject.tree.expandAll()
	

def calculateItem():
	pass

def exportItem():
	pass

def newItem():
	treeObject.tree.clear()

def sliderCountUpdate(value):
	print('slider',value)
	clearLayout(sliderLayout)
	for count in range(value):
		newSlider = LabeledSlider()
		sliderLayout.addWidget(newSlider)
        
def clearLayout(layout):
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().deleteLater()

def configManufacturer():
	print('addItemDiaglog')
	dialogue = Dialogue()
	print('return' , dialogue.response)
	newNode = QTreeWidgetItem([dialogue.response])
	global_SelectedNode[0].addChild(newNode)
	treeObject.tree.expandItem(global_SelectedNode[0])

BUTTON_LABEL = [
	['New',newItem],
	['Add',addItem],
	['Delete',deleteItem],
	['Config' , configManufacturer],
	['Import',importItem],
	['Calculate',calculateItem],
	['Export',exportItem]
]


global_SelectedNode = None
global_NodeTree = None



if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)
	win = QWidget()


	mainLayout = QVBoxLayout()
	
	interfaceLayout = QHBoxLayout()
	controlLayout = QHBoxLayout()
	mainLayout.addLayout(interfaceLayout)
	mainLayout.addLayout(controlLayout)
	treeLayout = QHBoxLayout()
	sliderLayout = QVBoxLayout()
	interfaceLayout.addLayout(treeLayout)
	rightLayout = QVBoxLayout()
	interfaceLayout.addLayout(rightLayout)

	# Add Tree
	treeObject = TreeParameter()
	treeLayout.addWidget(treeObject)

	# Adding widget
	spinBox = SpinBox()
	
	spinBoxLayout = QHBoxLayout()
	spinBoxLayout.addWidget(spinBox)
	spinBox.sp.valueChanged.connect(sliderCountUpdate)
	rightLayout.addLayout(spinBoxLayout)
	rightLayout.addLayout(sliderLayout)
	
	for i in range(treeObject.sliderCount):
		sliderLayout.addWidget(LabeledSlider())
	
	

	# Add Controll Button
	for b in BUTTON_LABEL :
		buttonLabel,function = b
		button = QPushButton()
		button.setText(buttonLabel)
		button.clicked.connect(function)
		controlLayout.addWidget(button)
	




	win.setLayout(mainLayout)
	win.show()
	sys.exit(app.exec_())