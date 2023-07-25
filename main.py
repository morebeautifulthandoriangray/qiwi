

# currency_rates = input("Введите код валюты: ")
# date = input("Введите дату: ")
#
# get_xml = requests.get(
#     'http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s/%s/%s' % (day, month, year)
# )

import sys
import requests
import xml.etree.ElementTree as ET
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QApplication, QComboBox, QPushButton, QMainWindow, QTextEdit, QLineEdit,
                             QVBoxLayout)
from PyQt6.QtGui import QPixmap, QFont, QIntValidator


class CBR_API(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.days()
        self.month()
        self.year()
        self.code_v()
        self.date()

        # Создаем кнопку "OK".
        ok_button = QPushButton('ОК', self)
        ok_button.resize(50, 25)
        ok_button.move(220, 250)

        # Каждый клик кнопки вызывает метод "makeRequest"
        ok_button.clicked.connect(self.makeRequest)

        self.setFixedSize(500, 500)
        self.setWindowTitle('Converter')
        self.show()



    def date(self):
        # Заголовок списка.
        day_label = QLabel("Дата", self)
        day_label.move(120, 300)

        self.input = QLineEdit(self)
        self.input.move(180, 300)
    def code_v(self):
        # Заголовок списка.
        day_label = QLabel("Валюта", self)
        day_label.move(20, 250)

        self.input = QLineEdit(self)
        self.input.move(80, 250)




    def days(self):
        """
        Выпадающий список дней.
        """

        # Создаем выпадающий список.
        self.days_combo = QComboBox(self)

        # Заголовок списка.
        day_label = QLabel("День", self)
        day_label.move(20, 170)

        for day in range(1, 31):
            # Наполняем список.
            self.days_combo.addItem('%d' % day)

        # Фиксируем список.
        self.days_combo.move(20, 200)

    def month(self):
        """
        Выпадающий список месяцев.
        """

        # Создаем выпадающий список.
        self.month_combo = QComboBox(self)

        # Заголовок списка.
        month_label = QLabel("Месяц", self)
        month_label.move(80, 170)

        for month_num in range(1, 13):
            # Наполняем список.
            self.month_combo.addItem('%d' % month_num)

        # Фиксируем список.
        self.month_combo.move(80, 200)

    def year(self):
        """
        Выпадающий список годов.
        """

        # Создаем выпадающий список.
        self.year_combo = QComboBox(self)

        # Заголовок списка.
        month_label = QLabel("Год", self)
        month_label.move(140, 170)

        for year_num in range(2000, 2018):
            # Наполняем список.
            self.year_combo.addItem('%d' % year_num)

        # Фиксируем список.
        self.year_combo.move(140, 200)


        self.dollar_value = QLabel("0 руб.", self)

        self.dollar_value.move(300, 250)


    def getResult(self, day, month, year):
        result = {'val': 0}
        try:
            get_xml = requests.get(
                'http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s/%s/%s' % (day, month, year)
            )
            structure = ET.fromstring(get_xml.content)
        except:
            return result

        try:
            # Поиск курса
            val = structure.find("./*[@ID='R01235']/Value")
            result['val'] = val.text.replace(',', '.')
        except:
            result['val'] = 'x'

        return result

    def makeRequest(self):
        """
        После нажатия на "ОК" выполняется запрос к API с выбранными данными.
        """

        # Получаем текущие значения из выпадающих списках.
        day_value = self.days_combo.currentText()
        month_value = self.month_combo.currentText()
        year_value = self.year_combo.currentText()

        # Выполняем запрос к API с выбранными данными.
        result = self.getResult(day_value, month_value, year_value)

        # Заменяем текст для доллара.
        self.dollar_value.setText('%s руб.' % result['val'])
        self.dollar_value.adjustSize()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    money = CBR_API()
    sys.exit(app.exec())