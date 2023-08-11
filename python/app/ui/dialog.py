# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!


from tank.platform.qt import QtCore, QtGui
from tank.platform.qt5 import QtWidgets
#from qgis.PyQt.QtWidgets import QVBoxLayout
from . import separator


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.app = QtWidgets.QApplication.instance()
        self.app.processEvents()

        Dialog.setObjectName("Dialog")
        #Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #Dialog.resize(431, 392)
        Dialog.resize(489, 592)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.layout().setContentsMargins(15, 20, 15, 10)

        # Search Layout
        #self.inputLayout = QtGui.QVBoxLayout(Dialog)
        #self.inputLayout.setObjectName("inputLayout")

        #self.searchLabel = QtGui.QLabel(Dialog)
        #self.searchLabel.setObjectName("context")
        #self.searchLabel.setText("Search")

        #self.playlistInput = QtGui.QLineEdit(Dialog)
        #self.playlistInput.setPlaceholderText("Playlist name...")
        #self.playlistInput.setToolTip('Enter the first few characters of query playlist name (case sensitive)')

        #self.inputLayout.addWidget(self.searchLabel)
        #self.inputLayout.addWidget(self.playlistInput)
        #self.verticalLayout.addLayout(self.inputLayout)

        # Playlists Layout
        self.playlistLayout = QtGui.QVBoxLayout(Dialog)
        #self.playlistLayout.layout().setContentsMargins(0, 5, 0, 30)
        self.playlistLabel = QtGui.QLabel(Dialog)
        self.playlistLabel.setText("Project paths")

        self.playlistSelection = QtWidgets.QListWidget()
        self.playlistSelection.setToolTip('Select project path in the form of %SG_UNREAL_PROJECT_ARK%/Projects/ShooterGame/ShooterGame.uproject')

        self.playlistLayout.addWidget(self.playlistLabel)
        self.playlistLayout.addWidget(self.playlistSelection)
        self.verticalLayout.addLayout(self.playlistLayout)

        # Selected Playlist Layout
        self.selectedPlaylistLayout = QtGui.QVBoxLayout(Dialog)
        self.selectedPlaylistLayout.layout().setContentsMargins(0, 0, 0, 20)
        self.selectedPlaylistLabel = QtGui.QLabel(Dialog)
        self.selectedPlaylistLabel.setText("Selected project path")

        self.selectedPlaylistInput = QtGui.QLineEdit(Dialog)
        self.selectedPlaylistInput.setPlaceholderText("Selected project path...")
        self.selectedPlaylistInput.setToolTip('Display the selected project path')

        self.playlistLayout.addWidget(self.selectedPlaylistLabel)
        self.playlistLayout.addWidget(self.selectedPlaylistInput)
        self.verticalLayout.addLayout(self.selectedPlaylistLayout)

        #self_playlist_separator = separator.Separator()
        #self.verticalLayout.addWidget(self_playlist_separator)

        #Output Layout
        self.outputLayout = QtGui.QVBoxLayout(Dialog)
        #self.outputLabel = QtGui.QLabel(Dialog)
        #self.outputLabel.setText("Output")

        self.fileLayout = QtGui.QHBoxLayout(Dialog)
        #self.outputPathText = QtGui.QLineEdit()
        #self.outputPathText.setPlaceholderText("Enter destination folder ")
        #self.outputPathText.setToolTip('Use default destination folder B:\Ark2Depot\MyPlaylists or enter a new one')
        self.outputDialogBtn = QtGui.QPushButton()
        self.outputDialogBtn.setText("Add project path")
        self.outputDialogBtn.setToolTip('Browse .uproject files to add another project path in the form of %SG_UNREAL_PROJECT_ARK%/Projects/ShooterGame/ShooterGame.uproject')

        self.save_project_path = QtGui.QPushButton()
        self.save_project_path.setText("Save project path")
        self.save_project_path.setToolTip('Save current project path')

        self.unreal_launcher_btn = QtGui.QPushButton()
        self.unreal_launcher_btn.setText("Launch Unreal Editor")
        self.unreal_launcher_btn.setToolTip("Save the current settings and launch Unreal Editor")

        #self.fileLayout.addWidget(self.outputPathText)
        self.fileLayout.addWidget(self.outputDialogBtn)
        self.fileLayout.addWidget(self.save_project_path)
        self.fileLayout.addWidget(self.unreal_launcher_btn)

        #self.outputLayout.addWidget(self.outputLabel)
        self.outputLayout.addLayout(self.fileLayout)
        self.verticalLayout.addLayout(self.outputLayout)


        # Status Layout
        self.statusLayout = QtGui.QVBoxLayout(Dialog)
        self.statusLayout.layout().setContentsMargins(0, 0, 0, 10)
        self.progressLabel = QtGui.QLabel(Dialog)
        self.progressLabel.setText("Progress")

        self.status_dialog = QtWidgets.QTextBrowser(Dialog)
        self.status_dialog.verticalScrollBar().setValue(self.status_dialog.verticalScrollBar().maximum())
        self.status_dialog.setMinimumHeight(100)

        self.statusLayout.addWidget(self.progressLabel)
        self.statusLayout.addWidget(self.status_dialog)
        self.verticalLayout.addLayout(self.statusLayout)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))


from . import resources_rc
