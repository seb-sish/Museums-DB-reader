import re
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
import sys
import os

from database import Museums

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        # Добавляем поля
        self.table = QtWidgets.QTableWidget(0, 6, self)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.table.setMinimumSize(480, 240)
        self.table.setHorizontalHeaderLabels(["Название", "Адрес", "Год открытия",
                                               "Описание", "Экспозиции", "X"])
        header = self.table.horizontalHeader()
        for i in range(3, self.table.columnCount() - 1): header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        # for i in range(3, 5): header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.table.columnCount() - 1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setItemDelegate(AlignDelegate())
        self.layout.addWidget(self.table)

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = None
        self.setWindowTitle("База данных музеев")
        # self.closeEvent = self.closeEvent
        self.resize(960, 480)

        # Создаем toolbar
        toolbar = self.addToolBar("Инструменты")
        toolbar.setMaximumHeight(36)
        
        # Добавляем кнопки на toolbar
        create_action = QAction(self)
        create_action.setIconText("Создать")
        create_action.setIcon(QIcon("./primary/create_new_file.svg"))
        create_action.triggered.connect(self.create_new_file)
        toolbar.addAction(create_action)
        
        open_action = QAction(self)
        open_action.setIconText("Открыть")
        open_action.setIcon(QIcon("./primary/open_file.svg"))
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction(self)
        save_action.setIconText("Сохранить")
        save_action.setIcon(QIcon("./primary/save_file.svg"))
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        saveas_action = QAction(self)
        saveas_action.setIconText("Сохранить как...")
        saveas_action.setIcon(QIcon("./primary/saveas_file.svg"))
        saveas_action.triggered.connect(self.saveas_file)
        toolbar.addAction(saveas_action)

        concatinate_action = QAction(self)
        concatinate_action.setIconText("Объеденить")
        concatinate_action.setIcon(QIcon("./primary/concatenate_file.svg"))
        concatinate_action.triggered.connect(self.concatinate_file)
        toolbar.addAction(concatinate_action)

        # Добавляем поле поиска на toolbar
        self.search_field = QtWidgets.QLineEdit(self)
        self.search_field.setStyleSheet("margin-right: 10px;")
        self.search_field.setPlaceholderText("Поиск...")
        self.search_field.textChanged.connect(self.search_table)
        self.search_field.setMaximumWidth(384)
        toolbar.addWidget(self.search_field)

        # create the menu bar
        menubar = self.menuBar()
        file = menubar.addMenu('&Файл')
        fcreate = QAction("Создать", self)
        fcreate.triggered.connect(self.create_new_file)
        fopen = QAction("Открыть файл...", self)
        fopen.triggered.connect(self.open_file)
        fsave = QAction("Сохранить", self)
        fsave.triggered.connect(self.save_file)
        fsaveas = QAction("Сохранить как...", self)
        fsaveas.triggered.connect(self.saveas_file)
        fconcatinate = QAction("Объеденить", self)
        fconcatinate.triggered.connect(self.concatinate_file)
        file.addActions([fcreate, fopen, fsave, fsaveas, fconcatinate])

        operations = menubar.addMenu('&Операции')
        oadd = QAction("Добавить запись", self)
        oadd.triggered.connect(self.addItem)
        oremove = QAction("Очистить таблицу", self)
        oremove.triggered.connect(self.clear_table)
        # ochange = QAction("Редактировать запись", self)
        operations.addActions([oadd, oremove])

        about = menubar.addMenu('&О программе') 
        about.aboutToShow.connect(self.about)
        
        self.widget = MyWidget()
        self.table = self.widget.table
        self.columsCount = self.table.columnCount()
        self.setCentralWidget(self.widget)

    def need_file_opened(func):
        def wrapper(self, *args, **kwargs):
            if self.database is None:
                self.open_file()
            return func(self, *args, **kwargs)
        return wrapper
    
    @need_file_opened
    @QtCore.Slot()
    def addItem(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setRowHeight(row, 36)
        for column in range(0, 3):
            self.table.setCellWidget(row, column, QtWidgets.QLineEdit("", alignment=Qt.AlignCenter))
        for column in range(3, self.columsCount - 1):
            self.table.setCellWidget(row, column, QtWidgets.QTextEdit("", alignment=Qt.AlignCenter))

        removeBtn = QtWidgets.QPushButton("X")
        removeBtn.clicked.connect(self.removeRow)
        self.table.setCellWidget(row, self.columsCount - 1, removeBtn)
        # return self.database.add_value(**self.parse_row(row))

    @QtCore.Slot()
    def search_table(self, text):
        for i in range(self.table.rowCount()):
            self.table.setRowHidden(i, True)
            for j in range(self.table.columnCount()-1):
                item = self.table.cellWidget(i, j)
                if item:
                    try:
                        if re.search(text, item.text() if type(item) is QtWidgets.QLineEdit 
                                     else item.toPlainText(), re.IGNORECASE):
                            self.table.setRowHidden(i, False)
                            break
                    except re.error:
                        if text.lower() in item.text() if type(item) is QtWidgets.QLineEdit \
                                     else item.toPlainText():
                            self.table.setRowHidden(i, False)
                            break

    def parse_row(self, row_index:int):
        return {
            "name": self.table.cellWidget(row_index, 0).text(),
            "address": self.table.cellWidget(row_index, 1).text(),
            "date": self.table.cellWidget(row_index, 2).text(),
            "description": self.table.cellWidget(row_index, 3).toPlainText(),
            "exposition": self.table.cellWidget(row_index, 4).toPlainText()
        }

    @need_file_opened
    @QtCore.Slot()    
    def removeRow(self):
        index = self.table.selectedIndexes()[0].row()
        self.table.removeRow(index)
        self.statusBar().showMessage(f"Удалена {index+1} строка")
        return self.database.remove_value(index)

    @QtCore.Slot()
    def open_file(self):
        try:
            path = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть файл БД', '',
                                            'Json files (*.json)')[0]
            self.database = Museums(path)
            self.load_database()
            self.statusBar().showMessage(f"Открыт файл {path}")
        except FileNotFoundError:
            print("file not open!")
            self.statusBar().showMessage(f"Файл НЕ был открыт!")

    @QtCore.Slot()
    def concatinate_file(self):
        try:
            path = QtWidgets.QFileDialog.getOpenFileName(self, 'Соединить файл БД', '',
                                            'Json files (*.json)')[0]
            self.concatenate_database(path)
            self.statusBar().showMessage(f"Исходная таблица объеденена с файлом {path}")
        except FileNotFoundError:
            print("file not open!")
            self.statusBar().showMessage(f"Файл НЕ был открыт!")

    @QtCore.Slot()
    def create_new_file(self):
        try:
            path = QtWidgets.QFileDialog.getSaveFileName(self, 'Создать файл БД', '',
                                            'Json files (*.json)')[0]
            self.database = Museums(path, create_new=True)
            self.load_database()
            self.statusBar().showMessage(f"Создан файл {path}")
        except FileNotFoundError:
            print("file not open!")
            self.statusBar().showMessage(f"Файл НЕ создан!")

    @need_file_opened
    @QtCore.Slot()
    def save_file(self):
        self.update_values()
        self.database.save_file()
        self.statusBar().showMessage("Файл сохранен")

    def update_values(self):
        self.database.clear()
        for row in range(self.table.rowCount()):
            self.database.add_value(**self.parse_row(row))

    def get_rows_values(self):
        return [self.parse_row(row) for row in range(self.table.rowCount())]
        
    @need_file_opened
    @QtCore.Slot()
    def saveas_file(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить файл БД', '',
                                        'Json files (*.json)')[0]
        if path != '' and path.split(".")[-1] in ("json"):
            self.update_values()
            self.database.saveas_file(path)
            self.statusBar().showMessage(f"Файл сохранен как {path}")
        else:
            print("file not save!")
            self.statusBar().showMessage(f"Файл НЕ сохранен!")

    @QtCore.Slot()
    def clear_table(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

    def load_database(self):
        self.clear_table()

        for row, data in enumerate(self.database):
            self.table.insertRow(self.table.rowCount())
            self.table.setRowHeight(row, 36)
            for column in range(0, 3):
                self.table.setCellWidget(row, column, QtWidgets.QLineEdit(str(data[column]), alignment=Qt.AlignCenter))
            for column in range(3, self.columsCount - 1):
                self.table.setCellWidget(row, column, QtWidgets.QTextEdit(str(data[column]), alignment=Qt.AlignCenter))

            removeBtn = QtWidgets.QPushButton("X")
            removeBtn.clicked.connect(self.removeRow)
            self.table.setCellWidget(row, self.columsCount - 1, removeBtn)
    
    def concatenate_database(self, path:str):
        add_db = Museums(path)

        for row, data in enumerate(add_db, start=self.table.rowCount()):
            self.table.insertRow(self.table.rowCount())
            self.table.setRowHeight(row, 36)
            for column in range(0, 3):
                self.table.setCellWidget(row, column, QtWidgets.QLineEdit(str(data[column]), alignment=Qt.AlignCenter))
            for column in range(3, self.columsCount - 1):
                self.table.setCellWidget(row, column, QtWidgets.QTextEdit(str(data[column]), alignment=Qt.AlignCenter))

            removeBtn = QtWidgets.QPushButton("X")
            removeBtn.clicked.connect(self.removeRow)
            self.table.setCellWidget(row, self.columsCount - 1, removeBtn)
    
    
    def closeEvent(self, event):
        if self.check_changed():
            r = self.saveQustion()
            if r == QtWidgets.QMessageBox.Yes:
                self.save_file()
            elif r == QtWidgets.QMessageBox.Cancel:
                event.ignore()
                return
        event.accept()

    def check_changed(self):
        return self.database is not None and self.database.is_changed(self.get_rows_values())
    
    def saveQustion(self):
        return QtWidgets.QMessageBox.question(self, 'Сохранить файл', "Последние изменения не были сохранены. Вы хотите сохранить файл?",
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, 
                                       defaultButton=QtWidgets.QMessageBox.Yes)

    @QtCore.Slot()
    def about(self):
        QtWidgets.QMessageBox.about(self, "О программе",
            "Выполнил:\nстудент 2 курса\nгруппы ИКПИ-32\nСкрипалев Виталий Сергеевич")

class AlignDelegate(QtWidgets.QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

if __name__ == "__main__":
    application = QtWidgets.QApplication([])

    css_file="theme.css"
    if css_file and os.path.exists(css_file):
        with open(css_file) as file:
            stylesheet = file.read()
    application.setStyleSheet(stylesheet)
    
    MyApp = MyApp()
    MyApp.show()

    sys.exit(application.exec())
