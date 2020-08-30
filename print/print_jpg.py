from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
import sys

app = QtWidgets.QApplication(sys.argv)
# Создаем принтер
printer = QtPrintSupport.QPrinter()
# Для целей отладки лучше выводить документ не на принтер,
# а в файл, в формате PDF. Чтобы сделать это, достаточно
# раскомментировать следующую строчку кода
printer.setOutputFileName("output.pdf")
# Создаем поверхность рисования и привязываем ее к принтеру
painter = QtGui.QPainter()
painter.begin(printer)
# Рисуем рамку вокруг страницы
pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.blue), 5, style = QtCore.Qt.DotLine)
painter.setPen(pen)
painter.setBrush(QtCore.Qt.NoBrush)
painter.drawRect(0, 0, printer.width(), printer.height())
# Выводим надпись
color = QtGui.QColor(QtCore.Qt.black)
painter.setPen(QtGui.QPen(color))
painter.setBrush(QtGui.QBrush(color))
font = QtGui.QFont("Verdana", pointSize=42)
painter.setFont(font)
painter.drawText(10, printer.height() // 2 - 100, printer.width() - 20, 50, QtCore.Qt.AlignCenter | QtCore.Qt.TextDontClip, "QPrinter")
# Изменяем ориентацию страницы. Сделать это нужно перед вызовом
# метода newPage()
printer.setPageOrientation(QtGui.QPageLayout.Landscape)
# Переходим на новую страницу
printer.newPage()
# Выводим изображение
pixmap = QtGui.QPixmap("img.jpg")
pixmap = pixmap.scaled(printer.width(), printer.height(), aspectRatioMode = QtCore.Qt.KeepAspectRatio)
painter.drawPixmap(0, 0, pixmap)
painter.end()
