from PySide6.QtWidgets import QApplication
from PySide6.QtGui import Qt
import darkdetect
import sys
from qasync import QEventLoop
import asyncio
from PySide6.QtCore import Qt
from ui import MainWindow
# import hupper


def create_app():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    is_dark = darkdetect.isDark()

    if is_dark:
        QApplication.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    else:
        QApplication.styleHints().setColorScheme(Qt.ColorScheme.Light)
        
    window = MainWindow()
    window.showMinimized()

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # app.setDesktopFileName("qURL") 
    with loop:
        loop.run_forever()

if __name__ == "__main__":
    create_app()
    # reloader = hupper.start_reloader("app.create_app")
