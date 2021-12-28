# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

from Automata import generateNFA, nfa_convert_to_dfa
from Exp2NFA import ExpToNFA
# from Lex import Draw

from minimizer import DFA


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("词法分析GUI")
        MainWindow.resize(700, 1000)
        MainWindow.setStyleSheet("background-color:rgb(255, 255, 255)")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.inputLabel = QtWidgets.QLabel(self.centralwidget)
        self.inputLabel.setGeometry(QtCore.QRect(40, 30, 100, 30))
        self.inputLabel.setObjectName("inputLabel")

        self.inputLine = QtWidgets.QLineEdit(self.centralwidget)
        self.inputLine.setGeometry(QtCore.QRect(160, 30, 241, 30))
        self.inputLine.setObjectName("inputLine")

        self.submit = QtWidgets.QPushButton(self.centralwidget)
        self.submit.setGeometry(QtCore.QRect(190, 80, 30, 17))
        self.submit.setObjectName("submit")
        self.submit.clicked.connect(self.draw3Pic) # 绘制结果图片

        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(250, 80, 30, 17))
        self.clear.setObjectName("clear")
        self.clear.clicked.connect(self.clearInput) # 清空输入

        self.NFA = QtWidgets.QLabel(self.centralwidget)
        self.NFA.setGeometry(QtCore.QRect(50, 160, 120, 300))
        self.NFA.setObjectName("NFA")

        self.DFA = QtWidgets.QLabel(self.centralwidget)
        self.DFA.setGeometry(QtCore.QRect(250, 160, 120, 300))
        self.DFA.setObjectName("DFA")

        self.minDFA = QtWidgets.QLabel(self.centralwidget)
        self.minDFA.setGeometry(QtCore.QRect(450, 160, 120, 300))
        self.minDFA.setObjectName("minDFA")

        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(100, 120, 80, 20))
        self.label_1.setObjectName("label_1")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(310, 120, 80, 20))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(520, 120, 80, 20))
        self.label_3.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.inputLabel.setText(_translate("MainWindow", "请输入正规表达式："))
        self.submit.setText(_translate("MainWindow", "确定"))
        self.clear.setText(_translate("MainWindow", "清除"))
        self.NFA.setText(_translate("MainWindow", ""))
        self.DFA.setText(_translate("MainWindow", ""))
        self.minDFA.setText(_translate("MainWindow", ""))
        self.label_1.setText(_translate("MainWindow", "正规式转NFA"))
        self.label_2.setText(_translate("MainWindow", "NFA转DFA"))
        self.label_3.setText(_translate("MainWindow", "化简DFA"))


    # 清空输入
    def clearInput(self):
        self.inputLine.setText('')
        self.NFA.setPixmap(QPixmap(""))
        self.DFA.setPixmap(QPixmap(""))
        self.minDFA.setPixmap(QPixmap(""))

    # 绘制三幅图
    def draw3Pic(self):
        self.draw3Pic()

        pix_1= QPixmap('NFA.gv.png')
        self.NFA.setPixmap(pix_1)
        self.NFA.setScaledContents(True)

        pix_2 = QPixmap('NFA.gv.png')
        self.DFA.setPixmap(pix_2)
        self.DFA.setScaledContents(True)

        pix_3 = QPixmap('NFA.gv.png')
        self.minDFA.setPixmap(pix_3)
        self.minDFA.setScaledContents(True)

    def reg2NFA(self):
        # 获取输入的正规式
        regular=self.inputLine.text()

        # Regular to NFA
        iden = ExpToNFA(1)
        bs, trans, ends = iden.convert(regular)
        # Draw(trans,ends,'img/Exp2NFA')

        # NFA to DFA
        nfa = generateNFA(trans)
        dfa = nfa_convert_to_dfa(nfa)
        dfa.draw('img/NFA2DFA')

        # minimize DFA
        dfa=DFA.generateDFA(dfa)
        dfa.draw('img/minDFA')

class SetUp(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("词法分析GUI")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SetUp()

    win.show()
    sys.exit(app.exec_())

