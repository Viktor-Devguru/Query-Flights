@echo off
echo ==================== Starting build process ====================

REM 이전 빌드 파일 정리
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "Query Flights.spec" del "Query Flights.spec"

REM 필요한 패키지 설치
echo ==================== Installing required packages ====================
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install requirements
    exit /b %errorlevel%
)

echo ==================== Installing PyInstaller ====================
pip install pyinstaller==6.10.0
if %errorlevel% neq 0 (
    echo Failed to install PyInstaller
    exit /b %errorlevel%
)

REM PyInstaller를 사용하여 실행 파일 생성
echo ==================== Building executable ====================
pyinstaller --onefile --windowed --name "Query Flights" --icon=airplane.ico --add-data "airplane.ico:." --hidden-import holidays.countries --hidden-import holidays.countries.korea .\query_flights_gui.py
if %errorlevel% neq 0 (
    echo Failed to build executable
    exit /b %errorlevel%
)

echo ==================== Build process completed ====================
pause