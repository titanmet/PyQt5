from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtMultimediaWidgets
import sys


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent, flags=QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Видеопроигрыватель")
        self.mplPlayer = QtMultimedia.QMediaPlayer()
        self.mplPlayer.setVolume(50)
        self.mplPlayer.mediaStatusChanged.connect(self.initPlayer)
        self.mplPlayer.stateChanged.connect(self.setPlayerState)
        vbox = QtWidgets.QVBoxLayout()
        btnOpen = QtWidgets.QPushButton("&Открыть файл...")
        btnOpen.clicked.connect(self.openFile)
        vbox.addWidget(btnOpen)
        vwg = QtMultimediaWidgets.QVideoWidget()
        vwg.setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
        self.mplPlayer.setVideoOutput(vwg)
        vbox.addWidget(vwg)
        self.sldPosition = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sldPosition.setMinimum(0)
        self.sldPosition.valueChanged.connect(self.mplPlayer.setPosition)
        self.mplPlayer.positionChanged.connect(self.sldPosition.setValue)
        self.sldPosition.setEnabled(False)
        vbox.addWidget(self.sldPosition)
        hbox = QtWidgets.QHBoxLayout()
        self.btnPlay = QtWidgets.QPushButton("&Пуск")
        self.btnPlay.clicked.connect(self.mplPlayer.play)
        self.btnPlay.setEnabled(False)
        hbox.addWidget(self.btnPlay)
        self.btnPause = QtWidgets.QPushButton("П&ауза")
        self.btnPause.clicked.connect(self.mplPlayer.pause)
        self.btnPause.setEnabled(False)
        hbox.addWidget(self.btnPause)
        self.btnStop = QtWidgets.QPushButton("&Стоп")
        self.btnStop.clicked.connect(self.mplPlayer.stop)
        self.btnStop.setEnabled(False)
        hbox.addWidget(self.btnStop)
        vbox.addLayout(hbox)
        hbox = QtWidgets.QHBoxLayout()
        lblVolume = QtWidgets.QLabel("&Громкость")
        hbox.addWidget(lblVolume)
        sldVolume = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sldVolume.setRange(0, 100)
        sldVolume.setTickPosition(QtWidgets.QSlider.TicksAbove)
        sldVolume.setTickInterval(10)
        sldVolume.setValue(50)
        lblVolume.setBuddy(sldVolume)
        sldVolume.valueChanged.connect(self.mplPlayer.setVolume)
        hbox.addWidget(sldVolume)
        btnMute = QtWidgets.QPushButton("&Тихо!")
        btnMute.setCheckable(True)
        btnMute.toggled.connect(self.mplPlayer.setMuted)
        hbox.addWidget(btnMute)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.resize(600, 600)

    def openFile(self):
        file = QtWidgets.QFileDialog.getOpenFileUrl(parent=self,
                                                    caption="Выберите видеофайл",
                                                    filter="Видеофайлы (*.avi *.mp4)")
        self.mplPlayer.setMedia(QtMultimedia.QMediaContent(file[0]))

    def initPlayer(self, state):
        if state == QtMultimedia.QMediaPlayer.LoadedMedia:
            # После загрузки файла подготавливаем проигрыватель
            # для его воспроизведения
            self.mplPlayer.stop()
            self.btnPlay.setEnabled(True)
            self.sldPosition.setEnabled(True)
            self.sldPosition.setMaximum(self.mplPlayer.duration())
        elif state == QtMultimedia.QMediaPlayer.EndOfMedia:
            # По окончании воспроизведения файла возвращаем
            # проигрыватель в изначальное состояние
            self.mplPlayer.stop()
        elif state == QtMultimedia.QMediaPlayer.NoMedia or state == QtMultimedia.QMediaPlayer.InvalidMedia:
            # Если файл не был загружен, отключаем компоненты,
            #  управляющие воспроизведением
            self.sldPosition.setValue(0)
            self.sldPosition.setEnabled(False)
            self.btnPlay.setEnabled(False)
            self.btnPause.setEnabled(False)
            self.btnStop.setEnabled(False)

        # В зависимости от того, воспроизводится ли файл, поставлен
        # ли он на паузу или остановлен, делаем соответствующие кнопки
        # доступными или недоступными
    def setPlayerState(self, state):
        if state == QtMultimedia.QMediaPlayer.StoppedState:
            self.sldPosition.setValue(0)
            self.btnPause.setEnabled(False)
            self.btnStop.setEnabled(False)
        elif state == QtMultimedia.QMediaPlayer.PlayingState:
            self.btnPause.setEnabled(True)
            self.btnStop.setEnabled(True)
        elif state == QtMultimedia.QMediaPlayer.PausedState:
            self.btnPause.setEnabled(False)
            self.btnStop.setEnabled(True)


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
