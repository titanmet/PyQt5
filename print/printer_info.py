from PyQt5 import QtCore, QtWidgets, QtPrintSupport
import sys


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent,
                                   flags=QtCore.Qt.Window)
        self.setWindowTitle("Класс QPrinterInfo")
        vbox = QtWidgets.QVBoxLayout()
        lblPrinter = QtWidgets.QLabel("Выберите &принтер")
        vbox.addWidget(lblPrinter)
        self.cboPrinter = QtWidgets.QComboBox()
        self.cboPrinter.addItems(
            QtPrintSupport.QPrinterInfo.availablePrinterNames())
        self.cboPrinter.currentTextChanged[str].connect(self.showData)
        lblPrinter.setBuddy(self.cboPrinter)
        vbox.addWidget(self.cboPrinter)
        self.txtOutput = QtWidgets.QTextEdit()
        self.txtOutput.setReadOnly(True)
        vbox.addWidget(self.txtOutput)
        self.setLayout(vbox)
        self.resize(400, 300)
        self.showData(self.cboPrinter.currentText())

    def showData(self, name):
        printer = QtPrintSupport.QPrinterInfo.printerInfo(name)
        s = "Название: " + name + "\n\n"
        if printer.isDefault():
            s += "Принтер по умолчанию\n"
        s2 = printer.makeAndModel()
        if s != s2:
            s += "Полное название: " + s2 + "\n"
        s2 = printer.description()
        if s != s2:
            s += "Описание: " + s2 + "\n"
        if printer.isRemote():
            s += "Сетевой принтер\n"
        s2 = printer.location()
        if s2:
            s += "Расположение: " + s2 + "\n"
        s += "\n"
        n = printer.state()
        if n == QtPrintSupport.QPrinter.Idle:
            s2 = "простаивает"
        elif n == QtPrintSupport.QPrinter.Active:
            s2 = "идёт печать"
        elif n == QtPrintSupport.QPrinter.Aborted:
            s2 = "печать прервана"
        elif n == QtPrintSupport.QPrinter.Error:
            s2 = "возникла ошибка"
        s += "Состояние: " + s2 + "\n\n"
        s += "Размер бумаги по умолчанию: " + printer.defaultPageSize().name() + "\n"
        s2 = ", ".join([s.name() for s in printer.supportedPageSizes()])
        if printer.supportsCustomPageSizes():
            s2 += ", произвольные размеры"
        s += "Поддерживаемые размеры бумаги: " + s2 + "\n"
        s += "Минимальный размер бумаги: " + \
             printer.minimumPhysicalPageSize().name() + "\n"
        s += "Максимальный размер бумаги: " + \
             printer.maximumPhysicalPageSize().name() + "\n\n"
        s += "Режим двусторонней печати по умолчанию: " + \
             self._getDuplexModeName(printer.defaultDuplexMode()) + "\n"
        s2 = ""
        for m in printer.supportedDuplexModes():
            if s2:
                s2 += ", "
            s2 += self._getDuplexModeName(m)
        s += "Поддерживаемые режимы двухсторонней печати: " + s2 + "\n\n"
        s2 = ", ".join([str(r) for r in printer.supportedResolutions()])
        s += "Поддерживаемые разрешения, точек/дюйм: " + s2
        self.txtOutput.setText(s)

    def _getDuplexModeName(self, ident):
        if ident == QtPrintSupport.QPrinter.DuplexNone:
            return "односторонняя печать"
        elif ident == QtPrintSupport.QPrinter.DuplexAuto:
            return "двухсторонняя печать с автоматическим выбором стороны листа"
        elif ident == QtPrintSupport.QPrinter.DuplexLongSide:
            return "двухсторонняя печать с переворотом листа вокруг длинной стороны"
        elif ident == QtPrintSupport.QPrinter.DuplexShortSide:
            return "двухсторонняя печать с переворотом листа вокруг короткой стороны"


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
