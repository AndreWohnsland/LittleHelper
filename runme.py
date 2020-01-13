import sys
import csv
import configparser
import datetime
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from mainwindow import Ui_MainWindow



class MainScreen(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        """ Init function for the MainWindow Class. """
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)
        self.config = configparser.ConfigParser()
        self.config.read("data.ini")
        self.price = float(self.config['data']['price'])
        self.balance = float(self.config['data']['balance'])

        # connects the buttons
        self.PB_add.clicked.connect(self.add_one)
        self.PB_subtract.clicked.connect(self.subtract_one)
        self.PB_pay.clicked.connect(self.pay)
        self.PB_save.clicked.connect(self.save_date)

        # updates the balance
        self.update_balance_text()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

    def add_one(self):
        self.balance -= self.price
        self.write_configfile()
        self.update_balance_text()

    def subtract_one(self):
        self.balance += self.price
        self.write_configfile()
        self.update_balance_text()

    def pay(self):
        try:
            payment = float(self.LE_money.text())
            self.balance += payment
            self.write_configfile()
            self.LE_money.clear()
            self.update_balance_text()
        except:
            pass

    def save_date(self):
        is_event1 = 1 if self.CB_event1.isChecked() else 0
        is_event2 = 1 if self.CB_event2.isChecked() else 0
        log_time = self.dateTimeEdit.dateTime().toString(Qt.ISODate).replace("T", " ")
        with open('events.csv', 'a', newline="") as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow([is_event1, is_event2, log_time])

    def update_balance_text(self):
        self.L_money.setText(f"{round(self.balance,2):.2f} €")

    def write_configfile(self):
        self.config['data']['balance'] = str(round(self.balance, 2))
        with open("data.ini", 'w') as configfile:
            self.config.write(configfile)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainScreen()
    w.show()
    # runs the app until the exit
    sys.exit(app.exec_())