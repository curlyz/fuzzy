# -*- coding: utf-8 -*-
"""
Example demonstrating a variety of scatter plot features.
"""



## Add path to library (just for examples; you do not need this)

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
pg.setConfigOption('background', [0,0,0])
pg.setConfigOption('foreground', 'k')
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('pyqtgraph example: ScatterPlot')

## create four areas to add plots
w2 = view.addViewBox()
print("Generating data, this takes a few seconds...")

## 2) Spots are transform-invariant, but not identical (top-right plot). 
## In this case, drawing is almsot as fast as 1), but there is more startup 
## overhead and memory usage since each spot generates its own pre-rendered 
## image.
n = 100
s2 = pg.ScatterPlotItem(size=1, pen=pg.mkPen('w'), pxMode=True)
pos = np.random.normal(size=(2,n))
spots = [{'pos': pos[:,i], 'data': 1, 'brush':'r', 'symbol': 1, 'size':5} for i in range(n)]
s2.addPoints(spots)
w2.addItem(s2)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

