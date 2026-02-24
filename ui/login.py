import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from database.db_manager import DatabaseManager


class LoginFrame(ttk.Frame):
    """
    Login screen for the SaveLife system.

    This frame handles user authentication and provides navigation
    to the signup screen.
    """

    def __init__(
        self,
        master: tk.Misc,
        db_manager: DatabaseManager,
        on_login_success: Callable[[str], None],
        on_go_to_signup: Callable[[], None],
        **kwargs,
    ) -> None:
        """
        Initialize the login frame.

        Args:
            master: Parent Tkinter widget.
            db_manager: Database manager instance for authentication.
            on_login_success: Callback invoked with username when login succeeds.
            on_go_to_signup: Callback to navigate to the signup screen.
            **kwargs: Additional ttk.Frame options.
        """
        super().__init__(master, **kwargs)

        self.db_manager = db_manager
        self.on_login_success = on_login_success
        self.on_go_to_signup = on_go_to_signup

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        """Build and layout all widgets for the login screen."""
        self.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            self,
            text="SaveLife Login",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="n")

        subtitle_label = ttk.Label(
            self,
            text="Driver Drowsiness Detection System",
            font=("Segoe UI", 10),
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 10), padx=20, sticky="n")

        form_frame = ttk.Frame(self)
        form_frame.grid(row=2, column=0, padx=40, pady=10, sticky="ew")
        form_frame.columnconfigure(1, weight=1)

        username_label = ttk.Label(form_frame, text="Username:")
        username_label.grid(row=0, column=0, pady=5, sticky="w")

        username_entry = ttk.Entry(form_frame, textvariable=self.username_var)
        username_entry.grid(row=0, column=1, pady=5, sticky="ew")
        username_entry.focus()

        password_label = ttk.Label(form_frame, text="Password:")
        password_label.grid(row=1, column=0, pady=5, sticky="w")

        password_entry = ttk.Entry(
            form_frame,
            textvariable=self.password_var,
            show="*",
        )
        password_entry.grid(row=1, column=1, pady=5, sticky="ew")

        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, pady=10, padx=40, sticky="ew")
        button_frame.columnconfigure((0, 1), weight=1)

        login_button = ttk.Button(
            button_frame,
            text="Login",
            command=self._handle_login,
        )
        login_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        signup_button = ttk.Button(
            button_frame,
            text="Sign Up",
            command=self.on_go_to_signup,
        )
        signup_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            foreground="red",
            wraplength=360,
        )
        status_label.grid(row=4, column=0, pady=(5, 15), padx=20, sticky="ew")

    def _handle_login(self) -> None:
        """Validate credentials and trigger login callback on success."""
        username = self.username_var.get().strip()
        password = self.password_var.get()

        self.status_var.set("")

        success, message = self.db_manager.validate_login(username, password)

        if success:
            self.status_var.set("")
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            self.on_login_success(username)
        else:
            self.status_var.set(message)

