import pyqtgraph as pg
import numpy as np
import math
from pyqtgraph.Qt import QtCore, QtGui



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


def onClick(evt):
    print(evt)

if __name__ == '__main__':
    position = [(-0.5,0), (0.5,0)]
    adjacency = [(0,1)]
    w = pg.GraphicsWindow()
    w.setWindowTitle('Title of the window') 
    v = w.addViewBox()
    v.setAspectLocked()
    g = Graph()
    v.addItem(g)

    g.setData(pos=np.array(position), adj=np.array(adjacency), pxMode=False, size=0.1)
    item = EllipseObject()
    item.sigClicked.connect(onClick)
    v.addItem(item)

    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()