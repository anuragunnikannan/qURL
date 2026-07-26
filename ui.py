from PySide6.QtWidgets import QApplication, QTableWidget, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QPlainTextEdit, QSplitter, QTabWidget, QLabel, QStyledItemDelegate
from PySide6.QtGui import Qt, QFont, QFontMetrics
from components.table import Table
import service
from components.syntax_highlighter import JsonHighlighter
from qasync import asyncSlot
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from qt_material_icons import MaterialIcon
from components.code_editor import CodeEditor
from utils.http_status_codes import HTTP_STATUS_CODES
import traceback

from utils.transform_headers import transform_headers_dict

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qURL")

        screen = QApplication.primaryScreen().availableGeometry()
        width = screen.width() * 0.6
        height = screen.height() * 0.6
        
        self.resize(width, height)

        self.combo_box = QComboBox(self)
        self.combo_box.setObjectName("method_selector")
        self.combo_box.addItem("GET")
        self.combo_box.addItem("POST")
        self.combo_box.addItem("PUT")
        self.combo_box.addItem("DELETE")

        self.line_edit = QLineEdit(self)
        self.line_edit.setObjectName("url_input")
        self.line_edit.setPlaceholderText("Enter URL")

        self.send_button = QPushButton("Send  ")
        self.send_button.setObjectName("send_button")
        self.send_button.setIcon(QIcon(MaterialIcon("send")))
        self.send_button.setLayoutDirection(Qt.RightToLeft)
        self.send_button.clicked.connect(self.button_clicked)

        # left section
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.combo_box)
        top_layout.addWidget(self.line_edit)
        top_layout.addWidget(self.send_button)

        self.header_input = Table(editable=True)
        self.body_input = CodeEditor()
        metrics = QFontMetrics(self.header_input.font())
        self.body_input.setTabStopDistance(4 * metrics.horizontalAdvance(' '))
        self.body_input.setFont(QFont("monospace"))
        self.highlighter = JsonHighlighter(self.body_input.document())

        central_layout = QSplitter(Qt.Horizontal)

        request_tab_widget = QTabWidget()

        body_tab = QWidget()
        body_tab_layout = QVBoxLayout(body_tab)
        body_tab_layout.addWidget(self.body_input)

        request_tab_widget.addTab(self.header_input, "Headers")
        request_tab_widget.addTab(body_tab, "Body")
        central_layout.addWidget(request_tab_widget)

        # right section

        self.status_label = QLabel("")
        self.size_label = QLabel("")
        self.time_label = QLabel("")
      
        self.response_editor = CodeEditor()
        metrics = QFontMetrics(self.response_editor.font())
        self.response_editor.setTabStopDistance(4 * metrics.horizontalAdvance(' '))
        self.response_editor.setFont(QFont("monospace"))
        self.response_editor.setReadOnly(True)
        self.highlighter = JsonHighlighter(self.response_editor.document())

        # self.response_header_editor = QPlainTextEdit()
        # self.response_header_editor.setReadOnly(True)
        self.response_header_editor = Table(editable=False)

        response_tab_widget = QTabWidget()
        

        response_tab_widget.addTab(self.response_editor, "Response")
        response_tab_widget.addTab(self.response_header_editor, "Headers")
        
        central_layout.addWidget(response_tab_widget)
        


        outer_layout = QVBoxLayout()
        outer_layout.addLayout(top_layout)
        outer_layout.addWidget(central_layout)


        container = QWidget()
        container.setLayout(outer_layout)
        
        
        self.setCentralWidget(container)
        self.status_bar = self.statusBar()

    @asyncSlot()
    async def button_clicked(self):
        self.send_button.setDisabled(True)
        try:
            result = await service.invoke(url=self.line_edit.text(), method=self.combo_box.currentText(), headers=self.header_input.get_data(), body=self.body_input.toPlainText())

            color = "white"
            if result["status"] >= 100 and result["status"] < 200:
                color = "blue"
            elif result["status"] >= 200 and result["status"] < 300:
                color = "green"
            elif result["status"] >= 300 and result["status"] < 400:
                color = "orange"
            else:
                color = "red"

            self.response_editor.setPlainText(str(result["content"]))
            # print(transform_headers_dict(result["headers"]))
            self.response_header_editor.set_data(result["headers"])

            self.status_label.setText(f"Status:&nbsp;&nbsp;&nbsp;<span style='color: {color}'>{str(result['status'])} {HTTP_STATUS_CODES[result['status']]}</span>")
            self.size_label.setText(f"Size:&nbsp;&nbsp;&nbsp;<span style='color: {color}'>{str(result['size'])} bytes</span>")
            self.time_label.setText(f"Time:&nbsp;&nbsp;&nbsp;<span style='color: {color}'>{str(result['time'])} ms</span>")

            self.status_bar.addPermanentWidget(self.status_label)
            self.status_bar.addPermanentWidget(self.size_label)
            self.status_bar.addPermanentWidget(self.time_label)

            self.send_button.setDisabled(False)
            self.send_button.setText("Send  ")
        except Exception as e:
            traceback.print_exc()
            self.send_button.setDisabled(False)
            self.send_button.setText("Send  ")