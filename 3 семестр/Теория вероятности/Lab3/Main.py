import math
import sys
import Counter
import traceback


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class Ui_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("Лабораторная работа №3")
        self.resize(800, 800)
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
        self.counter.step = float(self.step_edit.text())
        self.counter.n = int(self.n_edit.text())
        # if not self.counter.count_areas():
        #     raise ValueError("Сумма площадей ступенек не равна 1")
        self.wait_lab.setText("Wait, please")
        self.counter.do_lab()
        self.m_x_p_edit.setText(str(self.counter.m_x))
        self.m_y_p_edit.setText(str(self.counter.m_y))
        self.s_x_p_edit.setText(str(self.counter.sigma_x))
        self.s_y_p_edit.setText(str(self.counter.sigma_y))
        self.cor_p_edit.setText(str(self.counter.correlation))

        self.m_x_t_edit.setText(str(self.counter.m_x_t))
        self.m_y_t_edit.setText(str(self.counter.m_y_t))
        self.s_x_t_edit.setText(str(self.counter.sigma_x_t))
        self.s_y_t_edit.setText(str(self.counter.sigma_y_t))
        self.cor_t_edit.setText(str(self.counter.correlation_t))
        print("Ready!")

    def create_window(self):
        def data_changed():
            try:
                self.count()
            except Exception as ex:
                self.message = QtWidgets.QMessageBox.warning(self, 'Warning', ex.args[0])
                traceback.print_exc()

        self.counter = Counter.Counter()

        self.a_lab = QtWidgets.QLabel("a = ")
        self.a_edit = QtWidgets.QLineEdit()
        self.a_edit.setText(str(self.counter.a))

        self.b_lab = QtWidgets.QLabel("b = ")
        self.b_edit = QtWidgets.QLineEdit()
        self.b_edit.setText(str(self.counter.b))

        self.step_lab = QtWidgets.QLabel("step = ")
        self.step_edit = QtWidgets.QLineEdit()
        self.step_edit.setText(str(self.counter.step))

        self.n_lab = QtWidgets.QLabel("n = ")
        self.n_edit = QtWidgets.QLineEdit()
        self.n_edit.setText(str(self.counter.n))

        self.m_x_t_lab = QtWidgets.QLabel("Mx = ")
        self.m_x_t_edit = QtWidgets.QLineEdit()


        self.m_y_t_lab = QtWidgets.QLabel("My = ")
        self.m_y_t_edit = QtWidgets.QLineEdit()


        self.s_x_t_lab = QtWidgets.QLabel("s_x = ")
        self.s_x_t_edit = QtWidgets.QLineEdit()


        self.s_y_t_lab = QtWidgets.QLabel("s_y = ")
        self.s_y_t_edit = QtWidgets.QLineEdit()


        self.cor_t_lab = QtWidgets.QLabel("p = ")
        self.cor_t_edit = QtWidgets.QLineEdit()


        self.t_lab = QtWidgets.QLabel("Теоретические значения")
        self.t_lab.setFixedHeight(25)
        self.t_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.p_lab = QtWidgets.QLabel("Практические значения")
        self.p_lab.setFixedHeight(25)
        self.p_lab.setAlignment(QtCore.Qt.AlignCenter)

        self.m_x_p_lab = QtWidgets.QLabel("Mx = ")
        self.m_x_p_edit = QtWidgets.QLineEdit()
        #self.m_x_p_edit.setReadOnly(True)

        self.m_y_p_lab = QtWidgets.QLabel("My = ")
        self.m_y_p_edit = QtWidgets.QLineEdit()
        #self.m_y_p_edit.setReadOnly(True)

        self.s_x_p_lab = QtWidgets.QLabel("s_x = ")
        self.s_x_p_edit = QtWidgets.QLineEdit()
        #self.s_x_p_edit.setReadOnly(True)

        self.s_y_p_lab = QtWidgets.QLabel("s_y = ")
        self.s_y_p_edit = QtWidgets.QLineEdit()
        #self.s_y_p_edit.setReadOnly(True)

        self.cor_p_lab = QtWidgets.QLabel("p = ")
        self.cor_p_edit = QtWidgets.QLineEdit()


        self.count_button = QtWidgets.QPushButton("Рассчитать")
        self.count_button.clicked.connect(data_changed)

        self.wait_lab = QtWidgets.QLineEdit()


        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(self.a_lab, 0, 0)
        grid.addWidget(self.a_edit, 0, 1)

        grid.addWidget(self.b_lab, 1, 0)
        grid.addWidget(self.b_edit, 1, 1)

        grid.addWidget(self.step_lab, 0, 2)
        grid.addWidget(self.step_edit,0, 3)

        grid.addWidget(self.n_lab, 1, 2)
        grid.addWidget(self.n_edit, 1, 3)

        grid.addWidget(self.t_lab, 2, 1)
        grid.addWidget(self.p_lab, 2, 3)

        grid.addWidget(self.m_x_t_lab, 3, 0)
        grid.addWidget(self.m_x_t_edit, 3, 1)

        grid.addWidget(self.m_y_t_lab, 4, 0)
        grid.addWidget(self.m_y_t_edit, 4, 1)

        grid.addWidget(self.s_x_t_lab, 5, 0)
        grid.addWidget(self.s_x_t_edit, 5, 1)

        grid.addWidget(self.s_y_t_lab, 6, 0)
        grid.addWidget(self.s_y_t_edit, 6, 1)

        grid.addWidget(self.cor_t_lab, 7, 0)
        grid.addWidget(self.cor_t_edit, 7, 1)

        grid.addWidget(self.m_x_p_lab, 3, 2)
        grid.addWidget(self.m_x_p_edit, 3, 3)

        grid.addWidget(self.m_y_p_lab, 4, 2)
        grid.addWidget(self.m_y_p_edit, 4, 3)

        grid.addWidget(self.s_x_p_lab, 5, 2)
        grid.addWidget(self.s_x_p_edit, 5, 3)

        grid.addWidget(self.s_y_p_lab, 6, 2)
        grid.addWidget(self.s_y_p_edit, 6, 3)

        grid.addWidget(self.cor_p_lab, 7, 2)
        grid.addWidget(self.cor_p_edit, 7, 3)

        grid.addWidget(self.count_button, 8, 0, 1, 4)
        #grid.addWidget(self.wait_lab, 8, 2)




app = QApplication(sys.argv)
ui = Ui_Form()
sys.exit(app.exec_())