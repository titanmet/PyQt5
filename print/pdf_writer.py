from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
import sys

app = QtWidgets.QApplication(sys.argv)
writer = QtGui.QPdfWriter("output.pdf")
writer.setCreator("titanmet")
writer.setTitle("Тест")
# Заодно поэкспериментируем с указанием параметров бумаги с помощью
# класса QPageLayout
layout = QtGui.QPageLayout()
layout.setPageSize(QtGui.QPageSize(QtGui.QPageSize.A5))
layout.setOrientation(QtGui.QPageLayout.Portrait)
writer.setPageLayout(layout)
painter = QtGui.QPainter()
painter.begin(writer)
color = QtGui.QColor(QtCore.Qt.black)
painter.setPen(QtGui.QPen(color))
painter.setBrush(QtGui.QBrush(color))
font = QtGui.QFont("Verdana", pointSize=42)
painter.setFont(font)
painter.drawText(10, writer.height() // 2 - 50, writer.width() - 20,
                 50, QtCore.Qt.AlignCenter | QtCore.Qt.TextDontClip, "QPdfWriter")
layout.setOrientation(QtGui.QPageLayout.Landscape)
writer.setPageLayout(layout)
writer.newPage()
pixmap = QtGui.QPixmap("img.jpg")
pixmap = pixmap.scaled(writer.width(), writer.height(),
                       aspectRatioMode=QtCore.Qt.KeepAspectRatio)
painter.drawPixmap(0, 0, pixmap)
painter.end()
