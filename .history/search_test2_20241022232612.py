from PySide6 import QtWidgets, QtCore, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        # Создаем поле ввода для поиска
        self.search_field = QtWidgets.QLineEdit(self)
        self.search_field.setPlaceholderText("Поиск...")
        self.layout.addWidget(self.search_field)

        # Создаем таблицу
        self.table = QtWidgets.QTableView(self)
        self.layout.addWidget(self.table)

        # Создаем модель и прокси-модель для фильтрации
        self.model = QtGui.QStandardItemModel(0, 6, self)
        self.model.setHorizontalHeaderLabels(["Название", "Адрес", "Год открытия",
                                              "Описание", "Экспозиции", "X"])
        self.proxy_model = QtCore.QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)  # Фильтровать по всем столбцам

        # Устанавливаем прокси-модель в таблицу
        self.table.setModel(self.proxy_model)

        # Связываем изменение текста в поле поиска с обновлением фильтра
        self.search_field.textChanged.connect(self.proxy_model.setFilterFixedString)

        # Пример заполнения таблицы данными
        self.add_data()

    def add_data(self):
        data = [
            ["Музей 1", "Адрес 1", "2000", "Описание 1", "Экспозиция 1", "X1"],
            ["Музей 2", "Адрес 2", "2001", "Описание 2", "Экспозиция 2", "X2"],
            ["Музей 3", "Адрес 3", "2002", "Описание 3", "Экспозиция 3", "X3"],
        ]
        for row in data:
            items = [QtGui.QStandardItem(field) for field in row]
            self.model.appendRow(items)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()