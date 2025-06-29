import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QHBoxLayout, QStackedLayout,
    QDialog, QComboBox, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QMovie, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class CustomWarning(QDialog):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setStyleSheet("background-color: white; color: black;")
        self.setFixedSize(360, 160)
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setWordWrap(True)
        label.setStyleSheet("font-size: 14px; color: black;")
        label.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(label)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setFixedWidth(80)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: black;
                border: 1px solid #888;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch()
        layout.addSpacing(10)
        layout.addLayout(btn_layout)
        layout.addStretch()
        self.setLayout(layout)


class AnomalyDetectorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anomaly Detection")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #0e1b2c;")
        self.selected_file = None

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.main_widget = QWidget()
        self.loading_widget = QWidget()
        self.result_widget = QWidget()
        self.attack_type_widget = QWidget()

        self.init_main_ui()
        self.init_loading_ui()
        self.init_result_ui()
        self.init_attack_type_ui()

        self.stack.addWidget(self.main_widget)
        self.stack.addWidget(self.loading_widget)
        self.stack.addWidget(self.result_widget)
        self.stack.addWidget(self.attack_type_widget)

        self.stack.setCurrentWidget(self.main_widget)

    def init_main_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(80, 40, 40, 20)

        self.left_container = QVBoxLayout()
        self.left_container.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.left_container.setSpacing(15)

        title = QLabel("Детекция\nаномалий")
        font = QFont("Segoe UI", 54)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #fefefe;")
        title.setAlignment(Qt.AlignCenter)
        self.left_container.addWidget(title)
        self.left_container.addSpacing(-15)

        subtitle = QLabel("с применением ML")
        font = QFont("Segoe UI", 28)
        font.setWeight(QFont.Light)
        subtitle.setFont(font)
        subtitle.setStyleSheet("color: #b0b3b8;")
        self.left_container.addWidget(subtitle)

        self.model_label = QLabel("Выбрать модель:")
        self.model_label.setFont(QFont("Segoe UI", 24))
        self.model_label.setStyleSheet("color: white; margin-bottom: 10px")
        self.left_container.addWidget(self.model_label)
        self.left_container.addSpacing(-10)

        self.model_combo = QComboBox()
        self.model_combo.setFixedSize(330, 40)
        self.model_combo.addItems([
            "Случайный лес (по умолчанию)", "Наивный Байес", "Многослойный перцептрон",
            "К-ближайших соседей", "Адаптивный бустинг"
        ])
        self.model_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #606060;
                border-radius: 4px;
                padding: 5px;
                font-size: 20px;
                font-family: 'Segoe UI Semibold';
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #3b82f6;
                selection-color: white;
                font-size: 16px;
                font-family: 'Segoe UI';
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                background-color: #e0e0e0;
                border-left: 1px solid #cccccc;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                margin-right: 8px;
            }
        """)
        self.left_container.addWidget(self.model_combo)

        self.left_container.addSpacing(10)

        self.upload_btn = QPushButton("Загрузить файл")
        self.upload_btn.setFixedSize(250, 65)
        self.upload_btn.setFont(QFont("Segoe UI", 22))
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.upload_btn.clicked.connect(self.upload_pcap)
        self.left_container.addWidget(self.upload_btn)

        self.start_btn = QPushButton("Начать анализ")
        self.start_btn.setFixedSize(250, 55)
        self.start_btn.setFont(QFont("Segoe UI", 22))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.start_btn.clicked.connect(self.start_analysis)
        self.start_btn.setVisible(False)
        self.left_container.addWidget(self.start_btn)

        left_wrapper = QVBoxLayout()
        left_wrapper.setAlignment(Qt.AlignTop)
        left_wrapper.addLayout(self.left_container)

        layout.addLayout(left_wrapper, stretch=10)
        layout.addSpacing(40)

        right_layout = QVBoxLayout()
        image = QLabel()
        pixmap = QPixmap("anomaly_illustration.png")
        image.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image.setAlignment(Qt.AlignCenter)
        image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addStretch()
        right_layout.addWidget(image)
        right_layout.addStretch()

        layout.addLayout(right_layout, stretch=10)
        self.main_widget.setLayout(layout)

    def init_loading_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Ищем аномалии, подождите...")
        label.setFont(QFont("Segoe UI", 30))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)

        gif = QLabel()
        movie = QMovie("loading.gif")
        movie.setScaledSize(QSize(120, 120))
        gif.setMovie(movie)
        gif.setAlignment(Qt.AlignCenter)
        movie.start()

        layout.addStretch()
        layout.addWidget(label)
        layout.addWidget(gif)
        layout.addStretch()
        self.loading_widget.setLayout(layout)

    def start_analysis(self):
        if not self.selected_file:
            self.show_warning("Нет файла", "Пожалуйста, загрузите PCAP-файл.")
            return

        file_size = os.path.getsize(self.selected_file)
        if file_size > 10 * 1024 * 1024 * 1024:
            self.show_warning("Слишком большой", "Файл превышает 10 ГБ.")
            return

        with open(self.selected_file, "rb") as f:
            if f.read(4) == b"\x0a\x0d\x0d\x0a":
                self.show_warning("Неподдерживаемый формат", "Формат PCAPNG не поддерживается.")
                return

        self.stack.setCurrentWidget(self.loading_widget)
        QApplication.processEvents()
        time.sleep(3)

        result = {"benign_threads": 87, "attack_threads": 601}
        self.stack.setCurrentWidget(self.result_widget)
        self.show_result(result)

    def upload_pcap(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "PCAP Files (*.pcap)")
        if file_name:
            self.selected_file = file_name
            self.start_btn.setVisible(True)

    def show_result(self, result):
        self.canvas.figure.clf()
        fig = self.canvas.figure
        fig.patch.set_facecolor('none')
        ax = fig.add_subplot(111)
        ax.set_facecolor("none")

        ax.pie(
            [result["benign_threads"], result["attack_threads"]],
            labels=["Легитимный", "Аномальный"],
            autopct="%1.1f%%",
            colors=["#33BBFF", "#FF7A64"],
            textprops={"color": "white", "fontsize": 14},
            radius=1.5,
            
        )
        self.canvas.draw()
        self.model_chosen_label.setText("Выбранная модель: Случайный лес")
        self.result_info.setText(
            f"Легитимные потоки: {result['benign_threads']}\nАномальные потоки: {result['attack_threads']}"
        )
        #self.alert_label.setText("⚠ Высокий уровень аномалий!" if result["attack_threads"] > 400 else "")

    def init_result_ui(self):
        self.result_layout = QVBoxLayout()
        self.result_layout.setContentsMargins(20, 20, 20, 20)

        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon("back_icon.png"))
        self.back_btn.setIconSize(QSize(40, 40))
        self.back_btn.setFixedSize(60, 60)
        self.back_btn.setStyleSheet("background-color: transparent; border: none;")
        self.back_btn.clicked.connect(self.go_back_to_main)
        self.result_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)

        label = QLabel("Результаты анализа трафика")
        label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)

        self.model_chosen_label = QLabel()
        self.model_chosen_label.setFont(QFont("Segoe UI", 20))
        self.model_chosen_label.setStyleSheet("color: #cccccc;")
        self.model_chosen_label.setAlignment(Qt.AlignCenter)

        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        self.canvas.setStyleSheet("background-color: #0e1b2c;")

        self.result_info = QLabel()
        self.result_info.setFont(QFont("Segoe UI", 18))
        self.result_info.setStyleSheet("color: white;")
        self.result_info.setAlignment(Qt.AlignCenter)

        self.alert_label = QLabel()
        self.alert_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.alert_label.setStyleSheet("color: red;")
        self.alert_label.setAlignment(Qt.AlignCenter)

        self.attack_type_btn = QPushButton("Определить тип атаки")
        self.attack_type_btn.setFont(QFont("Segoe UI", 20))
        self.attack_type_btn.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                color: white;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #d97706;
            }
        """)
        self.attack_type_btn.clicked.connect(self.detect_attack_type)

        self.result_layout.addWidget(label)
        self.result_layout.addWidget(self.model_chosen_label)
        self.result_layout.addWidget(self.canvas)
        self.result_layout.addWidget(self.result_info)
        self.result_layout.addWidget(self.alert_label)
        self.result_layout.addWidget(self.attack_type_btn, alignment=Qt.AlignCenter)
        self.result_widget.setLayout(self.result_layout)

    def detect_attack_type(self):
        self.stack.setCurrentWidget(self.loading_widget)
        QTimer.singleShot(3000, lambda: self.stack.setCurrentWidget(self.attack_type_widget))

    def init_attack_type_ui(self):
        layout = QVBoxLayout()
        self.attack_back_btn = QPushButton()
        self.attack_back_btn.setIcon(QIcon("back_icon.png"))
        self.attack_back_btn.setIconSize(QSize(40, 40))
        self.attack_back_btn.setFixedSize(60, 60)
        self.attack_back_btn.setStyleSheet("background-color: transparent; border: none;")
        self.attack_back_btn.clicked.connect(self.go_back_to_main)
        layout.addWidget(self.attack_back_btn, alignment=Qt.AlignLeft)

        title = QLabel("Типы атак в данном файле:")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        main_attack = QLabel("DoS GoldenEye - вероятность 92.1%")
        main_attack.setFont(QFont("Segoe UI", 36, QFont.Bold))
        main_attack.setStyleSheet("color: #f59e0b;")
        main_attack.setAlignment(Qt.AlignCenter)
        layout.addWidget(main_attack)

        self.toggle_btn = QPushButton("Подробнее ↓")
        self.toggle_btn.setFont(QFont("Segoe UI", 20))
        self.toggle_btn.setFixedSize(220, 60)
        self.toggle_btn.setStyleSheet("background-color: #374151; color: white; border-radius: 6px;")
        self.toggle_btn.clicked.connect(self.toggle_details)
        layout.addWidget(self.toggle_btn, alignment=Qt.AlignCenter)

        self.extra_attacks_widget = QWidget()
        extra_layout = QVBoxLayout()
        extra_layout.setAlignment(Qt.AlignCenter)
        for attack, prob in {
            "Heartbleed": 0.2, "Infiltration": 0.05, "Botnet (Bot)": 0.1, "DoS Hulk": 3.5,
            "DoS Slowloris": 1.8, "Portscan": 0.3, "DoS Slowhttptest": 1.1, "DDoS": 0.7,
            "FTP-Patator": 0.05, "Web Attack": 0.05, "SSH-Patator": 0.05
        }.items():
            lbl = QLabel(f"{attack} - {prob}%")
            lbl.setFont(QFont("Segoe UI", 16))
            lbl.setStyleSheet("color: white;")
            extra_layout.addWidget(lbl)
        self.extra_attacks_widget.setLayout(extra_layout)
        self.extra_attacks_widget.setVisible(False)
        layout.addWidget(self.extra_attacks_widget)

        self.attack_type_widget.setLayout(layout)

    def toggle_details(self):
        visible = self.extra_attacks_widget.isVisible()
        self.extra_attacks_widget.setVisible(not visible)
        self.toggle_btn.setText("Скрыть ↑" if not visible else "Подробнее ↓")

    def go_back_to_main(self):
        self.stack.setCurrentWidget(self.main_widget)

    def show_warning(self, title, message):
        CustomWarning(title, message).exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnomalyDetectorUI()
    window.show()
    sys.exit(app.exec_())
