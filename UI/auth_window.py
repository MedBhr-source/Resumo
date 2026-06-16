from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QGraphicsDropShadowEffect, QMessageBox
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup, QTimer
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPixmap, QBrush
import os
import random

class AuthWindow(QWidget):

    W = 520
    H = 700

    def __init__(self, on_login_success, db_manager):
        super().__init__()
        self.on_login_success = on_login_success
        self.db = db_manager

        self.setWindowTitle("Resumo - Sign In")
        self.setFixedSize(self.W, self.H)

        # ── Particle star-field setup ──────────────────────────────────────
        self._stars = [
            {
                "x": random.uniform(0, self.W),
                "y": random.uniform(0, self.H),
                "r": random.uniform(0.6, 2.2),
                "speed": random.uniform(0.15, 0.55),
                "alpha": random.randint(60, 200),
            }
            for _ in range(70)
        ]
        self._particle_timer = QTimer(self)
        self._particle_timer.timeout.connect(self._tick_particles)
        self._particle_timer.start(16)   # ~60 fps

        # Build both panels as direct children (painted over shared bg)
        self.login_panel = self._build_login_panel()
        self.register_panel = self._build_register_panel()

        # Initial positions: login visible, register off-screen to the right
        self.login_panel.setGeometry(0, 0, self.W, self.H)
        self.register_panel.setGeometry(self.W, 0, self.W, self.H)

        self.login_panel.show()
        self.register_panel.show()

    #  HELPERS 

    def _card_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(91, 79, 232, 130))
        shadow.setOffset(0, 12)
        return shadow

    @staticmethod
    def _input_style():
        return """
            QLineEdit {
                padding: 14px 16px;
                background: #0D1525;
                border: 1.5px solid #1E2D4A;
                border-radius: 12px;
                color: #F1F5F9;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1.5px solid #7C5CFC;
                background: #111E35;
            }
        """

    @staticmethod
    def _primary_btn_style():
        return """
            QPushButton {
                padding: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B4FE8, stop:1 #8B5CF6);
                border-radius: 14px;
                color: #FFFFFF;
                font-weight: bold;
                font-size: 15px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6D62F0, stop:1 #9D72F8);
            }
            QPushButton:pressed { background: #4A3FCE; }
        """

    @staticmethod
    def _link_btn_style():
        return """
            QPushButton {
                padding: 10px;
                background: transparent;
                border: none;
                color: #94A3B8;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { color: #38BDF8; }
        """

    #  LOGIN PANEL 

    def _build_login_panel(self):
        panel = QWidget(self)
        panel.setStyleSheet("background: transparent;")

        outer = QVBoxLayout(panel)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedSize(430, 530)
        card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 24px;
                border: 1px solid #1E2D4A;
            }
        """)
        card.setGraphicsEffect(self._card_shadow())

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(18)
        layout.setContentsMargins(44, 44, 44, 44)

        subtitle = QLabel("Resumo - AI Powered")
        subtitle.setStyleSheet(
            "font-size: 13px; color: #94A3B8;"
            "background: transparent; border: none; margin-bottom: 10px;"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)


        icon = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
        pixmap = QPixmap(logo_path)
        icon.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.setStyleSheet("background: transparent; border: none;")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("Welcome back!")
        title.setStyleSheet(
            "font-size: 26px; font-weight: bold; color: #F1F5F9;"
            "background: transparent; border: none;"
        )
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Username")
        self.login_username.setStyleSheet(self._input_style())
        layout.addWidget(self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setStyleSheet(self._input_style())
        # Allow pressing Enter to login
        self.login_password.returnPressed.connect(self._handle_login)
        layout.addWidget(self.login_password)

        btn_login = QPushButton("Sign In")
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setMinimumHeight(50)
        btn_login.setStyleSheet(self._primary_btn_style())
        btn_login.clicked.connect(self._handle_login)
        layout.addWidget(btn_login)

        btn_go_reg = QPushButton("Don't have an account? Sign Up →")
        btn_go_reg.setCursor(Qt.PointingHandCursor)
        btn_go_reg.setStyleSheet(self._link_btn_style())
        btn_go_reg.clicked.connect(self._go_to_register)
        layout.addWidget(btn_go_reg)

        outer.addWidget(card)
        return panel

    #  REGISTER PANEL 

    def _build_register_panel(self):
        panel = QWidget(self)
        panel.setStyleSheet("background: transparent;")

        outer = QVBoxLayout(panel)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedSize(430, 610)
        card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 24px;
                border: 1px solid #1E2D4A;
            }
        """)
        card.setGraphicsEffect(self._card_shadow())

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(14)
        layout.setContentsMargins(44, 36, 44, 36)

        icon = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
        pixmap = QPixmap(logo_path)
        icon.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.setStyleSheet("background: transparent; border: none;")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("Create Account")
        title.setStyleSheet(
            "font-size: 26px; font-weight: bold; color: #F1F5F9;"
            "background: transparent; border: none;"
        )
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Join Resumo today")
        subtitle.setStyleSheet(
            "font-size: 13px; color: #94A3B8;"
            "background: transparent; border: none; margin-bottom: 8px;"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Choose a Username...")
        self.reg_username.setStyleSheet(self._input_style())
        layout.addWidget(self.reg_username)

        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Create a Password...")
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.reg_password.setStyleSheet(self._input_style())
        layout.addWidget(self.reg_password)

        self.reg_confirm = QLineEdit()
        self.reg_confirm.setPlaceholderText("Confirm Password...")
        self.reg_confirm.setEchoMode(QLineEdit.Password)
        self.reg_confirm.setStyleSheet(self._input_style())
        self.reg_confirm.returnPressed.connect(self._handle_register)
        layout.addWidget(self.reg_confirm)

        btn_register = QPushButton("Create Account")
        btn_register.setCursor(Qt.PointingHandCursor)
        btn_register.setMinimumHeight(50)
        btn_register.setStyleSheet(self._primary_btn_style())
        btn_register.clicked.connect(self._handle_register)
        layout.addWidget(btn_register)

        btn_go_login = QPushButton("← Already have an account? Sign In")
        btn_go_login.setCursor(Qt.PointingHandCursor)
        btn_go_login.setStyleSheet(self._link_btn_style())
        btn_go_login.clicked.connect(self._go_to_login)
        layout.addWidget(btn_go_login)

        outer.addWidget(card)
        return panel

    #  ANIMATION 
    def _go_to_register(self):
        """Login exits LEFT  ←  |  Register enters from RIGHT  →"""
        self._animate(
            login_target=QPoint(-self.W, 0),
            register_target=QPoint(0, 0),
        )
        self.setWindowTitle("Resumo — Create Account")

    def _go_to_login(self):
        """Register exits RIGHT  →  |  Login enters from LEFT  ←"""
        self._animate(
            login_target=QPoint(0, 0),
            register_target=QPoint(self.W, 0),
        )
        self.setWindowTitle("Resumo — Sign In")

    def _animate(self, login_target: QPoint, register_target: QPoint):
        """Runs both panel animations in parallel with OutCubic easing."""
        duration = 420
        easing = QEasingCurve.OutCubic

        a_login = QPropertyAnimation(self.login_panel, b"pos")
        a_login.setDuration(duration)
        a_login.setEndValue(login_target)
        a_login.setEasingCurve(easing)

        a_reg = QPropertyAnimation(self.register_panel, b"pos")
        a_reg.setDuration(duration)
        a_reg.setEndValue(register_target)
        a_reg.setEasingCurve(easing)

        # Keep a reference so it isn't GC'd mid-animation
        self._anim_group = QParallelAnimationGroup()
        self._anim_group.addAnimation(a_login)
        self._anim_group.addAnimation(a_reg)
        self._anim_group.start()

    #  BUSINESS LOGIC 

    def _handle_login(self):
        self.on_login_success(self.login_username.text(), self.login_password.text())

    def _handle_register(self):
        username = self.reg_username.text().strip()
        password = self.reg_password.text()
        confirm  = self.reg_confirm.text()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields!")
            return
        if len(password) < 4:
            QMessageBox.warning(self, "Weak Password", "Password must be at least 4 characters long!")
            return
        if password != confirm:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match!")
            return

        existing = self.db.fetch_query(
            "SELECT user_id FROM users WHERE username = %s", (username,)
        )
        if existing:
            QMessageBox.warning(self, "Username Taken", f"'{username}' is already taken.")
            return

        result = self.db.save_user(username, password)
        if result:
            QMessageBox.information(
                self, "Account Created! ✦",
                f"Welcome, {username}!\nYou can now sign in."
            )
            # Clear register fields and slide back to login
            self.reg_username.clear()
            self.reg_password.clear()
            self.reg_confirm.clear()
            self._go_to_login()
        else:
            QMessageBox.critical(self, "Error", "Could not create account. Please try again.")

    #  PARTICLE ANIMATION

    def _tick_particles(self):
        """Move each star upward; wrap around to the bottom when off-screen."""
        for s in self._stars:
            s["y"] -= s["speed"]
            if s["y"] < -4:
                s["y"] = self.H + 4
                s["x"] = random.uniform(0, self.W)
        self.update()   # trigger repaint

    #  BACKGROUND
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Deep gradient base
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#080D1A"))
        gradient.setColorAt(0.5, QColor("#0D1525"))
        gradient.setColorAt(1.0, QColor("#111827"))
        painter.fillRect(self.rect(), gradient)

        # Animated star particles
        for s in self._stars:
            color = QColor(139, 92, 246, s["alpha"])  
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(
                int(s["x"] - s["r"]), int(s["y"] - s["r"]),
                int(s["r"] * 2), int(s["r"] * 2)
            )
