from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeySequence
from quine import Quine
from functools import partial

class hoverLabel(QLabel):
	mouseMove = pyqtSignal()
	mouseLeave = pyqtSignal()

	def __init__(self, parent, s):
		super(hoverLabel, self).__init__(parent)
		self.setMouseTracking(True)
		self.setText(s)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.setFont(font)
		self.setAlignment(QtCore.Qt.AlignCenter)

	def mouseMoveEvent(self, event):
		self.setStyleSheet("color: rgb(108, 69, 76);")
		self.mouseMove.emit()

	def leaveEvent(self, event):
		self.setStyleSheet("")
		self.mouseLeave.emit()

	def on(self, x):  # Tambem recebe style extras
		style = "background-color: rgb(108, 69, 76); border-radius: 0px;"
		style += x
		self.setStyleSheet(style)

	def off(self):
		self.setStyleSheet("")

class janela2var(QMainWindow):
	def __init__(self, quine, parent):
		super(janela2var, self).__init__(parent)
		self.resize(800, 600)
		self.centralwidget = QtWidgets.QWidget(parent)
		self.centralwidget.setStyleSheet("background-color: rgb(215, 206, 199);")
		self.setWindowTitle("KARNAUGH")

		self.layout = QtWidgets.QGridLayout(self.centralwidget)
		self.layout.setContentsMargins(75, 75, 75, 75)

		self.hL = {}
		self.q = quine

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("puzzle.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(icon)

		self.mapaW()
		self.respostaW()
		self.backButton()

		self.setCentralWidget(self.centralwidget)
		QtCore.QMetaObject.connectSlotsByName(self)

	def newLabel(self, parent, text):
		label = QtWidgets.QLabel(parent)
		label.setText(text)
		label.setAlignment(QtCore.Qt.AlignCenter)

		font = QtGui.QFont()
		font.setPointSize(16)
		label.setFont(font)
		label.setMinimumSize(QtCore.QSize(100, 60))

		return label

	def mapaW(self): # Constroi widget do mapa
		widget = QtWidgets.QWidget(self.centralwidget)
		widget.setStyleSheet("background-color: rgb(192, 159, 128);" + 
		"border-radius: 20px;")

		layout = QtWidgets.QGridLayout(widget)
		layout.setSpacing(0)

		layout.addWidget(self.newLabel(widget, 'B' + '\u0305'), 0, 1)
		layout.addWidget(self.newLabel(widget, 'B'), 0, 2)
		layout.addWidget(self.newLabel(widget, 'A' + '\u0305'), 1, 0)
		layout.addWidget(self.newLabel(widget, 'B'), 2, 0)

		for i in range(0, 4):
			self.hL[i] = hoverLabel(widget, '0')

		k = 0

		for i in range(1, 3):
			for j in range(1, 3):
				layout.addWidget(self.hL[k], i, j)
				k += 1

		termos = self.q.getTermos()

		for i in termos:
			self.hL[i].setText('1')

		self.layout.addWidget(widget, 1, 1, 3, 3)

	def respostaW(self): # Constroi widget da resposta
		widget = QtWidgets.QWidget(self.centralwidget)
		widget.setStyleSheet("background-color: rgb(192, 159, 128);" +
		"border-radius: 20px;")

		layout = QtWidgets.QHBoxLayout(widget)
		res = self.q.getResposta()

		k = 0

		for i in res:
			if k != 0:
				layout.addWidget(self.newLabel(widget, '+'))

			label = hoverLabel(widget, self.q.toLiteral(i[0]))
			m = self.fillMapa(i[1])

			# Conecta com as labels do mapa

			for j in i[1]:
				style = ""

				if self.isTopLeft(m, j):
					style += "border-top-left-radius: 20px;"
				if self.isTopRight(m, j):
					style += "border-top-right-radius: 20px;"
				if self.isBottomLeft(m, j):
					style += "border-bottom-left-radius: 20px;"
				if self.isBottomRight(m, j):
					style += "border-bottom-right-radius: 20px;"

				label.mouseMove.connect(partial(self.hL[j].on, style))
				label.mouseLeave.connect(self.hL[j].off)

			layout.addWidget(label)
			k = 1

		self.layout.addWidget(widget, 4, 1, 1, 3)

	def backButton(self): # Adiciona botao de voltar
		button = QtWidgets.QPushButton(self.centralwidget)
		button.setGeometry(QtCore.QRect(5, 5, 50, 50))

		button.setStyleSheet("QPushButton{" +
        "background-color: rgb(118, 50, 63);" +
        "border: none;" + 
        "border-radius: 25px;" +
        "color:rgb(215, 206, 199);}" +
        "QPushButton:hover{" +
        "background-color: rgb(124, 59, 71);}" + 
        "QPushButton:pressed{" +
        "background-color: rgb(78, 41, 48);}")

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		button.setIcon(icon)
		button.clicked.connect(self.parent().recebeSinal)
		button.clicked.connect(self.close)

	def fillMapa(self, termos): # Metodo auxiliar para preencher um mapa
		idx = [[0, 1], [2, 3]]
		m = [[0, 0], [0, 0]]
		
		for t in termos:
			k = [(index, row.index(t)) for index, row in enumerate(idx) if t in row][0]
			m[k[0]][k[1]] = 1

		return m

	def isTopLeft(self, m, termo):
		if termo == 0:
			return True
		if (termo == 1 or termo == 2) and m[0][0] == 0:
			return True
		if termo == 3 and m[1][0] == 0 and m[0][1] == 0:
			return True

		return False

	def isTopRight(self, m, termo):
		if (termo == 0 or termo == 3) and m[0][1] == 0:
			return True
		if termo == 1:
			return True
		if termo == 2 and m[0][0] == 0 and m[1][1] == 0:
			return True
		
		return False

	def isBottomLeft(self, m, termo):
		if termo == 0 and m[1][0] == 0:
			return True
		if termo == 1 and m[0][0] == 0 and m[1][1] == 0:
			return True
		if termo == 2:
			return True
		if termo == 3 and m[1][0] == 0:
			return True

		return False

	def isBottomRight(self, m, termo):
		if termo == 0 and m[0][1] == 0 and m[1][0] == 0:
			return True
		if termo == 1 and m[1][1] == 0:
			return True
		if termo == 2 and m[1][1] == 0:
			return True
		if termo == 3:
			return True

		return False

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	ui = janela2var(Quine([0, 1, 3], 2))
	ui.show()
	sys.exit(app.exec_())


		