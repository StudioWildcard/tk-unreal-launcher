# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import sys
from . unreal_launcher import UnrealLauncher
from pathlib import Path
from os.path import expanduser

from tank.platform.qt5 import QtWidgets

# import shutil
import shutil


# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog
from collections import deque

# import the global_search_widget module from the qtwidgets framework
global_search_widget = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "global_search_widget")

# import the task manager from shotgunutils framework
# task_manager = sgtk.platform.import_framework(
#     "tk-framework-shotgunutils", "task_manager")

# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system.

    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Unreal Launcher", app_instance, AppDialog)


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)

        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Set up UI

        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        self.widget_app = QtWidgets.QApplication.instance()

        # create a bg task manager for pulling data from SG
        # self._bg_task_manager = task_manager.BackgroundTaskManager(self)

        # logging happens via a standard toolkit logger
        msg = "Unreal Launcher app..."
        self.log_status(msg)


        # via the self._app handle we can for example access:
        # - The engine, via self._app.engine
        # - A Shotgun API instance, via self._app.shotgun
        # - An Sgtk API instance, via self._app.sgtk

        # Shotgun API instance
        self.sg = self._app.shotgun

        self.projectName = str(self._app.context).replace("Project ", "")
        # self.ui.context.setText(self.projectName)

        self.localStorage = Path(self._app.sgtk.project_path).anchor.replace("\\", "/")

        #self.playlistInput = self.ui.playlistInput
        self.playlistnames = deque()
        self.playlistSelection = self.ui.playlistSelection
        self.unreal_filepath = self.get_engine_location_file()
        self.get_playlists()
        self.populate_playlist()
        self.select_first_playlist()
        self.playlistCount = len(self.playlistnames)
        self.current_unreal_project_path = None
        self.launch_dict = {}

        self.playlistSelection.clicked.connect(self.setPlaylist)
        self.ui.save_project_path.clicked.connect(self.save_project_paths_file)
        self.ui.unreal_launcher_btn.clicked.connect(self.launch_unreal)


        self.ui.outputDialogBtn.clicked.connect(self._on_browse)




    def setDefaultPath(self):
        projectDir = os.path.join(self.getProjectPath(), 'MyPlaylists')
        self.ui.outputPathText.setText(projectDir)

    def setPlaylist(self):
        self.current_unreal_project_path = self.playlistSelection.currentItem().text()
        self.ui.selectedPlaylistInput.setText(self.current_unreal_project_path)


    def get_playlists(self):
        """
        Populate the playlist
        """

        self.unreal_filepath = self.unreal_filepath.replace("\\", "/")
        #msg = 'unreal_filepath: {}'.format(self.unreal_filepath)
        #self.log_status(msg)
        if self.unreal_filepath and os.path.exists(self.unreal_filepath):
            msg = 'Reading project paths file: {} ...'.format(self.unreal_filepath)
            self.log_status(msg)

            # open the file and read the contents
            with open(self.unreal_filepath, 'r') as f:
               # read the contents of the file line by line
                for line in f.readlines():
                    # msg = 'Engine location: {}'.format(line)
                    # self.log_status(msg)
                    # strip the newline character
                    line = line.strip()
                    # add the line to the list
                    self.playlistnames.append(line)

    def populate_playlist(self):
        """
        Populate the playlist
        """
        playlistSelection = self.playlistSelection
        playlistSelection.clear()
        for playlist in self.playlistnames:
            playlistSelection.addItem(playlist)


    def addPlaylist(self):
        playlistName = self.ui.playlistInput.text()

    def reorder_playlist(self):
        self.current_unreal_project_path = self.ui.selectedPlaylistInput.text()
        self.current_unreal_project_path.replace("\\", "/")
        if self.current_unreal_project_path in self.playlistnames:
            self.playlistnames.remove(self.current_unreal_project_path)
            self.playlistnames.appendleft(self.current_unreal_project_path)


    def save_project_paths_file(self):
        """Saves the engine location file self.unreal_filepath"""

        # reorder the playlist, putting the selected file at the top
        self.reorder_playlist()

        if not os.path.exists(self.unreal_filepath):
            msg = 'Creating engine location file: {}'.format(self.unreal_filepath)
            self.log_status(msg)
            msg = 'Unable to write engine location file: {}'.format(self.unreal_filepath)
            self.log_status(msg)

            return
        # make a backup of the file
        backup_filepath = self.unreal_filepath + ".bak"
        shutil.copy(self.unreal_filepath, backup_filepath)
        # open the file and write the contents, overwriting the existing file
        with open(self.unreal_filepath, 'w') as f:
            # write the engine location to the file
            for line in self.playlistnames:
                f.write(line + '\n')
        # close the file
        f.close()
        msg = "\n <span style='color:#2C93E2'>Saving project path to file {}</span> \n".format(self.unreal_filepath)
        self.log_status(msg)




    def _on_browse(self, folders=False):
        """Opens a file dialog to browse to files for engine location."""

        # options for either browse type
        options = [
            QtGui.QFileDialog.DontResolveSymlinks,
            QtGui.QFileDialog.DontUseNativeDialog,
        ]

        if folders:
            # browse folders specifics
            caption = "Browse folders to select engine location"
            file_mode = QtGui.QFileDialog.Directory
            options.append(QtGui.QFileDialog.ShowDirsOnly)
        else:
            # browse files specifics
            caption = "Browse files to to select engine location"
            file_mode = QtGui.QFileDialog.ExistingFiles

        # create the dialog
        file_dialog = QtGui.QFileDialog(parent=self, caption=caption)
        file_dialog.setLabelText(QtGui.QFileDialog.Accept, "Select")
        file_dialog.setLabelText(QtGui.QFileDialog.Reject, "Cancel")
        file_dialog.setFileMode(file_mode)
        file_dialog.setNameFilter("Unreal Project Files (*.uproject)")  # Filter only .uproject files

        # set the appropriate options
        for option in options:
            file_dialog.setOption(option)

        # browse!
        if not file_dialog.exec_():
            return

        original_length = len(self.playlistnames)
        # process the browsed files/folders for publishing
        paths = file_dialog.selectedFiles()
        if paths:
            # add the engine location to the list
            for path in paths:
                path.replace("\\", "/")
                if not os.path.exists(path):
                    msg = 'Unable to add engine location {} as it does not exist'.format(path)
                    self.log_status(msg)
                    continue
                if path in self.playlistnames:
                    msg = 'Unable to add engine location {} as it already exists'.format(path)
                    self.log_status(msg)
                    continue

                #msg = 'Adding engine location: {} to the top of the list'.format(path)
                #self.log_status(msg)
                self.playlistnames.appendleft(path)


        current_length = len(self.playlistnames)
        diff = current_length - original_length
        if diff > 0:
            if diff == 1:
                msg = "\n <span style='color:#2C93E2'>Adding 1 project path to the top of the list</span> \n"
            else:
                msg = "\n <span style='color:#2C93E2'>Adding {} project paths to the top of the list</span> \n".format(diff)


            self.log_status(msg)
            self.populate_playlist()
            self.select_first_playlist()


    def select_first_playlist(self):
        self.playlistSelection.setCurrentRow(0)
        self.ui.selectedPlaylistInput.setText(self.playlistnames[0])

    def log(self, msg, error=0):
        if logger:
            if error:
                logger.warn(msg)
            else:
                logger.info(msg)

        print(msg)

    def get_engine_location_file(self):

        file_path = None
        unreal_folder = None
        if sys.platform.startswith("linux"):
            # ~/.shotgun/logs/unreal
            unreal_folder = os.path.join(os.path.expanduser("~"), ".unreal")
        elif sys.platform == "darwin":
            # ~/Library/Logs/Shotgun
            unreal_folder = os.path.join(os.path.expanduser("~"),  ".unreal")
        elif sys.platform == "win32":
            # %APPDATA%\Shotgun\logs\
            #unreal_folder = os.path.join(os.environ["APPDATA"], "Shotgun", "Logs", "unreal")
            home_dir = expanduser("~")
            unreal_folder = "{}/.unreal".format(home_dir)

        else:
            raise RuntimeError("Platform '%s' not supported!" % sys.platform)
        if unreal_folder:
            if not os.path.exists(unreal_folder):
                os.makedirs(unreal_folder)
            if self.projectName:
                file_name = "{}.txt".format(self.projectName)
                file_path = "{}/{}".format(unreal_folder, file_name)
                file_path.replace("\\", "/")

        msg = "\n <span style='color:#2C93E2'>Project paths file: {}</span> \n".format(file_path)
        self.log_status(msg)


        return file_path

    def get_sg_project_info(self):
        sg_project_info = self.sg.find_one('Project', [['name', 'is', self.projectName]], ['tank_name', 'id', 'sg_default_config'])
        logger.debug("SG Project Info: {}".format(sg_project_info))
        self.sg_project_id = sg_project_info['id']
        self.launch_dict["sg_project_id"] = self.sg_project_id
        # get the configuration name and id

        #self.sg_project_tank_name = sg_project_info['tank_name']
        #tankName = self.sg.find_one('Project', [['name', 'is', self.projectName]], ['tank_name', 'id'])['tank_name']
        #projectPath = os.path.join(self.localStorage, tankName)
        # self.log('PROJECT PATH: {}'.format(projectPath))
        #return projectPath

    def get_sg_config_info(self):
        """Get the shotgun config info for the current project."""
        pass

    def get_engine_location(self):
        if self.current_unreal_project_path and "Projects" in self.current_unreal_project_path:
            unreal_root = self.current_unreal_project_path.split("Projects")[0]
            self.engine_location = "{}Engine/Binaries/Win64/UnrealEditor.exe".format(unreal_root)
            self.engine_location.replace("\\", "/")
            self.launch_dict["unreal_engine_location"] = self.engine_location
    
    def get_unreal_project_info(self):
        self.current_unreal_project_path = self.ui.selectedPlaylistInput.text()
        self.current_unreal_project_path.replace("\\", "/")
        self.launch_dict["unreal_project_path"] = self.current_unreal_project_path
        self.launch_dict["unreal_project"] = os.path.dirname(self.current_unreal_project_path)

    def prepare_launch(self):
        # Save the project file path
        self.save_project_paths_file()
        self.get_unreal_project_info()
        self.get_engine_location()

        self.get_sg_project_info()
        msg = "\n <span style='color:#2C93E2'>Unreal Launch data is:</span> \n"
        self.log_status(msg)
        for k, v in self.launch_dict.items():
            msg = "{}: {}".format(k, v)
            self.log_status(msg)

        #self.get_sg_config_info()
        #self.launch_dict["sg_config_info"] = self.sg_config_info

    def launch_unreal(self):
        """Launches Unreal Engine using the engine location file created by this script."""
        

        self.prepare_launch()
        launcher = UnrealLauncher(self.launch_dict)

        # Run WITHOUT using the SG toolkit
        # launcher.env_run()

        # Run using the SG toolkit manager
        msg = "\n <span style='color:#2C93E2'>Launching Unreal Editor, please wait ...</span> \n"
        self.log_status(msg)
        launcher.sg_api_run()

        # close the dialog
        #self.close()


    def add_status(self, status):
        self.ui.status_dialog.append(status)
        self.setVericalScroll()
        self.widget_app.processEvents()


    def log_status(self, msg, error=0):
        txt = ""
        if logger:
            if error:
                logger.warn(msg)
                txt = "Warning: " + msg

            else:
                logger.debug(msg)
                txt = msg

        self.add_status(msg)



    def setVericalScroll(self):
        self.ui.status_dialog.verticalScrollBar().setValue(self.ui.status_dialog.verticalScrollBar().maximum())


