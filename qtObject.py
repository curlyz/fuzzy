
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

class SpinBox(QWidget):
	def __init__(self, parent = None):
		super(SpinBox, self).__init__(parent)
		
		layout = QVBoxLayout()
		self.l1 = QLabel("current value:")
		self.l1.setAlignment(Qt.AlignCenter)
		layout.addWidget(self.l1)
		self.sp = QSpinBox()
		
		layout.addWidget(self.sp)
		self.sp.valueChanged.connect(self.valuechange)
		self.setLayout(layout)
		self.setWindowTitle("SpinBox demo")
		
	def valuechange(self):
		self.l1.setText("current value:"+str(self.sp.value()))


class LabeledSlider(QWidget):
	FUZZY_LABELS = ["⅑","⅐","⅕","⅓","1","3","5","7","9"]
	def __init__(self,name='Hello',manufacturers = [], minimum=0, maximum=8, interval=1, orientation=Qt.Horizontal,
			labels=FUZZY_LABELS, parent=None):
		super(LabeledSlider, self).__init__(parent=parent)

		# Patch , manufacturer name
		# For internal dictionary key, use self.name
		# QLabel will use mapping value from parent.manufacturers
		levels=range(minimum, maximum+interval, interval)
		if labels is not None:
			if not isinstance(labels, (tuple, list)):
				raise Exception("<labels> is a list or tuple.")
			if len(labels) != len(levels):
				raise Exception("Size of <labels> doesn't match levels.")
			self.levels=list(zip(levels,labels))
		else:
			self.levels=list(zip(levels,map(str,levels)))

		if orientation==Qt.Horizontal:
			self.layout=QVBoxLayout(self)
		elif orientation==Qt.Vertical:
			self.layout=QHBoxLayout(self)
		else:
			raise Exception("<orientation> wrong.")
		self.name = name

		# Patch , ATLS0 vs ATLS1 => Manu1 vs Mannu2  ['Manu1' , 'Mannu2' ]
		if 'ATLS' in self.name :
			nameString = name.replace('ATLS','').split(' vs ') # ['0','1']
			for i in range(2):
				index = int(nameString[i])
				nameString[i] = manufacturers[index]
			self.labelString = ' vs '.join(nameString)
			self.label = QLabel(self.labelString)
		else :
			self.label = QLabel(name)
		
		# gives some space to pass#//print labels
		self.left_margin=10
		self.top_margin=10
		self.right_margin=10
		self.bottom_margin=10

		self.layout.setContentsMargins(self.left_margin,self.top_margin,
				self.right_margin,self.bottom_margin)

		self.slider=QSlider(orientation, self)
		
		self.slider.setMinimum(minimum)
		self.slider.setMaximum(maximum)
		self.slider.setValue(minimum)
		if orientation==Qt.Horizontal:
			self.slider.setTickPosition(QSlider.TicksBelow)
			self.slider.setMinimumWidth(300) # just to make it easier to read
		else:
			self.slider.setTickPosition(QSlider.TicksLeft)
			self.slider.setMinimumHeight(300) # just to make it easier to read
		self.slider.setTickInterval(interval)
		self.slider.setSingleStep(1)
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.slider)
		self.slider.valueChanged.connect(self.onValueChange)
		self.pos = 0
		self.setMinimumHeight(70)

	def __repr__(self):
		return 'LabeledSlider(' + str(self.name) + ')'

	def onValueChange(self,evt):
		pass#//print('change' , evt)
		self.pos = evt

	def mousePressEvent(self,evt):
		pass#//print(evt)

	def paintEvent(self, e):

		super(LabeledSlider,self).paintEvent(e)

		style=self.slider.style()
		painter=QPainter(self)
		st_slider=QStyleOptionSlider()
		st_slider.initFrom(self.slider)
		st_slider.orientation=self.slider.orientation()

		length=style.pixelMetric(QStyle.PM_SliderLength, st_slider, self.slider)
		available=style.pixelMetric(QStyle.PM_SliderSpaceAvailable, st_slider, self.slider)

		for v, v_str in self.levels:

			# get the size of the label
			rect=painter.drawText(QRect(), Qt.TextDontPrint, v_str)

			if self.slider.orientation()==Qt.Horizontal:
				# I assume the offset is half the length of slider, therefore
				# + length//2
				x_loc=QStyle.sliderPositionFromValue(self.slider.minimum(),
						self.slider.maximum(), v, available)+length//2

				# left bound of the text = center - half of text width + L_margin
				left=x_loc-rect.width()//2+self.left_margin
				bottom=self.rect().bottom()

				# enlarge margins if clipping
				if v==self.slider.minimum():
					if left<=0:
						self.left_margin=rect.width()//2-x_loc
					if self.bottom_margin<=rect.height():
						self.bottom_margin=rect.height()

					self.layout.setContentsMargins(self.left_margin,
							self.top_margin, self.right_margin,
							self.bottom_margin)

				if v==self.slider.maximum() and rect.width()//2>=self.right_margin:
					self.right_margin=rect.width()//2
					self.layout.setContentsMargins(self.left_margin,
							self.top_margin, self.right_margin,
							self.bottom_margin)

			else:
				y_loc=QStyle.sliderPositionFromValue(self.slider.minimum(),
						self.slider.maximum(), v, available, upsideDown=True)

				bottom=y_loc+length//2+rect.height()//2+self.top_margin-3
				# there is a 3 px offset that I can't attribute to any metric

				left=self.left_margin-rect.width()
				if left<=0:
					self.left_margin=rect.width()+2
					self.layout.setContentsMargins(self.left_margin,
							self.top_margin, self.right_margin,
							self.bottom_margin)

			pos=QPoint(left, bottom)
			painter.drawText(pos, v_str)

		return

	def setValue(self,value):
		pass#//print('set' , self , 'to' , value)
		self.slider.setValue(value)

	def getValue(self):
		return self.pos


