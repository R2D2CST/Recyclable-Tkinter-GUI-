# Native Python Libraries
from abc import ABC, abstractmethod
import ctypes
import os
import platform
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any

# Third Party Libraries

# Self Build Libraries

# Operative System Paths and Constants
OPERATING_SYSTEM = platform.system()
ICON_ASSETS_PATH = os.path.join("Assets","crown.icon")

#Abstract Class For Application Windows
class AppWindow(ABC, tk.Tk):
    """
    An abstract base class for creating a standardized application window using Tkinter.

    This class inherits from both ABC and tk.Tk to provide abstract methods that must be
    implemented by subclasses and to inherit all Tkinter window functionalities. It
    handles common window configurations like user settings persistence, icon and header
    setup, and dynamic theme application (light/dark mode).
    """

    def __init__(
        self,
        screenName=None,
        baseName=None,
        className="Tk",
        useTk=True,
        sync=False,
        use=None,
    ):
        """
        Initializes the AppWindow, inheriting from tk.Tk.

        It sets up the window by loading user configuration, building the icon and header,
        and applying the saved theme. It then calls the abstract _buildWidgets method
        which must be implemented by any subclass.
        """
        super().__init__(
            screenName,
            baseName,
            className,
            useTk,
            sync,
            use,
        )

        self.operatingSystem = OPERATING_SYSTEM
        self.configDict: Dict[str, Any] = {}

        self._getUserConfig()  # We get user configuration settings.
        # self._buildIconAndHeader()  # We set the Icon and Header in the Window.
        self._applyTheme()  # We apply the user configuration theme.

        pass

    @abstractmethod
    def _getUserConfig(self) -> None:
        """
        Loads user configuration settings from a file or sets default values if the file
        does not exist.

        The settings are stored in the self.configDict attribute.
        """

        self.configDict = config.getConfigData()

        pass

    def _buildIconAndHeader(self) -> None:
        """
        Sets the window's icon based on the operating system and sets the window title.
        TODO: The macOS implementation is currently a To-Do.
        """
        # Set the icon based on the operating system

        try:
            if self.operatingSystem == "Windows":
                # Windows uses .ico files
                iconPath = os.path.join(ICON_ASSETS_PATH, "crown.ico")
                self.iconbitmap(default=iconPath)

                """
                elif self.operatingSystem == "Linux":
                    # Linux with Tkinter supports .xbm and .gif formats.
                    # To support .png, we need to use a PhotoImage.
                    iconPath = os.path.join(ICON_ASSETS_PATH, "crown.xbm")
                    if os.path.exists(iconPath):
                        self.iconbitmap(default=f"@{iconPath}")
                    else:
                        # Fallback to PNG if XBM is not available
                        pngPath = os.path.join(ICON_ASSETS_PATH, "crown.png")
                        if os.path.exists(pngPath):
                            image = tk.PhotoImage(file=pngPath)
                            self.call("wm", "iconphoto", self._w, image)
                """
            elif self.operatingSystem == "Linux":
                # Linux with Tkinter supports .xbm and .gif formats.
                # To support .png, we need to use a PhotoImage.
                iconPath = os.path.join(ICON_ASSETS_PATH, "crown.xbm")

                if os.path.exists(iconPath):
                    # CORREGIDO: Usar la ruta con @ como argumento posicional, NO con 'default='.
                    self.iconbitmap(f"@{iconPath}")
                else:
                    # Fallback to PNG if XBM is not available
                    pngPath = os.path.join(ICON_ASSETS_PATH, "crown.png")
                    if os.path.exists(pngPath):
                        # Este método ya es correcto.
                        image = tk.PhotoImage(file=pngPath)
                        self.call("wm", "iconphoto", self._w, image)
            elif self.operatingSystem == "Darwin":  # macOS
                # macOS supports .icns files
                iconPath = os.path.join(ICON_ASSETS_PATH, "crown.icns")
                self.iconbitmap(default=iconPath)
        except tk.TclError as e:
            # Handle cases where the icon file is not found or is corrupted
            print(f"Warning: Could not set window icon. Error: {e}")

    def _applyTheme(self) -> None:
        """
        Applies the theme (Light or Dark) based on the user's configuration.

        Raises:
            TypeError: If the 'Theme' value in the configuration is not 'Dark' or 'Light'.
        """

        if self.configDict.get("Theme", False) == "Light":
            self._setLightMode()
        elif self.configDict.get("Theme", False) == "Dark":
            self._setDarkMode()
        else:
            raise TypeError(f"Theme must be 'Dark' or 'Light'.")

    def _setLightMode(self) -> None:
        """
        Method apply's the light mode into the window.
        """
        self.configure(bg="white")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background="white", foreground="black")
        style.map(
            "TButton", background=[("active", "lightgrey"), ("!disabled", "white")]
        )
        style.configure(
            "Treeview", background="white", foreground="black", fieldbackground="white"
        )
        style.configure("TProgressbar", troughcolor="white", background="lightgrey")
        self._applyThemeToAllWidgets("light")
        self.Theme = "light"

        # Changes title bar into light mode.
        if self.operatingSystem == "Windows":
            HWND = ctypes.windll.user32.GetParent(self.winfo_id())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                HWND,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(ctypes.c_int(0)),
                ctypes.sizeof(ctypes.c_int(1)),
            )

        pass

    def _setDarkMode(self) -> None:
        """
        Method apply's the dark mode into the window.
        """
        self.configure(bg="black")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background="black", foreground="white")
        style.map(
            "TButton", background=[("active", "darkgrey"), ("!disabled", "black")]
        )
        style.configure(
            "Treeview", background="black", foreground="white", fieldbackground="black"
        )
        style.configure("TProgressbar", troughcolor="black", background="darkgrey")
        self._applyThemeToAllWidgets("dark")
        self.Theme = "dark"

        # Changes title bar into dark mode.
        if self.operatingSystem == "Windows":
            HWND = ctypes.windll.user32.GetParent(self.winfo_id())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                HWND,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(ctypes.c_int(1)),
                ctypes.sizeof(ctypes.c_int(1)),
            )

        pass

    def _applyThemeToWidget(self, widget, theme: str) -> None:
        """
        Method apply's the theme into to each widget in the frame.
        """
        if isinstance(widget, tk.Frame):
            widget.configure(bg="black" if theme == "dark" else "white")
        elif isinstance(widget, tk.Label):
            widget.configure(
                bg="black" if theme == "dark" else "white",
                fg="white" if theme == "dark" else "black",
            )
        elif isinstance(widget, tk.Entry):
            widget.configure(
                bg="black" if theme == "dark" else "white",
                fg="white" if theme == "dark" else "black",
            )
        elif isinstance(widget, tk.Text):
            widget.configure(
                bg="black" if theme == "dark" else "white",
                fg="white" if theme == "dark" else "black",
            )
        elif isinstance(widget, tk.Button):
            widget.configure(
                bg="black" if theme == "dark" else "white",
                fg="white" if theme == "dark" else "black",
            )
        elif isinstance(widget, tk.Radiobutton):
            widget.configure(
                bg="black" if theme == "dark" else "white",
                fg="white" if theme == "dark" else "black",
            )
        elif isinstance(widget, ttk.Treeview):
            style = ttk.Style(widget)
            style.configure(
                "Treeview",
                background="black" if theme == "dark" else "white",
                foreground="white" if theme == "dark" else "black",
                fieldbackground="black" if theme == "dark" else "white",
            )
        elif isinstance(widget, ttk.Progressbar):
            style = ttk.Style(widget)
            style.configure(
                "TProgressbar",
                troughcolor="black" if theme == "dark" else "white",
                background="darkgrey" if theme == "dark" else "lightgrey",
            )
        for child in widget.winfo_children():
            self.__applyThemeToWidget(child, theme)
        pass

    def _applyThemeToAllWidgets(self, theme: str) -> None:
        """
        Apply the theme to all widgets in the window.
        """
        for widget in self.winfo_children():
            self.__applyThemeToWidget(widget, theme)
        pass

    @abstractmethod
    def _buildWidgets(self):
        """
        An abstract method that must be implemented by subclasses to build and
        place all widgets within the window.
        """
        pass

    pass
