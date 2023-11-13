import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QNetworkRequest
import socket


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the main window
        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 1024, 768)

        # Create a central widget and a layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Create a web view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # # Create a download button
        # download_button = QPushButton("Download Page")
        # download_button.clicked.connect(self.download_page)
        # layout.addWidget(download_button)

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Load an initial webpage
        self.web_view.setUrl(
            QUrl(f"http://{socket.gethostbyname(socket.gethostname())}:7000"))
        
        self.web_view.page().profile().downloadRequested.connect(self.download_requested)


    def download_page(self):
        # Get the current page's URL
        current_url = self.web_view.url()
        page_url = current_url.toString()

        # Download the page using Python's requests library or any other method you prefer
        # For example:
        # import requests
        # response = requests.get(page_url)
        # with open("downloaded_page.html", "w", encoding="utf-8") as file:
        #     file.write(response.text)
        # print("Page downloaded successfully!")
    def download_requested(self, download_item):
        # Handle download requests
        download_item.setUrl(download_item.url())
        # download_item.setDownloadOptions(options)
        download_item.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebBrowser()
    window.show()
    sys.exit(app.exec_())
