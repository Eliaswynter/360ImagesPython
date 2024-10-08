import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Panoramic(QtWidgets.QWidget):
    def __init__(self, imagePath):
        QtWidgets.QWidget.__init__(self)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.source = QtGui.QPixmap(imagePath)
        self.pano = QtGui.QPixmap(self.source.width() * 3, self.source.height())
        self.center = self.pano.rect().center()
        self.delta = QtCore.QPointF()
        self.deltaTimer = QtCore.QTimer(interval=10, timeout=self.moveCenter)
        self.sourceRect = QtCore.QRect()
        self.setMaximumSize(self.source.size())
        qp = QtGui.QPainter(self.pano)
        qp.drawPixmap(0, 0, self.source)
        qp.drawPixmap(self.source.width(), 0, self.source)
        qp.drawPixmap(self.source.width() * 2, 0, self.source)
        qp.end()

    def moveCenter(self):
        if not self.delta:
            return
        self.center += self.delta

        if self.center.y() < self.sourceRect.height() * .5:
            self.center.setY(self.sourceRect.height() * .5)
        elif self.center.y() > self.source.height() - self.height() * .5:
            self.center.setY(self.source.height() - self.height() * .5)

        if self.center.x() < self.source.width() * .5:
            self.center.setX(self.source.width() * 1.5)
        elif self.center.x() > self.source.width() * 2.5:
            self.center.setX(self.source.width() * 1.5)
        self.sourceRect.moveCenter(self.center.toPoint())
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton:
            return
        delta = event.pos() - self.mousePos

        self.delta.setX(max(-25, min(25, delta.x() * .125)))
        self.delta.setY(max(-25, min(25, delta.y() * .125)))
        if not self.deltaTimer.isActive():
            self.deltaTimer.start()

    def mouseReleaseEvent(self, event):
        self.deltaTimer.stop()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawPixmap(self.rect(), self.pano, self.sourceRect)

    def resizeEvent(self, event):
        self.sourceRect.setSize(self.size())
        self.sourceRect.moveCenter(self.center)



app = QtWidgets.QApplication(sys.argv)
w = Panoramic('pano.jpg')
w.show()

sys.exit(app.exec_())