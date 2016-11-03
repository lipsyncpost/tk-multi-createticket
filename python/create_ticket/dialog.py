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
import threading

# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

TICKET_TYPES = ['Feature',
                'Bug',
                'Notes',
                'Request']


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    submit = QtCore.Signal()

    def __init__(self, entity_type, entity_ids):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)

        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # most of the useful accessors are available through
        # the Application class instance it is often handy to
        # keep a reference to this.
        # You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        # via the self._app handle we can for example access:
        # - The engine, via self._app.engine
        # - A Shotgun API instance, via self._app.shotgun
        # - A tk API instance, via self._app.tk

        # Main signals

        self.ui.submit_btn.clicked.connect(self._on_submit)
        self.ui.cancel_btn.clicked.connect(self._on_cancel)

        # populate the options for the ticket type

        for tt in TICKET_TYPES:
            self.ui.ticketType_box.addItem(tt)

        # lastly, set up our very basic UI
        filters = [['id', 'is', entity_ids]]
        fields = ['code']
        entity = self._app.shotgun.find_one(entity_type, filters, fields)
        selection_text = "Current context: <strong><i>{0}</i></strong>"
        selection_text = selection_text.format(entity['code'])
        self.ui.context_label.setText(selection_text)

    def _on_submit(self):
        self.submit.emit()

    def _on_cancel(self):
        self.close()

    def get_inputs(self):

        # title_box
        # ticketType_box
        # priority_sb
        # desc_box

        _title = self.ui.title_box.text()
        _type = self.ui.ticketType_box.currentText()
        _priority = str(self.ui.priority_sb.value())
        _description = self.ui.desc_box.toPlainText()

        data = {'title': _title,
                'sg_ticket_type': _type,
                'sg_priority': _priority,
                'description': _description
                }

        return data
