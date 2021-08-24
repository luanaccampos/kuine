from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal
from quine import Quine
from PyQt5.QtGui import QKeySequence

class hoverLabel(QLabel):
	mouseMove = pyqtSignal()
	mouseLeave = pyqtSignal()

	def __init__(self, parent, s, size = 16):
		super(hoverLabel, self).__init__(parent)
		self.setMouseTracking(True)
		self.setText(s)
		self.setAlignment(QtCore.Qt.AlignCenter)
		font = QtGui.QFont()
		font.setPointSize(size)
		self.setFont(font)
		self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

	def mouseMoveEvent(self, event):
		self.setStyleSheet("color: rgb(108, 69, 76);")
		self.mouseMove.emit()

	def leaveEvent(self, event):
		self.setStyleSheet("")
		self.mouseLeave.emit()

	def on(self):
		self.setStyleSheet("background-color: rgb(108, 69, 76);")

	def off(self):
		self.setStyleSheet("")

class janelaQuine(QMainWindow):
	def __init__(self, quine, parent):
		super(janelaQuine, self).__init__(parent)
		self.resize(1000, 800)
		self.setWindowTitle("QUINE")
		self.setStyleSheet("QScrollBar:horizontal{" +
		"background-color: rgb(215, 206, 199);}" + 
		"QScrollBar::handle:horizontal{" + 
		"background-color: rgb(86, 86, 86);" + 
		"border-radius: 7px;}" +
		"QScrollBar::add-line:horizontal{" +
		"border: none;" + 
		"background: none;}" + 
		"QScrollBar::sub-line:horizontal{" + 
		"border: none;" + 
		"background: none;}" + 
		"QWidget{ background-color: rgb(215, 206, 199);}" +
		"QScrollBar:vertical{" + 
		"background-color: rgb(215, 206, 199);}" + 
		"QScrollBar::handle:vertical{" + 
		"background-color: rgb(86, 86, 86);" + 
		"border-radius: 7px;}" + 
		"QScrollBar::add-line:vertical{" + 
		"border: none;" + 
		"background: none;}" +
		"QScrollBar::sub-page{background-color: rgb(215, 206, 199);}" +
		"QScrollBar::add-page{background-color: rgb(215, 206, 199);}" +
		"QScrollBar::sub-line:vertical{" + 
		"border: none;" + 
		"background: none;}" + 
		"QTabWidget::pane{" +
		"border-top: 2px solid rgb(86, 86, 86);}"+
		"QTabBar::tab{" +
		"background: rgb(199, 199, 199);" +
		"border: 1px solid rgb(121, 121, 121);" + 
		"border-top-left-radius: 10px;" + 
		"border-top-right-radius: 4px;" + 
		"padding: 10px;" + 
		"margin-left: 5px;" + 
		"margin-right: 5px;" + 
		"color: rgb(121, 121, 121);" +
		"min-width: 14ex;}" + 
		"QTabBar::tab:selected{" + 
		"background: rgb(86, 86, 86);" + 
		"color: rgb(238, 238, 236);}")


		self.q = quine

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(icon)

		self.centralwidget = QtWidgets.QWidget(self)
		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout.setContentsMargins(60, 15, 0, 0)


		self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)

		self.hL = {} # hoverLabels
		self.Tabelas()
		self.Implicantes()
		self.backButton()
		self.verticalLayout.addWidget(self.tabWidget)
		self.setCentralWidget(self.centralwidget)

	def Tabelas(self): # Cria TAB com as tabelas
		widget = QtWidgets.QWidget()
		layout = QtWidgets.QVBoxLayout(widget)

		scrollArea = QtWidgets.QScrollArea(widget)
		scrollArea.setWidgetResizable(True)
		scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)

		scrollAreaConteudo = QtWidgets.QWidget()
		gridLayout = QtWidgets.QGridLayout(scrollAreaConteudo)

		quadros = self.q.getQuadros()
		coluna = 0

		for quadro in quadros:
			if len(quadro) > 0:
				gridLayout.addWidget(self.BinarioSetW(scrollAreaConteudo), 0, coluna, 1, 2)
				q = self.QuadroW(quadro, scrollAreaConteudo)
				gridLayout.addWidget(q[0], 1, coluna, q[1], 2)
				coluna += 2

		# Fazendo conexoes entre as hoverLabels

		grafo = self.q.getGrafo()

		for i in grafo:
			self.hL[i].mouseMove.connect(self.hL[grafo[i][0]].on)
			self.hL[i].mouseMove.connect(self.hL[grafo[i][1]].on)
			self.hL[i].mouseLeave.connect(self.hL[grafo[i][0]].off)
			self.hL[i].mouseLeave.connect(self.hL[grafo[i][1]].off)

		scrollArea.setWidget(scrollAreaConteudo)
		layout.addWidget(scrollArea)
		self.tabWidget.addTab(widget, "TABELAS")

	def BinarioSetW(self, parent): # Cria um widget com duas labels Binario - Set
		widget = QtWidgets.QWidget(parent)
		widget.setStyleSheet("QWidget{" + 
		"border-radius: 20px;" + 
		"color: rgb(215, 206, 199);}" +
		"QLabel{" + 
		"background-color: rgb(78, 41, 48);}")

		layout = QtWidgets.QHBoxLayout(widget)
		layout.addWidget(self.newLabel(widget, "BINÁRIO"))
		layout.addWidget(self.newLabel(widget, "SET"))

		return widget

	def newLabel(self, parent, text, width = 150):
		label = QtWidgets.QLabel(parent)
		label.setText(text)
		label.setAlignment(QtCore.Qt.AlignCenter)

		font = QtGui.QFont()
		font.setPointSize(16)
		label.setFont(font)
		label.setMinimumSize(QtCore.QSize(width, 60))

		return label

	def QuadroW(self, quadro, parent): # Cria um novo quadro retorna widget e qt de linhas utilizadas
		widget = QtWidgets.QWidget(parent)
		layout = QtWidgets.QGridLayout(widget)

		linha = 0

		for i in quadro:
			if len(quadro[i]) > 0:
				layout.addWidget(self.BoxW(quadro[i], widget), linha, 0, len(quadro[i]), 2)
				linha += len(quadro[i])

		return widget, linha

	def BoxW(self, termos, parent): # Cria uma caixa de um quadro, recebe uma lista de tuplas
		widget = QtWidgets.QWidget(parent)
		widget.setStyleSheet("background-color: rgb(192, 159, 128);" + 
		"border-radius: 20px;")

		gridLayout = QtWidgets.QGridLayout(widget)

		k = 0

		for i in termos:
			self.hL[i[0]] = hoverLabel(widget, i[0])
			gridLayout.addWidget(self.hL[i[0]], k, 0, 1, 1)
			gridLayout.addWidget(self.newLabel(widget, str(i[1])[10:-1]), k, 1, 1, 1)
			k += 1

		return widget

	def Implicantes(self):
		widget = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout(widget)

		scrollArea = QtWidgets.QScrollArea(widget)
		scrollArea.setWidgetResizable(True)
		scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)

		scrollAreaConteudo = QtWidgets.QWidget()
		gridLayout = QtWidgets.QGridLayout(scrollAreaConteudo)

		self.keyTermos = {} # Dicionario para facil acesso
		k = 1

		for i in self.q.getTermos():
			self.keyTermos[i] = k
			k += 1

		n = len(self.q.getTermos())


		gridLayout.addWidget(self.TermosW(self.q.getTermos()), 0, 2, 1, n)

		imps = self.q.getImplicantes()

		linha = 1
		f = True

		for imp in imps:
			gridLayout.addWidget(self.ImpW(imp, f), linha, 1, 1, n+1)
			linha += 1
			f = not f

		gridLayout.addWidget(self.RespostaW(), linha, 1, 1, n+1)

		scrollArea.setWidget(scrollAreaConteudo)
		layout.addWidget(scrollArea)
		self.tabWidget.addTab(widget, "IMPLICANTES") # Cria TAB com os implicantes

	def TermosW(self, termos):
		widget = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout(widget)

		widget.setStyleSheet("QLabel{" +
		"background-color: rgb(78, 41, 48);" + 
		"color: rgb(215, 206, 199);" + 
		"border-radius: 20px;}")

		for i in termos:
			layout.addWidget(self.newLabel(widget, str(i), 75))

		return widget # Cria widget com os termos

	def ImpW(self, imp, f): # Cria widget para implicante. Recebe tupla contendo binario e set de termos
		widget = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout(widget)

		style = "border-radius: 20px;"

		if f:
			style += "background-color: rgb(192, 159, 128);"
		else:
			style += "background-color: rgb(203, 180, 158);"

		widget.setStyleSheet(style)

		layout.addWidget(self.newLabel(widget, imp[0], 75))

		termos = self.q.getTermos()

		for i in termos:
			if i in imp[1]:
				layout.addWidget(hoverLabel(widget, "X"))
			else:
				layout.addWidget(self.newLabel(widget, "", 75))

		self.hL[imp[0]] = layout

		return widget

	def RespostaW(self):
		widget = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout(widget)

		widget.setStyleSheet("background: rgb(130, 130, 130);" + 
		"border-radius: 20px;")

		res = self.q.getResposta()

		k = 0

		for i in res:
			if k != 0:
				layout.addWidget(self.newLabel(widget, "+", 75))

			label = hoverLabel(widget, self.q.toLiteral(i[0]), 20)
			layout.addWidget(label)

			grid = self.hL[i[0]]

			# Conecta as hoverLabels

			for termo in i[1]:
				label2 = grid.itemAt(self.keyTermos[termo]).widget()
				label.mouseMove.connect(label2.on)
				label.mouseLeave.connect(label2.off)

			k = 1

		return widget

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

		btn.clicked.connect(self.parent().recebeSinal)
		btn.clicked.connect(self.close)
