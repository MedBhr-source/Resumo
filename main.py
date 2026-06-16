import sys
from PySide6.QtWidgets import QApplication, QMessageBox

from UI.auth_window import AuthWindow
from UI.main_win import MainWindow

from controllers.app_controller import AppController
from db.db_manager import DBManager

window     = None
controller = None
auth_win   = None

def main():
    global window, controller, auth_win

    app = QApplication(sys.argv)
    db  = DBManager()

    def start_main_app(username, pswrd):
        global window, controller

        if db.verify_user(username, pswrd):
            print(f" Login successful for: {username}")

            user_data = db.fetch_query(
                "SELECT user_id FROM users WHERE username = %s", (username,)
            )

            if user_data:
                user_id = user_data[0]["user_id"]

                auth_win.close()

                def handle_logout():
                    global auth_win
                    if window:
                        window.close()
                    auth_win = AuthWindow(
                        on_login_success=start_main_app,
                        db_manager=db,
                    )
                    auth_win.show()

                window     = MainWindow(username, on_logout=handle_logout)
                controller = AppController(window, user_id)
                window.show()

            else:
                QMessageBox.critical(auth_win, "Database Error",
                                     "Could not find User ID in database.")
        else:
            QMessageBox.warning(auth_win, "Login Failed",
                                "Invalid Username or Password! Please try again.")

    auth_win = AuthWindow(on_login_success=start_main_app, db_manager=db)
    auth_win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
