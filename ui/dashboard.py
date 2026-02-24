import tkinter as tk
from tkinter import ttk
from typing import Callable


class DashboardFrame(ttk.Frame):
    """
    Dashboard screen shown after successful login.

    Provides access to start the detection system, log out, or exit.
    """

    def __init__(
        self,
        master: tk.Misc,
        username: str,
        on_start_detection: Callable[[], None],
        on_logout: Callable[[], None],
        on_exit: Callable[[], None],
        **kwargs,
    ) -> None:
        """
        Initialize the dashboard frame.

        Args:
            master: Parent Tkinter widget.
            username: Currently logged-in username.
            on_start_detection: Callback to start the detection system.
            on_logout: Callback to log out and return to login screen.
            on_exit: Callback to close the application.
            **kwargs: Additional ttk.Frame options.
        """
        super().__init__(master, **kwargs)

        self.username = username
        self.on_start_detection = on_start_detection
        self.on_logout = on_logout
        self.on_exit = on_exit

        self._build_ui()

    def _build_ui(self) -> None:
        """Build and layout all widgets for the dashboard screen."""
        self.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            self,
            text="SaveLife Dashboard",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="n")

        welcome_label = ttk.Label(
            self,
            text=f"Welcome, {self.username}!",
            font=("Segoe UI", 12),
        )
        welcome_label.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="n")

        info_label = ttk.Label(
            self,
            text="Use the buttons below to start the drowsiness detection system\n"
            "or manage your session.",
            font=("Segoe UI", 10),
            justify="center",
        )
        info_label.grid(row=2, column=0, pady=(0, 10), padx=30, sticky="n")

        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, pady=10, padx=80, sticky="ew")
        button_frame.columnconfigure(0, weight=1)

        start_button = ttk.Button(
            button_frame,
            text="Start Detection",
            command=self.on_start_detection,
        )
        start_button.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        logout_button = ttk.Button(
            button_frame,
            text="Logout",
            command=self.on_logout,
        )
        logout_button.grid(row=1, column=0, pady=5, sticky="ew")

        exit_button = ttk.Button(
            button_frame,
            text="Exit",
            command=self.on_exit,
        )
        exit_button.grid(row=2, column=0, pady=5, sticky="ew")

