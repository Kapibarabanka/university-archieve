import math
import sys
import Counter


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class Ui_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("Лабораторная работа №2")
        self.resize(800, 500)
        self.center()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.create_window()
        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def count(self):
        self.counter.a = float(self.a_edit.text())
        self.counter.b = float(self.b_edit.text())
        self.counter.c = float(self.c_edit.text())
        self.counter.d = float(self.d_edit.text())
        self.counter.h1 = float(self.h1_edit.text())
        self.counter.h2 = float(self.h2_edit.text())
        self.counter.h3 = float(self.h3_edit.text())
        # if not self.counter.count_areas():
        #     raise ValueError("Сумма площадей ступенек не равна 1")
        if not self.counter.right_order():
            raise ValueError("Числа введены в неправильном порядке\nДолжно быть: a< b < c < d")
        answers = self.counter.count()
        self.tm_edit.setText(str(answers["tm"]))
        self.td_edit.setText(str(answers["td"]))
        self.pm_edit.setText(str(answers["pm"]))
        self.pd_edit.setText(str(answers["pd"]))


    def create_window(self):
        def data_changed():
            try:
                self.count()
            except Exception as ex:
                self.message = QtWidgets.QMessageBox.warning(self, 'Warning', ex.args[0])

        self.counter = Counter.Counter()

        self.a_lab = QtWidgets.QLabel("a = ")
        self.a_edit = QtWidgets.QLineEdit()
        self.a_edit.setText(str(self.counter.a))

        self.b_lab = QtWidgets.QLabel("b = ")
        self.b_edit = QtWidgets.QLineEdit()
        self.b_edit.setText(str(self.counter.b))

        self.c_lab = QtWidgets.QLabel("c = ")
        self.c_edit = QtWidgets.QLineEdit()
        self.c_edit.setText(str(self.counter.c))

        self.d_lab = QtWidgets.QLabel("d = ")
        self.d_edit = QtWidgets.QLineEdit()
        self.d_edit.setText(str(self.counter.d))

        self.h1_lab = QtWidgets.QLabel("h1 = ")
        self.h1_edit = QtWidgets.QLineEdit()
        self.h1_edit.setText(str(self.counter.h1))

        self.h2_lab = QtWidgets.QLabel("h2 = ")
        self.h2_edit = QtWidgets.QLineEdit()
        self.h2_edit.setText(str(self.counter.h2))

        self.h3_lab = QtWidgets.QLabel("h3 = ")
        self.h3_edit = QtWidgets.QLineEdit()
        self.h3_edit.setText(str(self.counter.h3))

        self.t_lab = QtWidgets.QLabel("Теоретические значения")
        self.t_lab.setFixedHeight(25)
        self.t_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.p_lab = QtWidgets.QLabel("Практические значения")
        self.p_lab.setFixedHeight(25)
        self.p_lab.setAlignment(QtCore.Qt.AlignCenter)

        self.tm_lab = QtWidgets.QLabel("M(t) = ")
        self.tm_edit = QtWidgets.QLineEdit()
        self.tm_edit.setReadOnly(True)

        self.td_lab = QtWidgets.QLabel("D(t) = ")
        self.td_edit = QtWidgets.QLineEdit()
        self.td_edit.setReadOnly(True)

        self.pm_lab = QtWidgets.QLabel("M(e) = ")
        self.pm_edit = QtWidgets.QLineEdit()
        self.pm_edit.setReadOnly(True)

        self.pd_lab = QtWidgets.QLabel("D(e) = ")
        self.pd_edit = QtWidgets.QLineEdit()
        self.pd_edit.setReadOnly(True)

        self.count_button = QtWidgets.QPushButton("Рассчитать")
        self.count_button.clicked.connect(data_changed)

        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(self.a_lab, 0, 0)
        grid.addWidget(self.a_edit, 0, 1)

        grid.addWidget(self.b_lab, 1, 0)
        grid.addWidget(self.b_edit, 1, 1)

        grid.addWidget(self.c_lab, 2, 0)
        grid.addWidget(self.c_edit, 2, 1)

        grid.addWidget(self.d_lab, 3, 0)
        grid.addWidget(self.d_edit, 3, 1)

        grid.addWidget(self.h1_lab, 0, 2)
        grid.addWidget(self.h1_edit, 0, 3)

        grid.addWidget(self.h2_lab, 1, 2)
        grid.addWidget(self.h2_edit, 1, 3)

        grid.addWidget(self.h3_lab, 2, 2)
        grid.addWidget(self.h3_edit, 2, 3)

        grid.addWidget(self.count_button, 3, 3)

        grid.addWidget(self.t_lab, 4, 1)
        grid.addWidget(self.p_lab, 4, 3)

        grid.addWidget(self.tm_lab, 5, 0)
        grid.addWidget(self.tm_edit, 5, 1)

        grid.addWidget(self.td_lab, 6, 0)
        grid.addWidget(self.td_edit, 6, 1)

        grid.addWidget(self.pm_lab, 5, 2)
        grid.addWidget(self.pm_edit, 5, 3)

        grid.addWidget(self.pd_lab, 6, 2)
        grid.addWidget(self.pd_edit, 6, 3)


app = QApplication(sys.argv)
ui = Ui_Form()
sys.exit(app.exec_())