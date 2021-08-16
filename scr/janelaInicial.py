from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow
from PyQt5.QtGui import QKeySequence
import csv
from quine import Quine
from janela2var import janela2var
from janela3var import janela3var
from janela4var import janela4var
from janelaQuine import janelaQuine

class janelaInicial(QMainWindow):
	def __init__(self):
		super(janelaInicial, self).__init__()
		self.resize(800, 400)
		self.setWindowTitle("KUINE")
		self.setStyleSheet("QWidget{" +
		"background-color:rgb(215, 206, 199);}" + 
		"QPushButton{" +
		"background-color: rgb(118, 50, 63);" + 
		"border:none;" + 
		"color: rgb(215, 206, 199);" + 
		"border-radius: 20px;" + 
		"font: 16px;}" + 
		"QPushButton:hover{" + 
		"background-color: rgb(124, 59, 71);" +
		"border: none;" + 
		"color: rgb(215, 206, 199);}" +
		"QPushButton:pressed{" + 
		"background-color: rgb(78, 41, 48);" + 
		"border: none;" + 
		"color: rgb(215, 206, 199);}" + 
		"QLineEdit{" + 
		"border: 2px solid gray;" +
		"border-radius: 10px;" + 
		"padding: 0 8px;" + 
		"background: white;" + 
		"selection-background-color: darkgray;}")

		self.arquivo = False
		self.msg = QMessageBox(self)
		self.msg.setWindowTitle(" ")
		self.msg.setStyleSheet("QLabel{" + 
		"min-height:150 px; font-size: 24px;}" + 
		"QPushButton{" 
		"width: 100px; height:50px; font-size: 18px;}");

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(icon)

		self.centralwidget = QtWidgets.QWidget(self)
		self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.layout.setContentsMargins(50, 50, 50, 50)

		self.line()
		self.btns()

		self.setCentralWidget(self.centralwidget)
		QtCore.QMetaObject.connectSlotsByName(self)

	def line(self):
		widget = QtWidgets.QWidget(self.centralwidget)
		layout = QtWidgets.QHBoxLayout(widget)

		self.lineEdit = QtWidgets.QLineEdit(widget)
		self.lineEdit.setReadOnly(True)
		self.lineEdit.setMinimumSize(QtCore.QSize(0, 50))

		btn = QtWidgets.QPushButton(widget)
		btn.setText("...")
		btn.setMinimumSize(QtCore.QSize(75, 50))
		btn.clicked.connect(self.open)

		layout.addWidget(self.lineEdit)
		layout.addWidget(btn)

		self.layout.addWidget(widget, alignment=QtCore.Qt.AlignBottom)

	def btns(self):
		widget = QtWidgets.QWidget(self.centralwidget)
		layout = QtWidgets.QHBoxLayout(widget)

		btn1 = QtWidgets.QPushButton(widget)
		btn1.setText("KARNAUGH")
		btn1.setMinimumSize(QtCore.QSize(100, 80))
		btn1.clicked.connect(self.openKarnaugh)

		btn2 = QtWidgets.QPushButton(widget)
		btn2.setText("QUINE")
		btn2.setMinimumSize(QtCore.QSize(100, 80))
		btn2.clicked.connect(self.openQuine)

		layout.addWidget(btn1)
		layout.addWidget(btn2)

		self.layout.addWidget(widget, alignment=QtCore.Qt.AlignTop)

	def open(self):
		file = QtWidgets.QFileDialog(self)
		file.setNameFilter("CSV/TSV files (*.csv *.tsv)")

		if file.exec_():
			c = file.selectedFiles()
			f = open(c[0], 'r')

			if c[0].endswith('.csv'):
				w = csv.reader(f)
			else:
				w = csv.reader(f, delimiter= '\t')

			if self.valido(w):
				termos = []
				self.lineEdit.setText(c[0])

				for i in self.entrada:
					if self.entrada[i] == '1':
						termos.append(int(i, 2))

				self.q = Quine(termos, self.N)
				self.arquivo = True
			else:
				self.entrada.clear()
				self.msg.setText("Entrada inválida!")
				self.msg.setIcon(QMessageBox.Warning)
				self.msg.exec_()

	def valido(self, f):
		self.entrada = {}

		for i in f:
			n = len(i)
			x = ""
			self.N = n-1

			for j in range(n - 1):
				if i[j] == '1' or i[j] == '0':
					x += i[j]
				else:
					return False

			if i[n-1] == '1' or i[n-1] == '0':
				self.entrada[x] = i[n-1]
			else:
				return False

		return True

	def openKarnaugh(self):
		if self.arquivo: # se existe algum arquivo carregado

			if self.N == 2:
				self.k = janela2var(self.q, self)
			elif self.N == 3:
				self.k = janela3var(self.q, self)
			elif self.N == 4:
				self.k = janela4var(self.q, self)
			else:
				self.msg.setText("Entrada não suportada!")
				self.msg.setIcon(QMessageBox.Warning)
				self.msg.exec_()
				return

			self.hide()
			self.k.show()

		else:
			self.msg.setText("Entrada não carregada!")
			self.msg.setIcon(QMessageBox.Information)
			self.msg.exec_()

	def openQuine(self):
		if self.arquivo:	
			self.k = janelaQuine(self.q, self)
			self.close()
			self.k.show()
		else:
			self.msg.setText("Entrada não carregada!")
			self.msg.setIcon(QMessageBox.Information)
			self.msg.exec_()

	def recebeSinal(self):
		self.show()


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	ui = janelaInicial()
	ui.show()
	sys.exit(app.exec_())
