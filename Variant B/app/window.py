import env_storage
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction, QToolBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
import socket
import os


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(os.environ.get("APP_NAME"))
        self.setFixedSize(1024, 768)
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Create a web view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        self.setCentralWidget(central_widget)

         # Create a toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Create a reload action
        reload_action = QAction('Reload', self)
        reload_action.triggered.connect(self.web_view.reload)

        # Add the reload action to the toolbar
        self.toolbar.addAction(reload_action)

        self.web_view.setUrl(
            QUrl(f"http://{socket.gethostbyname(socket.gethostname())}:7000"))

        self.web_view.page().profile().downloadRequested.connect(self.download_requested)

    def download_requested(self, download_item):
        download_item.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebBrowser()
    window.show()
    sys.exit(app.exec_())
