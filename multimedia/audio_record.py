from PyQt5 import QtCore, QtWidgets, QtMultimedia
import sys, os

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent, flags = QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Запись звука")
        # Инициализируем подсистему для записи звука
        self.ardRecorder = QtMultimedia.QAudioRecorder()
        # Устанавливаем максимальную громкость
        self.ardRecorder.setVolume(100)
        # Звук будет сохраняться в файле record.wav, находящемся в
        # той же папке, где хранится программа
        fn = QtCore.QUrl.fromLocalFile(os.path.abspath("record.wav"))
        self.ardRecorder.setOutputLocation(fn)
        # Устанавливаем звуковой вход по умолчанию
        self.ardRecorder.setAudioInput(self.ardRecorder.defaultAudioInput())
        # Указываем формат файла WAV
        self.ardRecorder.setContainerFormat("audio/x-wav")
        # Задаем параметры кодирования звука
        aes = QtMultimedia.QAudioEncoderSettings()
        aes.setCodec("audio/pcm")
        aes.setSampleRate(8000)
        aes.setChannelCount(1)
        aes.setEncodingMode(QtMultimedia.QMultimedia.ConstantQualityEncoding)
        aes.setQuality(QtMultimedia.QMultimedia.VeryLowQuality)
        self.ardRecorder.setAudioSettings(aes)
        self.ardRecorder.statusChanged.connect(self.initRecorder)
        self.ardRecorder.durationChanged.connect(self.showDuration)
        # Создаем компоненты для запуска, приостановки и остановки
        # записи звука и регулирования его уровня
        vbox = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        self.btnRecord = QtWidgets.QPushButton("&Запись")
        self.btnRecord.clicked.connect(self.ardRecorder.record)
        hbox.addWidget(self.btnRecord)
        self.btnPause = QtWidgets.QPushButton("П&ауза")
        self.btnPause.clicked.connect(self.ardRecorder.pause)
        self.btnPause.setEnabled(False)
        hbox.addWidget(self.btnPause)
        self.btnStop = QtWidgets.QPushButton("&Стоп")
        self.btnStop.clicked.connect(self.ardRecorder.stop)
        self.btnStop.setEnabled(False)
        hbox.addWidget(self.btnStop)
        vbox.addLayout(hbox)
        hbox = QtWidgets.QHBoxLayout()
        lblVolume = QtWidgets.QLabel("&Уровень записи")
        hbox.addWidget(lblVolume)
        sldVolume = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sldVolume.setRange(0, 100)
        sldVolume.setTickPosition(QtWidgets.QSlider.TicksAbove)
        sldVolume.setTickInterval(10)
        sldVolume.setValue(100)
        lblVolume.setBuddy(sldVolume)
        sldVolume.valueChanged.connect(self.ardRecorder.setVolume)
        hbox.addWidget(sldVolume)
        vbox.addLayout(hbox)
        # Создаем надпись, в которую будет выводиться состояние
        # программы
        self.lblStatus = QtWidgets.QLabel("Готово")
        vbox.addWidget(self.lblStatus)
        self.setLayout(vbox)
        self.resize(300, 100)

    # В зависимости от состояния записи звука делаем нужные
    # кнопки доступными или, напротив, недоступными и выводим
    # соответствующий текст в надписи
    def initRecorder(self, status):
        if status == QtMultimedia.QMediaRecorder.RecordingStatus:
            self.btnRecord.setEnabled(False)
            self.btnPause.setEnabled(True)
            self.btnStop.setEnabled(True)
            self.lblStatus.setText("Запись")
        elif status == QtMultimedia.QMediaRecorder.PausedStatus:
            self.btnRecord.setEnabled(True)
            self.btnPause.setEnabled(False)
            self.lblStatus.setText("Пауза")
        elif status == QtMultimedia.QMediaRecorder.FinalizingStatus:
            self.btnRecord.setEnabled(True)
            self.btnPause.setEnabled(False)
            self.btnStop.setEnabled(False)
            self.lblStatus.setText("Готово")

    # Выводим продолжительность записанного звука
    def showDuration(self, duration):
        self.lblStatus.setText("Записано " + str(duration // 1000) + " секунд")

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