class Dialogue(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 input dialogs - pythonspot.com'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.response = ''
		self.initUI()
		

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.getText()
		
		self.show()
		
	def getInteger(self):
		i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
		if okPressed:
			pass#//print(i)

	def getDouble(self):
		d, okPressed = QInputDialog.getDouble(self, "Get double","Value:", 10.50, 0, 100, 10)
		if okPressed:
			pass#//print( d)
		
	def getChoice(self):
		items = ("Red","Blue","Green")
		item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
		if ok and item:
			pass#//print(item)

	def getText(self):
		text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
		if okPressed and text != '':
			self.response = text

class ManufacturerDialog(QMainWindow):
	def __init__(self,count):
		QMainWindow.__init__(self)

		self.setMinimumSize(QSize(320, 140))    
		self.setWindowTitle("PyQt Line Edit example (textfield) - pythonprogramminglanguage.com") 

		self.nameLabel = QLabel(self)
		self.nameLabel.setText('Name:')
		self.line = QLineEdit(self)

		self.line.move(80, 20)
		self.line.resize(200, 32)
		self.nameLabel.move(20, 20)

		pybutton = QPushButton('OK', self)
		pybutton.clicked.connect(self.clickMethod)
		pybutton.resize(200,32)
		pybutton.move(80, 60)    

	def clickMethod(self):
		pass#//print('Your name: ' + self.line.text())

if False:
	class ManufacturerDialog(QWidget):

		def __init__(self,manufacturersCount):
			super().__init__()
			self.title = 'PyQt5 input dialogs - pythonspot.com'
			self.left = 10
			self.top = 10
			self.width = 640
			self.height = 480
			self.manufacturers = []
			self.manufacturersCount = manufacturersCount
			self.response = ''
			self.initUI()
			

		def initUI(self):
			self.setWindowTitle(self.title)
			self.setGeometry(self.left, self.top, self.width, self.height)
			
			self.layout = QVBoxLayout()

			for i in range(10):
				content = self.manufacturers[i] if len(self.manufacturers) > i else ''
				widget = QLineEdit(content)
				self.layout.addWidget(widget)

			self.setLayout(self.layout)
			self.show()
			
		def getInteger(self):
			i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
			if okPressed:
				pass#//print(i)

		def getDouble(self):
			d, okPressed = QInputDialog.getDouble(self, "Get double","Value:", 10.50, 0, 100, 10)
			if okPressed:
				pass#//print( d)
			
		def getChoice(self):
			items = ("Red","Blue","Green")
			item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
			if ok and item:
				pass#//print(item)

		def getText(self):
			text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
			if okPressed and text != '':
				self.response = text



class FileDialog(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 file dialogs - pythonspot.com'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.response = ''
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.openFileNameDialog()
		
		self.show()
	
	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			pass#//print(fileName)
			self.response = fileName
	
	def openFileNamesDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
		if files:
			pass#//print(files)
			self.response = files
	
	def saveFileDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
		if fileName:
			pass#//print(fileName)''
if False :
	a = QDialog()
	a.setLayout()

class ManufacturerForm(QDialog):

	def __init__(self,num , manufacturers ,  parent=None):
		super(ManufacturerForm, self).__init__(parent)
	
		self.setWindowTitle("Set Manufacturer Name")

		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.finishButton = QPushButton("OK")

		self.parameterLayout = QVBoxLayout()
		self.layout.addLayout(self.parameterLayout)
		for index in range(num):
			try :
				name = manufacturers[index]
			except :
				name = 'ATLS' + str(index)

			lineEdit = QLineEdit(name)
			
			self.parameterLayout.addWidget(lineEdit)
		self.layout.addWidget(self.finishButton)
		self.finishButton.clicked.connect(self.finish)

		self.response = []
	
	def finish(self):
		items = list(self.parameterLayout.itemAt(i).widget().text() for i in range(self.parameterLayout.count())) 
		self.response = items # ['Name1' , 'Name2']
		self.close()
		

class numManufacturerForm(QDialog):

	def __init__(self,parent=None):
		super(numManufacturerForm, self).__init__(parent)
		self.setWindowTitle("Set Manufacturer Name")

		self.response =  self.getInteger()

	def getInteger(self):
		i, okPressed = QInputDialog.getInt(self, "Config Manufacturer","How many manufacturers ?", 2, 0, 100, 1)
		if okPressed:
			return i

