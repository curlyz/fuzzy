#https://stackoverflow.com/questions/42007434/slider-widget-for-pyqtgraph
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget

import pyqtgraph as pg
import numpy as np


class Slider(QWidget):
    def __init__(self, minimum, maximum, parent=None):
        super(Slider, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Vertical)
        self.horizontalLayout.addWidget(self.slider)
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())

        self.minimum = minimum
        self.maximum = maximum
        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.setLabelValue(self.slider.value())

    def setLabelValue(self, value):
        self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
        self.maximum - self.minimum)
        self.label.setText("{0:.4g}".format(self.x))


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent=parent)
        self.horizontalLayout = QHBoxLayout(self)
        self.w1 = Slider(-10, 10)
        self.horizontalLayout.addWidget(self.w1)

        self.w2 = Slider(-1, 1)
        self.horizontalLayout.addWidget(self.w2)

        self.w3 = Slider(-10, 10)
        self.horizontalLayout.addWidget(self.w3)

        self.w4 = Slider(-10, 10)
        self.horizontalLayout.addWidget(self.w4)

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.horizontalLayout.addWidget(self.win)
        self.p6 = self.win.addPlot(title="My Plot")
        self.curve = self.p6.plot(pen='r')
        self.update_plot()

        self.w1.slider.valueChanged.connect(self.update_plot)
        self.w2.slider.valueChanged.connect(self.update_plot)
        self.w3.slider.valueChanged.connect(self.update_plot)
        self.w4.slider.valueChanged.connect(self.update_plot)

    def update_plot(self):
        a = self.w1.x
        b = self.w2.x
        c = self.w3.x
        d = self.w4.x
        x = np.linspace(0, 10, 100)
        data = a + np.cos(x + c * np.pi / 180) * np.exp(-b * x) * d
        self.curve.setData(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())


#https://github.com/mmisono/pyqt5-example/blob/master/tic_tac_toe.py
#!/usr/bin/env python

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

class TicTacToe(QGraphicsItem):
    def __init__(self):
        super(TicTacToe, self).__init__()
        self.board = [[-1, -1, -1],[-1, -1, -1], [-1, -1, -1]]
        self.O = 0
        self.X = 1
        self.turn = self.O

    def reset(self):
        for y in range(3):
            for x in range(3):
                self.board[y][x] = -1
        self.turn = self.O
        self.update()

    def select(self, x, y):
        if x < 0 or y < 0 or x >= 3 or y >= 3:
            return
        if self.board[y][x] == -1:
            self.board[y][x] = self.turn
            self.turn = 1 - self.turn

    def paint(self, painter, option, widget):
        painter.setPen(Qt.black)
        painter.drawLine(0,100,300,100)
        painter.drawLine(0,200,300,200)
        painter.drawLine(100,0,100,300)
        painter.drawLine(200,0,200,300)

        for y in range(3):
            for x in range(3):
                if self.board[y][x] == self.O:
                    painter.setPen(Qt.red)
                    painter.drawEllipse(QPointF(50+x*100, 50+y*100), 30, 30)
                elif self.board[y][x] == self.X:
                    painter.setPen(Qt.blue)
                    painter.drawLine(20+x*100, 20+y*100, 80+x*100, 80+y*100)
                    painter.drawLine(20+x*100, 80+y*100, 80+x*100, 20+y*100)

    def boundingRect(self):
        return QRectF(0,0,300,300)

    def mousePressEvent(self, event):
        pos = event.pos()
        self.select(int(pos.x()/100), int(pos.y()/100))
        self.update()
        super(TicTacToe, self).mousePressEvent(event)

class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        scene = QGraphicsScene(self)
        self.tic_tac_toe = TicTacToe()
        scene.addItem(self.tic_tac_toe)
        scene.setSceneRect(0, 0, 300, 300)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("Tic Tac Toe")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_R:
            self.tic_tac_toe.reset()
        super(MainWindow, self).keyPressEvent(event)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())



