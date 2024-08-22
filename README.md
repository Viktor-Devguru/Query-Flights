# Query Flights

항공권 조회 프로그램입니다. 사용자가 지정한 조건에 맞는 항공편을 검색하고 결과를 보여줍니다.

## 기능

- 출발지와 도착지 선택
- 최대 요금 설정
- 최대 비행 시간 설정
- 여행 기간 설정
- 최대 사용 휴가 일수 설정
- 조건에 맞는 항공편 검색 및 결과 표시

## 설치 방법

1. 이 저장소를 클론합니다:
   ```
   git clone https://github.com/Viktor-Devguru/Query-Flights.git
   cd query-flights
   ```

2. 필요한 패키지를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

## 사용 방법

### GUI 버전 실행

GUI 버전을 실행하려면 다음 명령어를 사용하세요:

```
python query_flights_gui.py
```

### 콘솔 버전 실행

콘솔 버전을 실행하려면 다음 명령어를 사용하세요:

```
python query_flights_core.py --scity ICN --ecity CTS --fare 250000 --duration 24 --day 3 --vacation 1
```

각 인자의 의미는 다음과 같습니다:
- `--scity`: 출발지 (기본값: ICN)
- `--ecity`: 도착지 (기본값: CTS)
- `--fare`: 최대 요금 (기본값: 250000)
- `--duration`: 최대 비행시간 (기본값: 24)
- `--day`: 여행 기간 (기본값: 3)
- `--vacation`: 최대 사용 휴가 일수 (기본값: 여행 기간과 동일)

## 실행 파일 빌드

Windows 환경에서 실행 파일을 빌드하려면 다음 명령어를 실행하세요:

```
build.bat
```

이 스크립트는 PyInstaller를 사용하여 단일 실행 파일을 생성합니다.

## 의존성

프로젝트의 주요 의존성은 다음과 같습니다:

- holidays==0.55
- PyQt6==6.7.1
- PyQt6_sip==13.8.0
- Requests==2.32.3

자세한 의존성 목록은 `requirements.txt` 파일을 참조하세요.

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)하에 배포됩니다. 단, 사용된 라이브러리들의 라이선스를 반드시 확인하고 준수해야 합니다:

- holidays: MIT 라이선스
- PyQt6: GPL v3 라이선스
- Requests: Apache 2.0 라이선스

각 라이브러리의 라이선스 조항을 꼭 확인하시기 바랍니다.
