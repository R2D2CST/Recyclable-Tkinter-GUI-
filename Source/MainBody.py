# Native Python Libraries
from typing import (
    Any,
    Callable,
    Dict,
)
import tkinter as tk

# Third Party Libraries


# Self Build Libraries
from ABS_Window import AppWindow

class MainBody(AppWindow):
    """
    Generates the main body frame where the user will interact with each module 
    in tha application.
    """

    def __init__(
        self,
        user: str,
        screenName=None,
        baseName=None,
        className="Tk",
        useTk=True,
        sync=False,
        use=None,
    ):
        super().__init__(
            screenName,
            baseName,
            className,
            useTk,
            sync,
            use,
        )

        # We built the widgets in our window.
        self._buildMenuBar()
        self._buildWidgets()

        # We set the window title
        self.title("Window Title")
        self._buildIconAndHeader()

        # We set a geometry for the emerging window.
        self.geometry("600x400")  # Width x Hight

        # We initialize our main loop.
        self.mainloop()

        pass

    def _buildMenuBar(self):
        """
        Builds the menu bar where the user will select how to procede to work.
            Args: None
            Returns: None
            Raises: None
        """
        # * We build the menu station bar
        self.menuBar = tk.Menu(self)

        # * We build the settings menu
        settingsMenu = tk.Menu(self.menuBar, tearoff=0)
        # We place the settings menu into the menu station bar
        self.menuBar.add_cascade(
            label="Settings",
            menu=settingsMenu,
        )

        # We build the sub menu for Light and Dark view mode
        submenuViewMode = tk.Menu(settingsMenu, tearoff=0)
        # We place the recent submenu into the settings menu
        settingsMenu.add_cascade(
            label="View Mode",
            menu=submenuViewMode,
        )

        # We set the light and dark command buttons
        submenuViewMode.add_command(
            label="Light Mode",
            command=lambda: (
                config.changeTheme(theme="Light"),
                self._refresh(),
            ),
        )
        submenuViewMode.add_command(
            label="Dark Mode",
            command=lambda: (
                config.changeTheme(theme="Dark"),
                self._refresh(),
            ),
        )


        # * We build the project management menu"
        projectManagement = tk.Menu(self.menuBar, tearoff=0)

        # We place the project management menu into our menubar
        self.menuBar.add_cascade(
            label="ProjectManagement",
            menu=projectManagement,
        )

        # We build the submenu for document render modules
        documentRender = tk.Menu(projectManagement, tearoff=0)

        # We set the submenu document render into our main window
        projectManagement.add_cascade(
            label="submenuDocRender",
            menu=documentRender,
        )

        # We set the create, work and render project commands

        documentRender.add_command(
            label="submenuNewProjectDocRender",
            command=lambda: print("Not Implemented"),
        )
        documentRender.add_command(
            label="submenuProjectDocRender",
            command=lambda: print("Not Implemented"),
        )

        """
        NOTE: Example of how to call the lambda function with several key arguments.
        command=lambda parent=self.mainFrame, language=self.languageDict, clear=self.__deleteWorkspace, theme=self.__applyTheme: DocRender(
            frame=parent,
            language=language,
            clear=clear,
            theme=theme,
        ),
        """

        # ! We set the menu station bar within the window
        self.config(menu=self.menuBar)

        pass

    def _buildWidgets(self):

        # Main frame were all the tabs will be loaded.
        self.mainFrame = tk.Frame(self)

        self.mainFrame.pack()

        pass

    def _buildNewTab(self):
        pass

    def _buildWidgetsInTab(self, workspaceClass: Callable[..., object]) -> None:
        """
        Clears the current workspace and loads a new one from a dedicated class.

        Args:
            workspaceClass (Callable): The class of the new workspace to be loaded.
        """
        # Clear existing widgets from the main frame.
        self._clearWorkspace()

        # Create an instance of the new workspace class and load it.
        # This instance is responsible for building its own widgets.
        self.currentWorkspace = workspaceClass(
            parentFrame=self.mainFrame, appInstance=self, configDict=self.configDict
        )
        pass

    def _clearWidgetsInTab(self):
        """
        Procedure deletes every widget within the application workspace.
            Args: None
            Returns: None
            Raises: None
        """
        [
            self.mainFrame.winfo_children()[frame].destroy()
            for frame in range(len(self.mainFrame.winfo_children()))
        ]
        return None

    def _refresh(self):
        """
        Method refreshes the application with the applied changes.
            Args: None
            Returns: None
            Raises: None
        """
        self.destroy()
        self.__init__()
        pass

    pass
