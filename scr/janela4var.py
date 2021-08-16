from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal
from quine import Quine
from PyQt5.QtGui import QKeySequence
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

	def on(self, x):
		style = "background-color: rgb(108, 69, 76); border-radius: 0px;"
		style += x
		self.setStyleSheet(style)

	def off(self):
		self.setStyleSheet("")

class janela4var(QMainWindow):
	def __init__(self, quine, parent):
		super(janela4var, self).__init__(parent)
		self.resize(800, 600)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setStyleSheet("background-color: rgb(215, 206, 199);")
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(icon)

		self.idx = [[0, 1, 3, 2], [4, 5, 7, 6], [12, 13, 15, 14], [8, 9, 11, 10]]
		self.q = quine
		self.hL = {}
		self.mapaW()
		self.respostaW()
		self.backButton()
		self.spacers()

		self.setCentralWidget(self.centralwidget)
		QtCore.QMetaObject.connectSlotsByName(self)

	def mapaW(self): # Constroi widget do mapa
		widget = QtWidgets.QWidget(self.centralwidget)
		widget.setStyleSheet("background-color: rgb(192, 159, 128);" + 
		"border-radius: 20px;")
		gridLayout = QtWidgets.QGridLayout(widget)
		gridLayout.setSpacing(0)

		gridLayout.addWidget(self.newLabel(widget, 'C' + '\u0305' + 'D' + '\u0305'), 0, 1)
		gridLayout.addWidget(self.newLabel(widget, 'C' + '\u0305' + 'D'), 0, 2)
		gridLayout.addWidget(self.newLabel(widget, 'CD'), 0, 3)
		gridLayout.addWidget(self.newLabel(widget, 'C' + 'D' + '\u0305'), 0, 4)
		gridLayout.addWidget(self.newLabel(widget, 'A' + '\u0305' + 'B' + '\u0305'), 1, 0)
		gridLayout.addWidget(self.newLabel(widget, 'A' + '\u0305' + 'B'), 2, 0)
		gridLayout.addWidget(self.newLabel(widget, 'AB'), 3, 0)
		gridLayout.addWidget(self.newLabel(widget, 'A' + 'B' + '\u0305'), 4, 0)

		for i in range(0, 16):
			self.hL[i] = hoverLabel(widget, '0')

		v = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]
		k = 0

		for i in range(1, 5):
			for j in range(1, 5):
				gridLayout.addWidget(self.hL[v[k]], i, j, 1, 1)
				k += 1

		for i in self.q.termos:
			self.hL[i].setText('1')

		self.gridLayout.addWidget(widget, 1, 1, 5, 5)

	def newLabel(self, parent, s):
		label = QtWidgets.QLabel(parent)
		label.setText(s)
		font = QtGui.QFont()
		font.setPointSize(18)
		label.setFont(font)
		label.setAlignment(QtCore.Qt.AlignCenter)

		return label

	def respostaW(self): # Constroi widget da resposta
		widget = QtWidgets.QWidget(self.centralwidget)
		widget.setStyleSheet("background-color: rgb(192, 159, 128);" + 
		"border-radius: 20px;")

		horizontalLayout = QtWidgets.QHBoxLayout(widget)

		k = 0

		resposta = self.q.getResposta()

		for i in resposta:
			if k != 0:
				horizontalLayout.addWidget(self.newLabel(widget, '+'))

			label = hoverLabel(widget, self.q.toLiteral(i[0]))
			horizontalLayout.addWidget(label)

			m = self.fillMapa(i[1])

			for j in i[1]:
				style = ""
				ij = [(index, row.index(j)) for index, row in enumerate(self.idx) if j in row][0]

				if self.isTopLeft(m, ij[0], ij[1]):
					style += "border-top-left-radius: 20px;"
				if self.isTopRight(m, ij[0], ij[1]):
					style += "border-top-right-radius: 20px;"
				if self.isBottomLeft(m, ij[0], ij[1]):
					style += "border-bottom-left-radius: 20px;"
				if self.isBottomRight(m, ij[0], ij[1]):
					style += "border-bottom-right-radius: 20px;"

				if len(i[1]) == 1:
					style = "border-radius: 20px;"

				label.mouseMove.connect(partial(self.hL[j].on, style))
				label.mouseLeave.connect(self.hL[j].off)

			k = 1

		self.gridLayout.addWidget(widget, 7, 1, 1, 5)

	def backButton(self):
		btn = QtWidgets.QPushButton(self.centralwidget)
		btn.setGeometry(QtCore.QRect(5, 5, 50, 50))
		btn.setStyleSheet("QPushButton{" +
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
		btn.setIcon(icon)

		btn.clicked.connect(self.close)
		btn.clicked.connect(self.parent().recebeSinal)
		

	def spacers(self):
		s1 = QtWidgets.QSpacerItem(0, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		self.gridLayout.addItem(s1, 0, 0)

		s2 = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(s2, 1, 0)

		s3 = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(s3, 0, 6)

		s4 = QtWidgets.QSpacerItem(0, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		self.gridLayout.addItem(s4, 8, 0)

	# Metodos para auxiliar no design das bordas das labels - não leia se não pretende ter um surto psicótico

	def fillMapa(self, termos): 
		m = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		
		for t in termos:
			k = [(index, row.index(t)) for index, row in enumerate(self.idx) if t in row][0]
			m[k[0]][k[1]] = 1

		return m

	def isTopLeft(self, m, i, j):
		if i != 0 and j != 0 and m[i-1][j] == 0 and m[i][j-1] == 0:
			return True

		if i == 0:
			if j != 0:
				if m[i][j-1] == 0:
					if m[3][j] == 0:
						return True
					else:
						if m[1][j] == 1:
							return True
			else:
				if m[3][3] == 0:
					if m[0][3] == 0:
						if m[3][0] == 0:
							return True
					else:
						if m[0][1] == 1:
							return True

					if m[3][0] == 1 and m[2][0] == 1:
						return True

		if j == 0 and i != 0:
			if m[i-1][j] == 0:
				if m[i][3] == 0:
					return True
				else:
					if m[i][1] == 1:
						return True
		return False

	def isTopRight(self, m, i, j):
		if i != 0 and j != 3 and m[i-1][j] == 0 and m[i][j+1] == 0:
			return True

		if i == 0:
			if j != 3:
				if m[i][j+1] == 0:
					if m[3][j] == 0:
						return True
					else:
						if m[1][j] == 1:
							return True
			else:
				if m[3][0] == 0:
					if m[0][0] == 0:
						if m[3][3] == 0:
							return True
					else:
						if m[0][2] == 1:
							return True

					if m[3][3] == 1 and m[1][3] == 1:
						return True

		if j == 3 and i != 0:
			if m[i-1][j] == 0:
				if m[i][0] == 0:
					return True
				else:
					if m[i][2] == 1:
						return True
		return False

	def isBottomLeft(self, m, i, j):
		if i != 3 and j != 0 and m[i][j-1] == 0 and m[i+1][j] == 0:
			return True


		if i == 3:
			if j != 0:
				if m[3][j-1] == 0:
					if m[0][j] == 0:
						return True
					else:
						if m[2][j] == 1:
							return True
			else:
				if m[0][3] == 0:
					if m[3][3] == 0:
						if m[0][0] == 0:
							return True
					else:
						if m[3][1] == 1:
							return True

					if m[0][0] == 1 and m[2][0] == 1:
						return True

		if j == 0 and i != 3:
			if m[i+1][0] == 0:
				if m[i][3] == 0:
					return True
				else:
					if m[i][1] == 1:
						return True


		return False

	def isBottomRight(self, m, i, j):
		if i != 3 and j != 3 and m[i+1][j] == 0 and m[i][j+1] == 0:
			return True

		if j == 3:
			if i != 3:
				if m[i+1][3] == 0:
					if m[i][0] == 0:
						return True
					else:
						if m[i][2] == 1:
							return True
			else:
				if m[0][0] == 0:
					if m[3][0] == 0:
						if m[0][3] == 0:
							return True
					else:
						if m[3][2] == 1:
							return True

					if m[0][3] == 1 and m[2][3] == 1:
						return True

		if i == 3 and j != 3:
			if m[i][j+1] == 0:
				if m[0][j] == 0:
					return True
				else:
					if m[2][j] == 1:
						return True

		return False