#qt.py
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyle, QStyleOptionSlider
from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

class LabeledSlider(QtWidgets.QWidget):
    FUZZY_LABELS = ["⅑","⅐","⅕","⅓","1","3","5","7","9"]
    def __init__(self, minimum=1, maximum=9, interval=1, orientation=Qt.Horizontal,
            labels=FUZZY_LABELS, parent=None):
        super(LabeledSlider, self).__init__(parent=parent)

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
            self.layout=QtWidgets.QVBoxLayout(self)
        elif orientation==Qt.Vertical:
            self.layout=QtWidgets.QHBoxLayout(self)
        else:
            raise Exception("<orientation> wrong.")

        # gives some space to print labels
        self.left_margin=10
        self.top_margin=10
        self.right_margin=10
        self.bottom_margin=10

        self.layout.setContentsMargins(self.left_margin,self.top_margin,
                self.right_margin,self.bottom_margin)

        self.sl=QtWidgets.QSlider(orientation, self)
        self.sl.setMinimum(minimum)
        self.sl.setMaximum(maximum)
        self.sl.setValue(minimum)
        if orientation==Qt.Horizontal:
            self.sl.setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.sl.setMinimumWidth(300) # just to make it easier to read
        else:
            self.sl.setTickPosition(QtWidgets.QSlider.TicksLeft)
            self.sl.setMinimumHeight(300) # just to make it easier to read
        self.sl.setTickInterval(interval)
        self.sl.setSingleStep(1)

        self.layout.addWidget(self.sl)
        self.sl.valueChanged.connect(self.onValueChange)

    def onValueChange(self,evt):
        print('change' , evt)

    def mousePressEvent(self,evt):
        print(evt)

    def paintEvent(self, e):

        super(LabeledSlider,self).paintEvent(e)

        style=self.sl.style()
        painter=QPainter(self)
        st_slider=QStyleOptionSlider()
        st_slider.initFrom(self.sl)
        st_slider.orientation=self.sl.orientation()

        length=style.pixelMetric(QStyle.PM_SliderLength, st_slider, self.sl)
        available=style.pixelMetric(QStyle.PM_SliderSpaceAvailable, st_slider, self.sl)

        for v, v_str in self.levels:

            # get the size of the label
            rect=painter.drawText(QRect(), Qt.TextDontPrint, v_str)

            if self.sl.orientation()==Qt.Horizontal:
                # I assume the offset is half the length of slider, therefore
                # + length//2
                x_loc=QStyle.sliderPositionFromValue(self.sl.minimum(),
                        self.sl.maximum(), v, available)+length//2

                # left bound of the text = center - half of text width + L_margin
                left=x_loc-rect.width()//2+self.left_margin
                bottom=self.rect().bottom()

                # enlarge margins if clipping
                if v==self.sl.minimum():
                    if left<=0:
                        self.left_margin=rect.width()//2-x_loc
                    if self.bottom_margin<=rect.height():
                        self.bottom_margin=rect.height()

                    self.layout.setContentsMargins(self.left_margin,
                            self.top_margin, self.right_margin,
                            self.bottom_margin)

                if v==self.sl.maximum() and rect.width()//2>=self.right_margin:
                    self.right_margin=rect.width()//2
                    self.layout.setContentsMargins(self.left_margin,
                            self.top_margin, self.right_margin,
                            self.bottom_margin)

            else:
                y_loc=QStyle.sliderPositionFromValue(self.sl.minimum(),
                        self.sl.maximum(), v, available, upsideDown=True)

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



        
# class Controller (QtWidgets.QWidget):
#     def __init__(self,parent=None):
#         super(Controller,self).__init__(parent=parent)

        
#         w = LabeledSlider(1, 9 , 1, orientation=Qt.Horizontal,labels = FUZZY_LABELS)
#         g = LabeledSlider(1, 9 , 1, orientation=Qt.Horizontal,labels = FUZZY_LABELS)
#         h = LabeledSlider(1, 9 , 1, orientation=Qt.Horizontal,labels = FUZZY_LABELS)

