
import tank
from tank import TankError
from tank.platform.qt import QtCore, QtGui


class TicketHandler(object):

    def __init__(self, app):

        self._app = app

    def show_ticket_dlg(self, entity_type=None, entity_ids=None):
        """
        Shows the main dialog window, using the special Shotgun multi-select mode.
        """
        # in order to handle UIs seamlessly, each toolkit engine has methods for launching
        # different types of windows. By using these methods,
        # your windows will be correctly decorated and handled
        # in a consistent fashion by the system.

        # we pass the dialog class to this method and leave the actual construction
        # to be carried out by toolkit.

        try:
            from .dialog import AppDialog

            form = self._app.engine.show_dialog("Create Support Ticket",
                                                self._app,
                                                AppDialog,
                                                entity_type,
                                                entity_ids)
            form.submit.connect(lambda f=form: self._on_submit(f))
        except TankError, e:
            QtGui.QMessageBox.information(None, "Unable To show ticket dialog!", "%s" % e)

        except Exception, e:
            self._app.log_exception("Unable to show ticket dialog! : {0}".format(e))

    def _on_submit(self, form):
        """
        Run the creation of the ticket based on input from the dialog
        """
        try:
            inputs = form.get_inputs()

            self._app.log_debug(inputs)

            ctx = self._app.context

            sg_link = ctx.entity if ctx.entity else ctx.project

            if ctx.task:
                sg_link = ctx.task

            data = {"sg_link": sg_link,
                    "project": ctx.project,
                    "created_by": ctx.user
                    }

            data.update(inputs)

            self._app.shotgun.create('Ticket', data)

        except TankError, e:
            QtGui.QMessageBox.information(None, "Unable To submit!", "%s" % e)

        except Exception, e:
            self._app.log_exception("Unable to submit : {0}".format(e))

        finally:
            # finally close the form
            form.close()
