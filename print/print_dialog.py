from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
import sys


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, flags=
        QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Печать изображений")
        self.printer = QtPrintSupport.QPrinter()
        self.printer.setPageOrientation(QtGui.QPageLayout.Landscape)
        self.file = None
        vbox = QtWidgets.QVBoxLayout()
        btnOpen = QtWidgets.QPushButton("&Открыть файл...")
        btnOpen.clicked.connect(self.openFile)
        vbox.addWidget(btnOpen)
        btnPageOptions = QtWidgets.QPushButton("Настройка &страницы...")
        btnPageOptions.clicked.connect(self.showPageOptions)
        vbox.addWidget(btnPageOptions)
        btnPrint = QtWidgets.QPushButton("&Печать...")
        btnPrint.clicked.connect(self.print)
        vbox.addWidget(btnPrint)
        self.setLayout(vbox)
        self.resize(200, 100)

    def openFile(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                          caption="Выберите графический файл",
                                                          filter="Графические файлы (*.bmp *.jpg *.png)")[0]

    def showPageOptions(self):
        pd = QtPrintSupport.QPageSetupDialog(self.printer, parent=self)
        pd.exec()

    def print(self):
        pd = QtPrintSupport.QPrintDialog(self.printer, parent=self)
        pd.setOptions(QtPrintSupport.QAbstractPrintDialog.PrintToFile |
                      QtPrintSupport.QAbstractPrintDialog.PrintSelection)
        if pd.exec() == QtWidgets.QDialog.Accepted:
            painter = QtGui.QPainter()
            painter.begin(self.printer)
            pixmap = QtGui.QPixmap(self.file)
            pixmap = pixmap.scaled(self.printer.width(),
                                   self.printer.height(), aspectRatioMode=
                                   QtCore.Qt.KeepAspectRatio)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
