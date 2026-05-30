from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QPlainTextEdit, QSplitter, QTabWidget, QLabel
from PySide6.QtGui import Qt, QFont, QFontMetrics
import service
from components.syntax_highlighter import JsonHighlighter
from qasync import asyncSlot
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from components.code_editor import CodeEditor
from utils.http_status_codes import HTTP_STATUS_CODES
import traceback

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qURL")

        screen = QApplication.primaryScreen().availableGeometry()
        width = screen.width() * 0.6
        height = screen.height() * 0.6
        
        self.resize(width, height)

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("GET")
        self.combo_box.addItem("POST")
        self.combo_box.addItem("PUT")
        self.combo_box.addItem("DELETE")

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Enter URL")

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.button_clicked)

        # left section
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.combo_box)
        top_layout.addWidget(self.line_edit)
        top_layout.addWidget(self.send_button)

        self.header_input = QPlainTextEdit()
        self.body_input = CodeEditor()
        metrics = QFontMetrics(self.header_input.font())
        self.body_input.setTabStopDistance(4 * metrics.horizontalAdvance(' '))
        self.body_input.setFont(QFont("monospace"))
        self.highlighter = JsonHighlighter(self.body_input.document())

        central_layout = QSplitter(Qt.Horizontal)

        tab_widget = QTabWidget()
        headers_tab = QWidget()
        headers_tab_layout = QVBoxLayout(headers_tab)
        headers_tab_layout.addWidget(self.header_input)

        body_tab = QWidget()
        body_tab_layout = QVBoxLayout(body_tab)
        body_tab_layout.addWidget(self.body_input)

        tab_widget.addTab(headers_tab, "Headers")
        tab_widget.addTab(body_tab, "Body")
        central_layout.addWidget(tab_widget)

        # right section

        right_section_widget = QWidget()
        right_section = QVBoxLayout(right_section_widget)

        request_info_container = QHBoxLayout()
        request_info_container.setAlignment(Qt.AlignmentFlag.AlignRight)
        request_info_container.setContentsMargins(0, 0, 20, 0)
        # self.status_label_header = QLabel("Status:")
        # self.size_label_header = QLabel("Size:")
        # self.time_label_header = QLabel("Time:")
        self.status_label = QLabel("")
        self.size_label = QLabel("")
        self.time_label = QLabel("")
        # request_info_container.addWidget(self.status_label_header)
        request_info_container.addWidget(self.status_label)
        # request_info_container.addWidget(self.size_label_header)
        request_info_container.addWidget(self.size_label)
        # request_info_container.addWidget(self.time_label_header)
        request_info_container.addWidget(self.time_label)
        

        self.response_editor = CodeEditor()
        metrics = QFontMetrics(self.response_editor.font())
        self.response_editor.setTabStopDistance(4 * metrics.horizontalAdvance(' '))
        self.response_editor.setFont(QFont("monospace"))
        self.response_editor.setReadOnly(True)
        self.highlighter = JsonHighlighter(self.response_editor.document())

        right_section.addLayout(request_info_container)
        right_section.addWidget(self.response_editor)
        central_layout.addWidget(right_section_widget)
        


        outer_layout = QVBoxLayout()
        outer_layout.addLayout(top_layout)
        outer_layout.addWidget(central_layout)


        container = QWidget()
        container.setLayout(outer_layout)
        
        
        self.setCentralWidget(container)

        # self.combo_box.setItemDelegate(QStyledItemDelegate())

    @asyncSlot()
    async def button_clicked(self):
        self.send_button.setDisabled(True)
        self.send_button.setText("Loading...")
        try:
            result = await service.invoke(url=self.line_edit.text(), method=self.combo_box.currentText(), headers=self.header_input.toPlainText(), body=self.body_input.toPlainText())

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
            self.status_label.setText(f"Status:&nbsp;&nbsp;&nbsp;<span style='color: {color}'>{str(result["status"])} {HTTP_STATUS_CODES[result["status"]]}</span>")
            self.size_label.setText(f"Size:&nbsp;&nbsp;&nbsp;<span style='color: {color}'>{str(result["size"])} bytes</span>")
            self.time_label.setText(f"Time:&nbsp;&nbsp;&nbsp;<span style='color: {color}'>{str(result["time"])} ms</span>")
            self.send_button.setDisabled(False)
            self.send_button.setText("Send")
        except Exception as e:
            traceback.print_exc()
            self.send_button.setDisabled(False)
            self.send_button.setText("Send")