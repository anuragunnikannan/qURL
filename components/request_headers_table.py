from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QAbstractItemView, QHBoxLayout, QHeaderView, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout
from PySide6.QtGui import QIcon, Qt
from qt_material_icons import MaterialIcon

class RequestHeadersTable(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([" ", "Key", "Value"])
        self.table.verticalHeader().hide()

        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 36)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table)
        self.add_row()
        self.table.cellChanged.connect(self.on_cell_changed)

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 1, QTableWidgetItem(""))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn = QPushButton("")
        btn.setObjectName("delete_header_item_button")
        btn.setFixedWidth(20)
        btn.setFixedHeight(20)
        btn.setIcon(QIcon(MaterialIcon("close")))
        btn_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn.clicked.connect(lambda: self.remove_row(btn))
        self.table.setCellWidget(row_position, 0, btn_container)

    def remove_row(self, button):
        if self.table.rowCount() <= 1:
            return
        
        print(button.parentWidget().pos())
        position = button.parentWidget().pos()
        index = self.table.indexAt(position)
        print(index.row())

        self.table.removeRow(index.row())
    
    def get_headers(self):
        headers = {}
        for row in range(self.table.rowCount()):
            key_item = self.table.item(row, 1)
            value_item = self.table.item(row, 2)
            if key_item and value_item:
                key = key_item.text().strip()
                value = value_item.text().strip()
                if key and value:
                    headers[key] = value
        return headers
    
    def on_cell_changed(self, row, column):
        if row == self.table.rowCount() - 1:
            self.table.blockSignals(True)
            self.add_row()
            self.table.blockSignals(False)