#         self.layout = QtWidgets.QGridLayout(self)
#         self.sliderLayout = QtWidgets.QVBoxLayout()

#         self.sliderLayout.addWidget(w)
#         self.sliderLayout.addWidget(g)

#         self.layout.addLayout(self.sliderLayout,0,0,0,0,Qt.AlignHCenter)
#         self.layout.addLayout(self.graphicLayout,0,1,0,0,Qt.AlignHCenter)
#         # Example of right hand slider and a central graph

class Node(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()
    
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

    QGraphicsEllipseItem.mousePressEvent(self, event)
TypeError: mousePressEvent(self, QGraphicsSceneMouseEvent): first argument of unbound method must have type 'QGraphicsEllipseItem'

# Construct a unit radius circle for the graph
class EllipseObject(QtGui.QGraphicsObject):
    sigClicked = QtCore.pyqtSignal(float, float)
    def __init__(self, center= (0.0, 0.0), radius=1.0, pen=QtGui.QPen(QtCore.Qt.white)):
        QtGui.QGraphicsObject.__init__(self)
        self.center = center
        self.radius = radius
        self.pen = pen

    def boundingRect(self):
        rect = QtCore.QRectF(0, 0, 2*self.radius, 2*self.radius)
        rect.moveCenter(QtCore.QPointF(*self.center))
        return rect

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawEllipse(self.boundingRect())

    def mousePressEvent(self, event):
        p = event.pos()
        self.sigClicked.emit(p.x(), p.y())
        QtGui.QGraphicsEllipseItem.mousePressEvent(self, event)

class Graph(pg.GraphItem):
    def __init__(self):
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        pg.GraphItem.__init__(self)
        self.scatter.sigClicked.connect(self.onclick)
        self.data = lambda x: None
        self.text = lambda x: None

    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:            
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.settexts(self.text)
        self.updategraph()

    def settexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)

    def updategraph(self):
        pg.GraphItem.setData(self, **self.data)
        for i, item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])

    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return

        if ev.isStart():
            # We are already one step into the drag.
            # Find the point(s) at the mouse cursor when the button was first
            # pressed:
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind] - pos
        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return

        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset
        self.updategraph()
        ev.accept()

    # Once a node on the graph is clicked, the clicked node should become the center of the graph
    def onclick(plot, points):
        x = 0
        y = 0
        x, y = points.ptsClicked[0]._data[0], points.ptsClicked[0]._data[1]     # position of the clicked point
        print('Clicked point is (' + str(x) + ', ' + str(y) + ')')

# pg.setConfigOption('background', [0,0,0])
# pg.setConfigOption('foreground', 'k')
# app = QtGui.QApplication([])
# mw = QtGui.QMainWindow()
# mw.resize(800,800)
# view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
# mw.setCentralWidget(view)
# mw.show()
# mw.setWindowTitle('pyqtgraph example: ScatterPlot')

# app = QtGui.QApplication(sys.argv)
# win = QtWidgets.QWidget()
# grid = QtWidgets.QGridLayout()

# for i in range(5):
#     for j in range(5):
#         grid.addWidget( LabeledSlider( ) ,i,j)


    # for i in range(5):
    #     grid.addWidget( LabeledSlider() , i , 1)
    # tree = spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
    # grid.addWidget(tree,0,0)
    # win.setLayout(grid)
    # win.setGeometry(100,100,200,100)
    # win.show()

class Controller(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(Controller,self).__init__(parent=parent)
        
        
        self.slider = [LabeledSlider() for i in range(10)]
        print(self.slider)
        self.sliderLayout = QtWidgets.QVBoxLayout()
        for slider in self.slider :
            print('add' , slider)
            self.sliderLayout.addWidget(slider)

        self.graphicLayout = QtWidgets.QHBoxLayout()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Controller()
    w.show()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()

