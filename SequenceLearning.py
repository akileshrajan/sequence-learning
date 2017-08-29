import sys,os
from PyQt4 import QtCore, QtGui
from NaoGui import Ui_MainWindow
import play as p


class SequenceLearning(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.connect_muse_button, QtCore.SIGNAL('clicked()'), self.connect_muse)
        QtCore.QObject.connect(self.ui.start_button,QtCore.SIGNAL('clicked()'),self.start)

    def start(self):
        """
        Start point of the application
        :return: None
        """

        # user info and folders
        user_name, ok = QtGui.QInputDialog.getText(self, 'Text Input Dialog', 'Enter user name:')
        user_folder = "data/user_" + str(user_name) + '/'

        if os.path.exists(user_folder):
            session_id = len(os.listdir(user_folder)) + 1
        else:
            session_id = 1
        os.makedirs(user_folder + "session_" + str(session_id))
        play = p.play()
        play.connect()
        #play.introduction(user_folder,session_id)

    def connect_muse(self):
        """
        Function to Connect to muse.
        :return: None
        """
        os.system(
            "gnome-terminal -e 'bash -c \"cd ~ && "
            "cd /home/akilesh/Muse && muse-io --device 00:06:66:79:48:35 --osc osc.udp://localhost:5000; exec bash\"'")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = SequenceLearning()
    myapp.show()
    sys.exit(app.exec_())