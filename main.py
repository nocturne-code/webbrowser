import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon("icons/cat.png"))
        self.showMaximized()

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon("icons/back-arrow.png"))
        back_btn.setIconSize(QSize(20, 20))
        back_btn.clicked.connect(self.back_btn)
        navbar.addWidget(back_btn)

        forward_btn = QPushButton()
        forward_btn.setIcon(QIcon("icons/forward-arrow.png"))
        forward_btn.setIconSize(QSize(20, 20))
        forward_btn.clicked.connect(self.forward_btn)
        navbar.addWidget(forward_btn)

        reload_btn = QPushButton()
        reload_btn.setIcon(QIcon("icons/forward-button.png"))
        reload_btn.setIconSize(QSize(20, 20))
        reload_btn.clicked.connect(self.reload_btn)
        navbar.addWidget(reload_btn)

        home_btn = QPushButton()
        home_btn.setIcon(QIcon("icons/home-button.png"))
        home_btn.setIconSize(QSize(20, 20))
        home_btn.clicked.connect(self.navigate_home)
        navbar.addWidget(home_btn)

        navbar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        navbar.addSeparator()

        add_btn = QPushButton()
        add_btn.setIcon(QIcon("icons/add.png"))
        add_btn.setIconSize(QSize(20, 20))
        add_btn.clicked.connect(self.tab_open)
        navbar.addWidget(add_btn)

        self.add_new_tab(QUrl('http://duckduckgo.com'), 'homepage')
        self.show()

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('http://duckduckgo.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def tab_open(self, i):
        if i == 0:
            self.add_new_tab()

    def current_tab_changed(self):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl)
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Cat Browser" % title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl('http://duckduckgo.com'))

    def back_btn(self):
        self.tabs.currentWidget().back()

    def forward_btn(self):
        self.tabs.currentWidget().forward()

    def reload_btn(self):
        self.tabs.currentWidget().reload()

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)


app = QApplication(sys.argv)
QApplication.setApplicationName('Cat Browser')
app.setStyleSheet("""
QWidget{
background-color:rgb(49,49,49);
color:rgb(255,255,255);
}
QTabWidget::pane{
border-top: 2px solid rgb(90,90,90);
position:absolute;
top:-0.5em;
color:rgb(255,255,255);
padding:5px;
}
QTabWidget::tab-bar{
alignment:left;
}
QLabel,QToolButton,QTabBar::tab{
background:rgb(90,90,90);
border:2px solid rgb(90,90,90);
border-radius:10px;
min-width:8ex;
padding:5px;
margin-right:2px;
color:rgb(255,255,255);
margin-top:3px;
}
QLabel:hover,QToolButton::hover,QTabBar::tab:hover,QTabBar::tab:selected{
background:rgb(49,49,49);
border:2px solid rgb(0,36,36);
background-color:rgb(0,36,36);
}
QLineEdit{border:2px solid rgb(0,36,36);
border-radius:10px;
padding:5px;
background-color:rgb(0,36,36);
color:rgb(255,255,255);
}
QLineEdit:hover{
border: 2px solid rgb(0,66,124);
}
QLineEdit:focus{
border: 2px solid rgb(0,136,255);
color:rgb(200,200,200);
}
QPushButton{
background:rgb(49,49,49);
border:none;
background-color: rgb(49,49,49);
padding:10px;
margin-right:2px;
}
""")
window = MainWindow()
app.exec_()
