import sys
import csv
import configparser
import datetime
import re
import os

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

        # creates the connection to the files or creates them
        self.data_name = "data.ini"
        self.event_name = "events.csv"
        self.check_files()
        self.config.read(self.data_name)
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
        with open(self.event_name, 'a', newline="") as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow([is_event1, is_event2, log_time])

    def update_balance_text(self):
        # choose the appropriate color
        if self.balance > 0:
            self.L_money.setStyleSheet('color: rgb(34,139,34)')
        elif self.balance < 0:
            self.L_money.setStyleSheet('color: rgb(255, 0, 0)')
        else:
            self.L_money.setStyleSheet('color: rgb(0,0,0)')
        self.L_money.setText(f"{round(self.balance,2):.2f} €")

    def write_configfile(self):
        self.config['data']['balance'] = str(round(self.balance, 2))
        with open(self.data_name, 'w') as configfile:
            self.config.write(configfile)

    def check_files(self):
        if not os.path.isfile(self.data_name):
            self.create_datafile()
        if not os.path.isfile(self.event_name):
            self.create_eventfile()

    def create_datafile(self):
        self.config['data'] = {'balance': str(0), 'price': str(0.20)}
        with open(self.data_name, 'w') as configfile:
            self.config.write(configfile)

    def create_eventfile(self):
        with open(self.event_name, 'w', newline="") as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow(["is_event1", "is_event2", "log_time"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainScreen()
    w.show()
    # runs the app until the exit
    sys.exit(app.exec_())