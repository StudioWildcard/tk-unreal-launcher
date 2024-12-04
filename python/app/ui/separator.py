"""
Custom Separator

    This class creates a separator that is similar to that of Maya's
"""
from sgtk.platform.qt import QtCore
for name, cls in QtCore.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls

from sgtk.platform.qt import QtGui
for name, cls in QtGui.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls

class Separator(QFrame):
    def __init__(self):
        """
        Constructor
        """
        super(Separator, self).__init__(parent=None)

        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setFixedHeight(1)
