from PySide6.QtWidgets import QApplication
from PySide6.QtGui import Qt
import darkdetect
import sys
from qasync import QEventLoop
import asyncio
from PySide6.QtCore import Qt, QFile, QTextStream
from ui import MainWindow
import os
import components
# import hupper

def create_app():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    base_dir = os.path.dirname(os.path.abspath(components.__file__))
    qss_path = os.path.join(base_dir, "style.qss")
    with open(qss_path, "r") as f:
        app.setStyleSheet(f.read())

    is_dark = darkdetect.isDark()

    if is_dark:
        QApplication.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    else:
        QApplication.styleHints().setColorScheme(Qt.ColorScheme.Light)
        
    window = MainWindow()
    window.show()

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    create_app()
    # reloader = hupper.start_reloader("app.create_app")
