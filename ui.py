from PySide6.QtWidgets import QApplication, QButtonGroup, QRadioButton, QSizePolicy, QStackedWidget, QTableWidget, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QPlainTextEdit, QSplitter, QTabWidget, QLabel, QStyledItemDelegate
from PySide6.QtGui import Qt, QFont, QFontMetrics
from components.dynamic_syntax_highlighter import DynamicHighlighter
from components.table import Table
import service
from components.syntax_highlighter import JsonHighlighter
from qasync import asyncSlot
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, Qt
from qt_material_icons import MaterialIcon
from components.code_editor import CodeEditor
from utils.http_status_codes import HTTP_STATUS_CODES
from utils.formatter import format_response
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
        self.body_input_raw_editor = CodeEditor()
        metrics = QFontMetrics(self.header_input.font())
        self.body_input_raw_editor.setTabStopDistance(4 * metrics.horizontalAdvance(' '))
        self.body_input_raw_editor.setFont(QFont("monospace"))
        # self.highlighter = JsonHighlighter(self.body_input_raw_editor.document())
        # self.raw_highlighter = DynamicHighlighter(
                    # self.body_input_raw_editor.document()
                # )

        body_tab = QWidget()
        body_tab_layout = QVBoxLayout(body_tab)
        body_tab_layout.setContentsMargins(0, 0, 0, 0)

        self.body_content_type_tab_widget = QTabWidget()
        self.body_content_type_tab_widget.setObjectName("body_content_type_tab_widget")
        self.body_content_type_tab_widget.addTab(QStackedWidget(), "none")
        self.body_content_type_tab_widget.addTab(QStackedWidget(), "form-data")
        self.body_content_type_tab_widget.addTab(QStackedWidget(), "urlencoded")
        self.body_content_type_tab_widget.addTab(QStackedWidget(), "binary")
        self.body_content_type_tab_widget.addTab(self.body_input_raw_editor, "raw")

        self.raw_content_type_selector = QComboBox()
        self.raw_content_type_selector.setObjectName("raw_content_type_selector")
        self.raw_content_type_selector.addItems(["json", "html", "xml", "text"])
        self.raw_content_type_selector.hide()
        self.raw_body_content_highlighter = DynamicHighlighter(self.body_input_raw_editor.document())
        self.raw_content_type_selector.currentTextChanged.connect(self.on_raw_content_type_changed)

        # self.body_content_type_tab_widget.currentChanged.connect(lambda index: self.raw_content_type_selector.setVisible(index == 4))
        self.body_content_type_tab_widget.currentChanged.connect(self.body_content_type_tab_widget_changed)

        self.body_content_type_tab_widget.setCornerWidget(self.raw_content_type_selector, Qt.BottomRightCorner)
        body_tab_layout.addWidget(self.body_content_type_tab_widget)

        central_layout = QSplitter(Qt.Horizontal)

        request_tab_widget = QTabWidget()

        request_tab_widget.addTab(self.header_input, "Headers")
        request_tab_widget.addTab(body_tab, "Body")
        central_layout.addWidget(request_tab_widget)

        # right section

        self.status_label = QLabel("")
        self.size_label = QLabel("")
        self.time_label = QLabel("")
      
        self.response_viewer = CodeEditor()
        metrics = QFontMetrics(self.response_viewer.font())
        self.response_viewer.setTabStopDistance(4 * metrics.horizontalAdvance(' '))
        self.response_viewer.setFont(QFont("monospace"))
        self.response_viewer.setReadOnly(True)
        # self.highlighter = JsonHighlighter(self.response_viewer.document())
        # Dynamic highlighter setup
        self.response_viewer_highlighter = DynamicHighlighter(
            self.response_viewer.document()
        )
        # self.detected_mime_type = "text/plain"

        # # Debounce timer for language detection
        # self.detect_timer = QTimer(self)
        # self.detect_timer.setSingleShot(True)
        # self.detect_timer.setInterval(300)
        # self.detect_timer.timeout.connect(self.on_raw_content_changed)
        # self.body_input_raw_editor.textChanged.connect(self.detect_timer.start)

        # self.response_header_editor = QPlainTextEdit()
        # self.response_header_editor.setReadOnly(True)
        self.response_header_editor = Table(editable=False)

        response_tab_widget = QTabWidget()
        

        response_tab_widget.addTab(self.response_viewer, "Response")
        response_tab_widget.addTab(self.response_header_editor, "Headers")
        
        central_layout.addWidget(response_tab_widget)
        central_layout.setStretchFactor(0, 1)
        central_layout.setStretchFactor(1, 1)
        central_layout.setSizes([500, 500])

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
            result = await service.invoke(url=self.line_edit.text(), method=self.combo_box.currentText(), headers=self.header_input.get_data(), body=self.body_input_raw_editor.toPlainText())

            color = "white"
            if result["status"] >= 100 and result["status"] < 200:
                color = "blue"
            elif result["status"] >= 200 and result["status"] < 300:
                color = "green"
            elif result["status"] >= 300 and result["status"] < 400:
                color = "orange"
            else:
                color = "red"

            self.response_header_editor.set_data(result["headers"])
            self.response_viewer.setPlainText(format_response(str(result["content"]), result["headers"]["content-type"]))
            self.response_viewer_highlighter.detect_and_update(str(result["content"]))

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

    def on_raw_content_type_changed(self, content_type: str):
        mime_type_mapping = {
            "json": "application/json",
            "html": "text/html",
            "xml": "application/xml",
            "text": "text/plain"
        }
        self.raw_body_content_highlighter.set_language(content_type)

        headers = self.header_input.get_data()
        headers["Content-Type"] = mime_type_mapping.get(content_type, "text/plain")
        self.header_input.set_data(headers)

    def body_content_type_tab_widget_changed(self, index):
        mime_type_mapping = {
            0: "text/plain",  # none
            1: "multipart/form-data",  # form-data  
            2: "application/x-www-form-urlencoded",  # urlencoded
            3: "application/octet-stream",  # binary
            4: "application/json"
        }
        self.raw_content_type_selector.setVisible(index == 4)
        headers = self.header_input.get_data()
        headers["Content-Type"] = mime_type_mapping.get(index, "text/plain")
        self.header_input.set_data(headers)