# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("QGroupBox")
window.resize(200, 80)
mainbox = QtWidgets.QVBoxLayout()
radio1 = QtWidgets.QRadioButton("&Да")
radio2 = QtWidgets.QRadioButton("&Нет")
box = QtWidgets.QGroupBox("&Вы знаете язык Python?")  # Объект группы
hbox = QtWidgets.QHBoxLayout()  # Контейнер для группы
hbox.addWidget(radio1)  # Добавляем компоненты
hbox.addWidget(radio2)
box.setLayout(hbox)  # Передаем ссылку на контейнер
mainbox.addWidget(box)  # Добавляем группу в главный контейнер
window.setLayout(mainbox)  # Передаем ссылку на главный контейнер в окно
radio1.setChecked(True)  # Выбираем первый переключатель
window.show()
sys.exit(app.exec_())

