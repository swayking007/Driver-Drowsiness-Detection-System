"""
SaveLife Launcher
Entry point for the Driver Drowsiness Detection System with authentication.

This module presents a Tkinter-based login/signup flow before allowing
access to the existing OpenCV-based detection system defined in main.py.
"""

import traceback
import tkinter as tk
from tkinter import ttk, messagebox

from database.db_manager import DatabaseManager
from ui.login import LoginFrame
from ui.signup import SignupFrame
from ui.dashboard import DashboardFrame


class SaveLifeApp(tk.Tk):
    """
    Main Tkinter application that manages authentication and dashboard screens.
    """

    def __init__(self) -> None:
        super().__init__()

        self.title("SaveLife - Driver Drowsiness Detection")
        self.geometry("480x360")
        self.resizable(False, False)

        self._configure_style()

        self.db_manager = DatabaseManager()
        self.current_user: str | None = None
        self.current_frame: ttk.Frame | None = None

        self.protocol("WM_DELETE_WINDOW", self._on_exit)

        # Center window after it has been drawn
        self.after(0, self._center_window)

        # Start with login screen
        self.show_login()

    def _configure_style(self) -> None:
        """Configure a simple modern-looking style for the UI."""
        style = ttk.Style(self)
        try:
            # Use a theme that looks modern on most platforms
            style.theme_use("clam")
        except tk.TclError:
            # Fall back silently if theme is not available
            pass

        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5")
        style.configure("TButton", padding=6)
        style.map(
            "TButton",
            foreground=[("disabled", "#999999")],
        )

    def _center_window(self) -> None:
        """Center the main window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _clear_current_frame(self) -> None:
        """Destroy the current content frame, if any."""
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_login(self) -> None:
        """Display the login screen."""
        self._clear_current_frame()
        self.current_user = None

        self.current_frame = LoginFrame(
            self,
            db_manager=self.db_manager,
            on_login_success=self._on_login_success,
            on_go_to_signup=self.show_signup,
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_signup(self) -> None:
        """Display the signup screen."""
        self._clear_current_frame()

        self.current_frame = SignupFrame(
            self,
            db_manager=self.db_manager,
            on_signup_success=self._on_signup_success,
            on_go_to_login=self.show_login,
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self, username: str) -> None:
        """Display the dashboard for the given user."""
        self._clear_current_frame()
        self.current_user = username

        self.current_frame = DashboardFrame(
            self,
            username=username,
            on_start_detection=self._start_detection,
            on_logout=self.show_login,
            on_exit=self._on_exit,
        )
        self.current_frame.pack(fill="both", expand=True)

    def _on_login_success(self, username: str) -> None:
        """Handle successful login."""
        self.show_dashboard(username)

    def _on_signup_success(self, username: str) -> None:
        """Handle successful signup."""
        messagebox.showinfo(
            "Signup Successful",
            "Your account has been created and you are now logged in.",
        )
        self.show_dashboard(username)

    def _start_detection(self) -> None:
        """
        Start the existing detection system.

        The Tkinter window is temporarily hidden while the OpenCV window is
        active. When the detection program exits, the dashboard is shown again.
        """
        # Import here to avoid any circular import issues
        import main as detection_main

        self.withdraw()
        error: Exception | None = None

        try:
            detection_main.main()
        except Exception as exc:  # noqa: BLE001
            # Record the error and show a user-friendly message after restoring UI
            error = exc
            traceback.print_exc()
        finally:
            # Restore the launcher window
            self.deiconify()
            self._center_window()

            if error is not None:
                messagebox.showerror(
                    "Error",
                    f"An error occurred while running the detection system:\n{error}",
                )

            # Return the user to the dashboard or login, depending on state
            if self.current_user:
                self.show_dashboard(self.current_user)
            else:
                self.show_login()

    def _on_exit(self) -> None:
        """Exit the application cleanly."""
        self.destroy()


def main() -> None:
    """Application entry point for the launcher."""
    app = SaveLifeApp()
    app.mainloop()


if __name__ == "__main__":
    main()

