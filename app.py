# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


from sgtk.platform import Application

class CreateTicket(Application):
    """
    The app entry point. This class is responsible for intializing and tearing down
    the application, handle menu registration etc.
    """

    def init_app(self):
        """
        Called as the application is being initialized
        """

        # first, we use the special import_module command to access the app module
        # that resides inside the python folder in the app. This is where the actual UI
        # and business logic of the app is kept. By using the import_module command,
        # toolkit's code reload mechanism will work properly.
        create_ticket = self.import_module("create_ticket")

        self.__ticketHandler = create_ticket.TicketHandler(self)

        # now register a *command*, which is normally a menu entry of some kind on a Shotgun
        # menu (but it depends on the engine). The engine will manage this command and 
        # whenever the user requests the command, it will call out to the callback.

        # first, set up our callback, calling out to a method inside the app module contained
        # in the python folder of the app. 
        #
        # Note! By passing the additional (special) entity_type and entity_ids parameters,
        # the Shotgun enging will pass the current selection into the app via those parameters.
        # Also note that this does not work in any other engines.        

        deny_permissions = self.get_setting("deny_permissions")
        deny_platforms = self.get_setting("deny_platforms")

        # in order for the shotgun engine to enable multiple selection mode,
        #  we need to pass a special param flag:

        # register commands:
        display_name = self.get_setting("display_name")

        # "Publish Render" ---> publish_render
        command_name = display_name.lower().replace(" ", "_")
        if command_name.endswith("..."):
            command_name = command_name[:-3]

        parameters = {
            "short_name": command_name,
            "title": "{} ...".format(display_name),
            "deny_permissions": deny_permissions,
            "deny_platforms": deny_platforms,
            "supports_multiple_selection": False
        }

        menu_name = "{} ...".format(display_name)
        if self.engine.name == "tk-shotgun":
            menu_name = command_name

        # now register the command with the engine
        self.engine.register_command(menu_name,
                                     self.__ticketHandler.show_ticket_dlg,
                                     parameters)
