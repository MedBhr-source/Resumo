from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QProgressBar, QListWidget, 
                             QFrame, QTabWidget, QLineEdit, QGraphicsDropShadowEffect, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QSize, QTimer
from PySide6.QtGui import QColor, QPixmap, QPainter, QLinearGradient, QBrush
import os
import random

# ─────────────────────────────────────────────
#  PALETTE  –  Deep Ocean Blue-Violet
#  BG_DEEP    : #080D1A
#  BG_SURFACE : #111827
#  BG_CARD    : #141D2E
#  BG_HOVER   : #1E2640
#  BORDER     : #1E2D4A  (visible clear border)
#  BORDER_FOC : #7C5CFC  (violet focus ring)
#  PRIMARY_1  : #5B4FE8  (indigo)
#  PRIMARY_2  : #8B5CF6  (violet)
#  ACCENT     : #38BDF8  (sky-blue)
#  TEXT_PRI   : #F1F5F9
#  TEXT_SEC   : #94A3B8
#  DANGER     : #F43F5E
#  SUCCESS    : #10B981
# ─────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self, username, on_logout=None):
        super().__init__()
        self.on_logout = on_logout
        self._chat_visible = False
        
        # 1. Window Configuration
        self.setWindowTitle("Resumo")
        self.setMinimumSize(1200, 800)
        
        # --- GLOBAL THEME: DEEP OCEAN BLUE-VIOLET ---
        self.setStyleSheet("""
            QMainWindow { background: transparent; }
            QWidget {
                color: #F1F5F9;
                font-family: 'Segoe UI', 'Inter', sans-serif;
            }

            /* ── Popups / Dialogs ── */
            QMessageBox {
                background-color: #111827;
            }
            QMessageBox QLabel {
                color: #F1F5F9;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #1E2D4A;
                color: #FFFFFF;
                padding: 6px 16px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
                min-height: 25px;
            }
            QMessageBox QPushButton:hover {
                background-color: #5B4FE8;
            }
            QMessageBox QPushButton:pressed {
                background-color: #4A3FCE;
            }

            /* ── Sidebar ── */
            QFrame#Sidebar {
                background-color: #0F1928;
                border-right: 1px solid #1E3A5A;
            }

            /* ── App Title ── */
            QLabel#Header {
                font-size: 30px;
                font-weight: bold;
                color: #8B5CF6;
                background: transparent;
            }

            /* ── Generic Buttons ── */
            QPushButton {
                border-radius: 10px;
                font-size: 14px;
            }

            /* ── Analyze CTA ── */
            QPushButton#AnalyzeBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B4FE8, stop:1 #8B5CF6);
                color: #FFFFFF;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            QPushButton#AnalyzeBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6D62F0, stop:1 #9D72F8);
            }
            QPushButton#AnalyzeBtn:pressed {
                background: #4A3FCE;
            }

            /* ── Download Button ── */
            QPushButton#DownloadBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0EA5E9, stop:1 #38BDF8);
                color: #FFFFFF;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton#DownloadBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #38BDF8, stop:1 #7DD3FC);
            }
            QPushButton#DownloadBtn:pressed {
                background: #0284C7;
            }

            /* ── Text Areas ── */
            QTextEdit {
                background-color: #111827;
                border: 1.5px solid #1E2D4A;
                border-radius: 14px;
                padding: 15px;
                color: #F1F5F9;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1.5px solid #7C5CFC;
                background-color: #141D2E;
            }

            /* ── List Widget ── */
            QListWidget {
                background-color: transparent;
                border: none;
                color: #CBD5E1;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px 6px;
                border-radius: 8px;
                color: #CBD5E1;
            }
            QListWidget::item:hover {
                background-color: #1E2640;
                color: #F1F5F9;
            }
            QListWidget::item:selected {
                background-color: #1E2640;
                color: #8B5CF6;
                font-weight: bold;
            }

            /* ── Progress Bar ── */
            QProgressBar {
                border: none;
                border-radius: 8px;
                text-align: center;
                background-color: #141D2E;
                color: #F1F5F9;
                font-weight: bold;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B4FE8, stop:1 #8B5CF6);
                border-radius: 8px;
            }

            /* ── Tabs ── */
            QTabWidget::pane {
                border: none;
                background-color: #080D1A;
            }
            QTabBar::tab {
                background-color: #111827;
                color: #94A3B8;
                padding: 10px 18px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 3px;
                font-size: 12px;
                border: 1px solid #1E2D4A;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B4FE8, stop:1 #8B5CF6);
                color: #FFFFFF;
                font-weight: bold;
                border: none;
            }
            QTabBar::tab:hover {
                background-color: #1E2640;
                color: #F1F5F9;
            }

            /* ── Scrollbar ── */
            QScrollBar:vertical {
                background: #080D1A;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #1E2D4A;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #7C5CFC;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # ── Particle star-field setup ──────────────────────────────────────
        self._stars = [
            {
                "x": random.uniform(0, 2000),
                "y": random.uniform(0, 1500),
                "r": random.uniform(0.6, 2.2),
                "speed": random.uniform(0.15, 0.55),
                "alpha": random.randint(60, 200),
            }
            for _ in range(150)
        ]
        self._particle_timer = QTimer(self)
        self._particle_timer.timeout.connect(self._tick_particles)
        self._particle_timer.start(16)   # ~60 fps

        # Main Container
        main_widget = QWidget()

        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # =========================================================================
        # --- LEFT SIDEBAR ---
        # =========================================================================
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(320)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(20)
        
        # Drop Shadow on Sidebar
        sidebar_shadow = QGraphicsDropShadowEffect()
        sidebar_shadow.setBlurRadius(30)
        sidebar_shadow.setColor(QColor(0, 0, 0, 140))
        sidebar_shadow.setOffset(5, 0)
        self.sidebar.setGraphicsEffect(sidebar_shadow)

        # User Profile Section
        profile_card = QFrame()
        profile_card.setStyleSheet("""
            QFrame {
                background-color: #141D2E;
                border-radius: 14px;
                border: 1px solid #1E2D4A;
            }
        """)
        profile_layout = QHBoxLayout(profile_card)
        profile_layout.setContentsMargins(14, 14, 14, 14)
        
        self.prof_icon = QLabel()
        avatar_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "avatar.png")
        avatar_pixmap = QPixmap(avatar_path)
        self.prof_icon.setPixmap(avatar_pixmap.scaled(26, 26, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.prof_icon.setStyleSheet("background: transparent; border: none;")
        self.prof_icon.setFixedSize(45, 45)
        self.prof_icon.setAlignment(Qt.AlignCenter)
        
        prof_info = QVBoxLayout()
        prof_info.setSpacing(2)
        welcome_lbl = QLabel("Welcome back,")
        welcome_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; background: transparent; border: none;")
        self.prof_name = QLabel(f"{username}")
        self.prof_name.setStyleSheet("font-weight: bold; font-size: 15px; color: #F1F5F9; background: transparent; border: none;")
        prof_info.addWidget(welcome_lbl)
        prof_info.addWidget(self.prof_name)
        
        profile_layout.addWidget(self.prof_icon)
        profile_layout.addLayout(prof_info)
        profile_layout.addStretch()
        sidebar_layout.addWidget(profile_card)

        # --- TABBED SECTION: History + Vault ---
        self.sidebar_tabs = QTabWidget()

        # Tab 1: History
        history_tab = QWidget()
        history_tab.setStyleSheet("background-color: #0F1928;")
        history_tab_layout = QVBoxLayout(history_tab)
        history_tab_layout.setContentsMargins(5, 10, 5, 5)
        
        self.history_list = QListWidget()
        history_tab_layout.addWidget(self.history_list)
        self.sidebar_tabs.addTab(history_tab, " History")

        # Tab 2: Vault
        vault_tab = QWidget()
        vault_tab.setStyleSheet("background-color: #0F1928;")
        vault_tab_layout = QVBoxLayout(vault_tab)
        vault_tab_layout.setContentsMargins(5, 10, 5, 5)
        
        self.vault_list = QListWidget()
        vault_tab_layout.addWidget(self.vault_list)

        # Vault action buttons
        vault_actions_layout = QHBoxLayout()
        self.btn_vault_export = QPushButton(" Export")
        self.btn_vault_export.setCursor(Qt.PointingHandCursor)
        self.btn_vault_export.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B4FE8, stop:1 #8B5CF6);
                color: #FFFFFF; font-weight: bold;
                padding: 8px; border-radius: 8px; border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6D62F0, stop:1 #9D72F8);
            }
            QPushButton:pressed { background: #4A3FCE; }
        """)
        self.btn_vault_delete = QPushButton(" Delete")
        self.btn_vault_delete.setCursor(Qt.PointingHandCursor)
        self.btn_vault_delete.setStyleSheet("""
            QPushButton {
                background-color: #1E1525;
                color: #F43F5E;
                font-weight: bold;
                padding: 8px; border-radius: 8px;
                border: 1px solid #3D1A2A;
            }
            QPushButton:hover {
                background-color: #F43F5E;
                color: #FFFFFF;
                border: 1px solid #F43F5E;
            }
            QPushButton:pressed { background-color: #C7283E; }
        """)
        
        vault_actions_layout.addWidget(self.btn_vault_export)
        vault_actions_layout.addWidget(self.btn_vault_delete)
        vault_tab_layout.addLayout(vault_actions_layout)

        self.sidebar_tabs.addTab(vault_tab, " Vault")
        sidebar_layout.addWidget(self.sidebar_tabs)
        
        sidebar_layout.addStretch()

        # Exit Button
        self.btn_exit = QPushButton("⮜── Logout")
        self.btn_exit.setCursor(Qt.PointingHandCursor)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #141D2E;
                color: #94A3B8;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
                border: 1px solid #1E2D4A;
            }
            QPushButton:hover {
                background-color: #F43F5E;
                color: #FFFFFF;
                border: 1px solid #F43F5E;
            }
            QPushButton:pressed {
                background-color: #C7283E;
            }
        """)
        self.btn_exit.clicked.connect(self.handle_exit)
        sidebar_layout.addWidget(self.btn_exit)

        layout.addWidget(self.sidebar)

        # =========================================================================
        # --- MAIN CONTENT AREA ---
        # =========================================================================
        main_content = QWidget()
        main_layout = QVBoxLayout(main_content)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(25)

        # Top: App Logo/Name
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        logo_icon = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
        pixmap = QPixmap(logo_path)
        logo_icon.setPixmap(pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_icon.setStyleSheet("background: transparent; border: none;")
        
        self.app_logo = QLabel(" New Resume Is Calling...")
        self.app_logo.setObjectName("Header")
        self.app_logo.setStyleSheet("font-size: 26px; font-weight: 500;")
        
        header_layout.addWidget(logo_icon)
        header_layout.addWidget(self.app_logo)
        main_layout.addWidget(header_container)

        # Middle: Horizontal Input Boxes
        input_container = QHBoxLayout()
        input_container.setSpacing(30)
        
        # 1. JD Input Box
        self.jd_input = QTextEdit()
        self.jd_input.setPlaceholderText(
            "Paste the Job Description here...\n\n"
            "Example: Looking for a Python Developer with 3 years of experience in Django and MySQL..."
        )
        
        # 2. Right side vertical container
        right_container = QVBoxLayout()
        right_container.setSpacing(15)

        self.upload_box = QPushButton("📁\n\nUpload Resume\n(.pdf, .docx, .txt)")
        self.upload_box.setCursor(Qt.PointingHandCursor)
        self.upload_box.setMinimumHeight(150)
        self.upload_box.setStyleSheet("""
            QPushButton {
                background-color: #111827;
                border: 2px dashed #2E3A5A;
                border-radius: 15px;
                font-size: 15px;
                color: #94A3B8;
            }
            QPushButton:hover {
                background-color: #141D2E;
                border-color: #7C5CFC;
                color: #8B5CF6;
            }
        """)
        
        upload_shadow = QGraphicsDropShadowEffect()
        upload_shadow.setBlurRadius(15)
        upload_shadow.setColor(QColor(0, 0, 0, 80))
        upload_shadow.setOffset(0, 4)
        self.upload_box.setGraphicsEffect(upload_shadow)
        
        self.btn_analyze = QPushButton("✦  Analyze Match Score")
        self.btn_analyze.setObjectName("AnalyzeBtn")
        self.btn_analyze.setCursor(Qt.PointingHandCursor)
        self.btn_analyze.setMinimumHeight(55)
        
        analyze_shadow = QGraphicsDropShadowEffect()
        analyze_shadow.setBlurRadius(25)
        analyze_shadow.setColor(QColor(91, 79, 232, 120))
        analyze_shadow.setOffset(0, 6)
        self.btn_analyze.setGraphicsEffect(analyze_shadow)

        right_container.addWidget(self.upload_box)
        right_container.addWidget(self.btn_analyze)

        input_container.addWidget(self.jd_input, stretch=2)
        input_container.addLayout(right_container, stretch=1)
        main_layout.addLayout(input_container)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(500)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Missing Keywords Section
        self.keywords_container = QWidget()
        self.keywords_container.setVisible(False)
        keywords_layout = QVBoxLayout(self.keywords_container)
        keywords_layout.setContentsMargins(0, 0, 0, 0)
        keywords_layout.setSpacing(8)

        keywords_header = QLabel("  Missing Keywords from Job Description:")
        keywords_header.setStyleSheet("font-weight: bold; font-size: 14px; color: #38BDF8; background: transparent;")
        keywords_layout.addWidget(keywords_header)

        self.keywords_flow = QLabel("")
        self.keywords_flow.setWordWrap(True)
        self.keywords_flow.setStyleSheet("""
            background-color: #111827;
            border: 1px solid #1E2D4A;
            border-radius: 10px;
            padding: 12px;
            font-size: 13px;
            color: #8B5CF6;
        """)
        keywords_layout.addWidget(self.keywords_flow)

        main_layout.addWidget(self.keywords_container)

        # Results Area
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        self.results_area.setPlaceholderText("Analysis results will appear here after clicking 'Analyse'...")
        main_layout.addWidget(self.results_area)

        # Skeleton Loader (hidden by default)
        self.skeleton_label = QLabel("  Analyzing & Rewriting... Please wait.")
        self.skeleton_label.setAlignment(Qt.AlignCenter)
        self.skeleton_label.setStyleSheet("""
            font-size: 17px; color: #8B5CF6; font-weight: bold;
            padding: 40px; background-color: #111827;
            border: 2px dashed #1E2D4A; border-radius: 15px;
        """)
        self.skeleton_label.setVisible(False)
        main_layout.addWidget(self.skeleton_label)

        # Download Button
        self.btn_download = QPushButton(" Download Optimized Resume (.docx)")
        self.btn_download.setObjectName("DownloadBtn")
        self.btn_download.setCursor(Qt.PointingHandCursor)
        self.btn_download.setFixedWidth(380)
        self.btn_download.setFixedHeight(50)
        self.btn_download.setVisible(False)
        main_layout.addWidget(self.btn_download, alignment=Qt.AlignCenter)

        layout.addWidget(main_content)

        # --- FLOATING CHAT OVERLAY ---
        # Toggle Button
        self.btn_chat_toggle = QPushButton("💬", self)
        self.btn_chat_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_chat_toggle.setFixedSize(60, 60)
        self.btn_chat_toggle.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5B4FE8, stop:1 #8B5CF6);
                border-radius: 30px;
                font-size: 26px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6D62F0, stop:1 #9D72F8);
            }
        """)
        
        toggle_shadow = QGraphicsDropShadowEffect()
        toggle_shadow.setBlurRadius(24)
        toggle_shadow.setColor(QColor(91, 79, 232, 160))
        toggle_shadow.setOffset(0, 5)
        self.btn_chat_toggle.setGraphicsEffect(toggle_shadow)

        # Chat Box
        self.chat_widget = QFrame(self)
        self.chat_widget.setFixedSize(390, 490)
        self.chat_widget.setStyleSheet("""
            QFrame {
                background-color: #0D1525;
                border: 1px solid white;
                border-radius: 20px;
            }
        """)
        self.chat_widget.setVisible(False)
        
        chat_shadow = QGraphicsDropShadowEffect()
        chat_shadow.setBlurRadius(40)
        chat_shadow.setColor(QColor(0, 0, 0, 200))
        chat_shadow.setOffset(0, 10)
        self.chat_widget.setGraphicsEffect(chat_shadow)
        
        chat_layout = QVBoxLayout(self.chat_widget)
        chat_layout.setContentsMargins(20, 18, 20, 18)
        chat_layout.setSpacing(12)

        # Chat Header
        chat_header = QHBoxLayout()
        header_lbl = QLabel("         ✦  Alex - Career Assistant")
        header_lbl.setStyleSheet("""
            font-weight: bold; font-size: 15px;
            color: white; border: none; background: transparent;
        """)
        self.btn_chat_close = QPushButton("✖")
        self.btn_chat_close.setCursor(Qt.PointingHandCursor)
        self.btn_chat_close.setFixedSize(30, 30)
        self.btn_chat_close.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold; border: none; font-size: 16px;
            }
            QPushButton:hover { color: #F43F5E; }
        """)
        chat_header.addWidget(header_lbl)
        chat_header.addStretch()
        chat_header.addWidget(self.btn_chat_close)
        chat_layout.addLayout(chat_header)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #1E2D4A; max-height: 1px; border: none;")
        chat_layout.addWidget(separator)

        # Chat History
        self.chat_history_area = QTextEdit()
        self.chat_history_area.setReadOnly(True)
        self.chat_history_area.setStyleSheet("""
            QTextEdit {
                background-color: #111827;
                border: 1px solid white;
                border-radius: 12px;
                padding: 12px;
                font-size: 13px;
                color: #F1F5F9;
            }
        """)
        chat_layout.addWidget(self.chat_history_area)

        # Input Area
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask about resumes, recruitment...")
        self.chat_input.setStyleSheet("""
            QLineEdit {
                background-color: #111827;
                border: 1.5px solid #1E2D4A; 
                border-radius: 12px;
                padding: 10px 14px;
                color: #F1F5F9; 
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1.5px solid #7C5CFC;
                background-color: #141D2E;
            }
        """)
        
        self.btn_chat_send = QPushButton("➤")
        self.btn_chat_send.setCursor(Qt.PointingHandCursor)
        self.btn_chat_send.setFixedSize(42, 42)
        self.btn_chat_send.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B4FE8, stop:1 #8B5CF6);
                color: #FFFFFF; font-weight: bold;
                border-radius: 12px; font-size: 17px; border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6D62F0, stop:1 #9D72F8);
            }
            QPushButton:pressed { background: #4A3FCE; }
        """)
        
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(self.btn_chat_send)
        chat_layout.addLayout(input_layout)

    def toggle_chat(self):
        """Simple and robust toggle for chat visibility."""
        self._chat_visible = not self._chat_visible
        
        if self._chat_visible:
            chat_height = self.chat_widget.height()
            self.chat_widget.move(self.width() - 420, self.height() - chat_height - 80)
            self.chat_widget.setVisible(True)
            self.chat_widget.raise_()
        else:
            self.chat_widget.setVisible(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.btn_chat_toggle.move(self.width() - 90, self.height() - 90)
        if self._chat_visible:
            chat_height = self.chat_widget.height()
            self.chat_widget.move(self.width() - 420, self.height() - chat_height - 80)

    def handle_exit(self):
        if self.on_logout:
            self.on_logout()
        else:
            self.close()

    # ──────────────────────────── PARTICLE ANIMATION ──────────────────────
    def _tick_particles(self):
        """Move each star upward; wrap around to the bottom when off-screen."""
        for s in self._stars:
            s["y"] -= s["speed"]
            if s["y"] < -4:
                s["y"] = self.height() + 4
                s["x"] = random.uniform(0, self.width())
        self.update()   # trigger repaint

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
            # Only draw if within bounds for performance
            if 0 <= s["x"] <= self.width() and 0 <= s["y"] <= self.height():
                color = QColor(139, 92, 246, s["alpha"])  # violet tint
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(
                    int(s["x"] - s["r"]), int(s["y"] - s["r"]),
                    int(s["r"] * 2), int(s["r"] * 2)
                )
