import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QFormLayout, QGroupBox, QComboBox
from PyQt6.QtGui import QTextCursor, QRegularExpressionValidator, QGuiApplication, QIcon
from PyQt6.QtCore import QRegularExpression
from query_flights_core import query_flights, parse_args

class FlightQueryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.default_args = parse_args()
        self.WIDTH = 800
        self.HEIGHT = 800
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # Input fields
        input_group = QGroupBox("검색 조건")
        form_layout = QFormLayout()

        # 공항 리스트 (코드와 이름)
        self.airports = {
            "ICN": "인천", "GMP": "김포", "CJU": "제주", "PUS": "부산", 
            "CTS": "삿포로", "NRT": "도쿄/나리타", "HND": "도쿄/하네다", "KIX": "오사카", 
            "FUK": "후쿠오카", "HKG": "홍콩", "BKK": "방콕", "SGN": "호찌민", 
            "DPS": "발리", "SIN": "싱가포르", "TPE": "타이페이", "MNL": "마닐라", 
            "CEB": "세부", "BKI": "코타키나발루", "LAX": "로스앤젤레스", "JFK": "뉴욕",
            "CDG": "파리", "FCO": "로마", "BCN": "바르셀로나", "IST": "이스탄불"
        }

        self.scity_input = self.create_airport_combobox(self.default_args.scity)
        self.ecity_input = self.create_airport_combobox(self.default_args.ecity)

        self.fare_input = QLineEdit(self.default_args.fare)
        self.duration_input = QLineEdit(self.default_args.duration)
        self.day_input = QLineEdit(self.default_args.day)
        self.vacation_input = QLineEdit(str(self.default_args.vacation) if self.default_args.vacation else "")

        # Set validators
        number_validator = QRegularExpressionValidator(QRegularExpression(r'^\d+$'))
        self.fare_input.setValidator(number_validator)
        self.duration_input.setValidator(number_validator)
        self.day_input.setValidator(number_validator)
        self.vacation_input.setValidator(number_validator)

        form_layout.addRow("출발지:", self.scity_input)
        form_layout.addRow("도착지:", self.ecity_input)
        form_layout.addRow("최대 요금:", self.fare_input)
        form_layout.addRow("최대 비행시간:", self.duration_input)
        form_layout.addRow("여행 기간:", self.day_input)
        form_layout.addRow("최대 사용 휴가 일수:", self.vacation_input)

        input_group.setLayout(form_layout)
        main_layout.addWidget(input_group)

        # Search button
        self.search_button = QPushButton("Query!")
        self.search_button.clicked.connect(self.search_flights)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                font-family: 'Segoe UI', Arial, sans-serif;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        main_layout.addWidget(self.search_button)

        # Results area
        results_group = QGroupBox("검색 결과")
        results_layout = QVBoxLayout()
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        results_layout.addWidget(self.results_area)
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)

        self.setLayout(main_layout)
        self.setWindowTitle('Query Flights ✈️')        
        self.resize(self.WIDTH, self.HEIGHT) # 창 크기 설정
        
        # 화면 중앙으로 위치
        qr = self.frameGeometry()
        screen = QGuiApplication.primaryScreen()
        cp = screen.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
        """)

    def create_airport_combobox(self, default_code):
        combo = QComboBox()
        combo.setEditable(True)
        for code, name in self.airports.items():
            combo.addItem(f"{code} ({name})", code)
        combo.setCurrentText(f"{default_code} ({self.airports[default_code]})")
        combo.setValidator(QRegularExpressionValidator(QRegularExpression(r'^[A-Za-z]+$')))
        combo.editTextChanged.connect(lambda text: combo.setEditText(text.upper()))
        return combo

    def get_airport_code(self, combo):
        text = combo.currentText()
        code = text.split()[0] if ' ' in text else text
        return code if code in self.airports else text
    
    def appendConstraints(self, args):
        self.results_area.append(f"출발지: {args.scity}")
        self.results_area.append(f"도착지: {args.ecity}")
        self.results_area.append(f"최대 요금: {int(args.fare):,}원")
        self.results_area.append(f"최대 비행시간: {args.duration}시간")
        self.results_area.append(f"여행 기간: {args.day}일")
        if args.vacation:
            self.results_area.append(f"최대 사용 휴가 일수: {args.vacation}일")
        self.results_area.append("\n")

    def search_flights(self):
        args_list = [
            '--scity', self.get_airport_code(self.scity_input),
            '--ecity', self.get_airport_code(self.ecity_input),
            '--fare', self.fare_input.text(),
            '--duration', self.duration_input.text(),
            '--day', self.day_input.text(),
        ]
        if self.vacation_input.text():
            args_list.extend(['--vacation', self.vacation_input.text()])

        args = parse_args(args_list)

        flights = query_flights(args)

        self.results_area.clear()
        # self.appendConstraints(args)

        for flight in flights:
            self.results_area.append(flight.get_flight_data())
            self.results_area.append(flight.get_flight_link())
            self.results_area.append("\n")

        self.results_area.moveCursor(QTextCursor.MoveOperation.Start)
        self.results_area.ensureCursorVisible()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # 현재 실행 파일의 위치를 기반으로 아이콘 파일 경로 설정
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        application_path = sys._MEIPASS
    else:
        # 디버그 또는 스크립트 실행 시
        application_path = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(application_path, 'airplane.ico')
    app.setWindowIcon(QIcon(icon_path))

    ex = FlightQueryApp()
    ex.show()
    sys.exit(app.exec())