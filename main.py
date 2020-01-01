""" Main Module """

import logging
import os
import subprocess
import mimetypes
import shutil
import gi
gi.require_version("Gtk", "3.0")
# pylint: disable=import-error
from gi.repository import Gio, Gtk
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

LOGGING = logging.getLogger(__name__)

FILE_SEARCH_ALL = "ALL"

FILE_SEARCH_DIRECTORY = "DIR"

FILE_SEARCH_FILE = "FILE"


class FileSearchExtension(Extension):
    """ Main Extension Class  """

    def __init__(self):
        """ Initializes the extension """
        super(FileSearchExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def search(self, query, file_type=None, fd_cmd="fd"):
        """ Searches for Files using fd command """
        base_dir = self.preferences["base_dir"]
        timeout = self.preferences["timeout"]
        threads = self.preferences["threads"]

        cmd = ["timeout", timeout, "ionice", "-c", "3", fd_cmd, "--hidden"]

        if file_type == FILE_SEARCH_FILE:
            cmd.append("-t")
            cmd.append("f")
        elif file_type == FILE_SEARCH_DIRECTORY:
            cmd.append("-t")
            cmd.append("d")

        if threads != "0":
            cmd.append("--threads")
            cmd.append(threads)

        cmd.append(query)
        cmd.append(base_dir)

        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        out, err = process.communicate()

        if err:
            self.logger.error(err)
            return []

        files = out.split("\n".encode())
        files = list([_f for _f in files if _f])  # remove empty lines

        result = []
        #get folder icon outside loop, so it only happens once
        file = Gio.File.new_for_path("/")
        folder_info = file.query_info("standard::icon", 0, Gio.Cancellable())
        folder_icon = folder_info.get_icon().get_names()[0]
        icon_theme = Gtk.IconTheme.get_default()
        icon_folder = icon_theme.lookup_icon(folder_icon, 128, 0)
        if icon_folder:
            folder_icon = icon_folder.get_filename()
        else:
            folder_icon = "images/folder.png"

        # pylint: disable=C0103
        for f in files[:15]:
            if os.path.isdir(f):
                icon = folder_icon
            else:
                type_, encoding = mimetypes.guess_type(f.decode("utf-8"))

                if type_:
                    file_icon = Gio.content_type_get_icon(type_)
                    file_info = icon_theme.choose_icon(file_icon.get_names(), 128, 0)
                    if file_info:
                        icon = file_info.get_filename()
                    else:
                        icon = "images/file.png"
                else:
                    icon = "images/file.png"

            result.append({"path": f, "name": f, "icon": icon})

        return result

    def get_open_in_terminal_script(self, path):
        """ Returns the script based on the type of terminal """
        terminal_emulator = self.preferences["terminal_emulator"]

        # some terminals might work differently. This is already prepared for that.
        if terminal_emulator in [
                "gnome-terminal", "terminator", "tilix", "xfce-terminal"
        ]:
            return RunScriptAction(terminal_emulator,
                                   ["--working-directory", path])

        return DoNothingAction()


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """

    # pylint: disable=unused-argument,no-self-use
    def on_event(self, event, extension):
        """ Handles the event """
        fd_cmd = extension.preferences["fd_cmd"]
        if shutil.which(fd_cmd) is None:
            return RenderResultListAction([
                ExtensionResultItem(icon="images/icon.png",
                                    name=f"Command {fd_cmd} is not found, please install it first",
                                    on_enter=HideWindowAction())
            ])

        query = event.get_argument()

        if not query or len(query) < 3:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="Keep typing your search criteria ...",
                    on_enter=DoNothingAction())
            ])

        keyword = event.get_keyword()
        keyword_id = None
        # Find the keyword id using the keyword (since the keyword can be changed by users)
        for kw_id, kw in list(extension.preferences.items()):
            if kw == keyword:
                keyword_id = kw_id

        file_type = FILE_SEARCH_ALL
        if keyword_id == "ff_kw":
            file_type = FILE_SEARCH_FILE
        elif keyword_id == "fd_kw":
            file_type = FILE_SEARCH_DIRECTORY

        results = extension.search(query.strip(), file_type, fd_cmd)

        if not results:
            return RenderResultListAction([
                ExtensionResultItem(icon="images/icon.png",
                                    name=f"No Results found matching {query}",
                                    on_enter=HideWindowAction())
            ])

        items = []
        for result in results[:15]:
            items.append(
                ExtensionSmallResultItem(
                    icon=result["icon"],
                    name=result["path"].decode("utf-8"),
                    on_enter=OpenAction(result["path"].decode("utf-8")),
                    on_alt_enter=extension.get_open_in_terminal_script(
                        result["path"].decode("utf-8"))))

        return RenderResultListAction(items)


if __name__ == "__main__":
    FileSearchExtension().run()
