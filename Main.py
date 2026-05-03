import sys
from PySide6.QtWidgets import QApplication


# the Main Screen must be in a separate file because it has to be loaded AFTER django support

from PySide6.QtWidgets import (QWidget, QVBoxLayout, )

from app_secrets import (usr_auth, )

from sysver import (_appname, sysver, )
from calvincTools import calvincTools

from menuformname_viewMap import FormNameToURL_Map
from externalWebPageURL_Map import ExternalWebPageURL_Map
from database import get_app_sessionmaker

class MainScreen(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        if not self.objectName():
            self.setObjectName("MainWindow")
        
        cTools = calvincTools(
            appname=_appname,
            appver=sysver['DEV'],
            FormNameToURL_Map=FormNameToURL_Map,
            ExternalWebPageURL_Map=ExternalWebPageURL_Map,
            app_sessionmaker=get_app_sessionmaker(),
            usr_auth=usr_auth,
        )
        
        llayout = QVBoxLayout(self)
        stack = cTools.main_window_stack()
        if stack is not None:
            llayout.addWidget(stack)
        self.setLayout(llayout)
        
        self.setWindowTitle(self.tr(_appname + " " + sysver['DEV']))

        cTools.login()
    # __init__
# MainScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    topscreen = MainScreen()
    topscreen.show()

    sys.exit(app.exec())

