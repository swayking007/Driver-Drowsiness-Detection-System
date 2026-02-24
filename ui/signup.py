import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from database.db_manager import DatabaseManager


class SignupFrame(ttk.Frame):
    """
    Signup screen for creating new SaveLife accounts.

    This frame allows users to register with a username and password.
    """

    def __init__(
        self,
        master: tk.Misc,
        db_manager: DatabaseManager,
        on_signup_success: Callable[[str], None],
        on_go_to_login: Callable[[], None],
        **kwargs,
    ) -> None:
        """
        Initialize the signup frame.

        Args:
            master: Parent Tkinter widget.
            db_manager: Database manager instance for user creation.
            on_signup_success: Callback invoked with username when signup succeeds.
            on_go_to_login: Callback to navigate back to the login screen.
            **kwargs: Additional ttk.Frame options.
        """
        super().__init__(master, **kwargs)

        self.db_manager = db_manager
        self.on_signup_success = on_signup_success
        self.on_go_to_login = on_go_to_login

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        """Build and layout all widgets for the signup screen."""
        self.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            self,
            text="Create Account",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="n")

        subtitle_label = ttk.Label(
            self,
            text="Sign up to use the SaveLife system",
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

        confirm_label = ttk.Label(form_frame, text="Confirm Password:")
        confirm_label.grid(row=2, column=0, pady=5, sticky="w")

        confirm_entry = ttk.Entry(
            form_frame,
            textvariable=self.confirm_var,
            show="*",
        )
        confirm_entry.grid(row=2, column=1, pady=5, sticky="ew")

        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, pady=10, padx=40, sticky="ew")
        button_frame.columnconfigure((0, 1), weight=1)

        signup_button = ttk.Button(
            button_frame,
            text="Sign Up",
            command=self._handle_signup,
        )
        signup_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        back_button = ttk.Button(
            button_frame,
            text="Back to Login",
            command=self.on_go_to_login,
        )
        back_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            foreground="red",
            wraplength=360,
        )
        status_label.grid(row=4, column=0, pady=(5, 15), padx=20, sticky="ew")

    def _handle_signup(self) -> None:
        """Validate input, create a new user, and trigger success callback."""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        confirm = self.confirm_var.get()

        self.status_var.set("")

        if not username or not password or not confirm:
            self.status_var.set("All fields are required.")
            return

        if len(password) < 6:
            self.status_var.set("Password must be at least 6 characters long.")
            return

        if password != confirm:
            self.status_var.set("Passwords do not match.")
            return

        success, message = self.db_manager.create_user(username, password)

        if success:
            self.status_var.set("")
            messagebox.showinfo("Signup Successful", "Your account has been created.")
            self.on_signup_success(username)
        else:
            self.status_var.set(message)

