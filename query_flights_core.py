import argparse
import requests
import sys
import holidays
from datetime import datetime, timedelta

DEFAULT_ARGS = {
    '--scity': {'type': str, 'default': 'ICN', 'help': '출발지'},
    '--ecity': {'type': str, 'default': 'CTS', 'help': '도착지'},
    '--fare': {'type': str, 'default': '250000', 'help': '최대 요금'},
    '--duration': {'type': str, 'default': '24', 'help': '최대 비행시간'},
    '--day': {'type': str, 'default': '3', 'help': '여행 기간'},
    '--vacation': {'type': str, 'default': None, 'help': '최대 사용 휴가 일수'}
}

AIRLINE_CODES = {
    'ZE': '이스타항공(ZE)',
    'NH': '전일본공수/ANA(NH)',
    'KE': '대한항공(KE)',
    'LJ': '진에어(LJ)',
    'OZ': '아시아나항공(OZ)',
    '7C': '제주항공(7C)',
    'MU': '중국동방항공(MU)',
    'TW': '티웨이항공(TW)',
    'SC': '산동항공(SC)',
    'BX': '에어부산(BX)',
    'FM': '상하이항공(FM)',
    'VN': '베트남항공(VN)',
    'CA': '중국국제항공(CA)',
    'JL': '일본항공(JL)',
    'SQ': '싱가포르항공(SQ)',
    'TG': '타이항공(TG)',
    'CX': '캐세이퍼시픽(CX)',
    'UA': '유나이티드항공(UA)',
    'AA': '아메리칸항공(AA)',
    'DL': '델타항공(DL)',
    'AF': '에어프랑스(AF)',
    'LH': '루프트한자(LH)',
    'EK': '에미레이트항공(EK)',
    'QR': '카타르항공(QR)',
    'BA': '브리티시 에어웨이즈(BA)',
    'TK': '터키항공(TK)',
    'ET': '에티하드항공(ET)'
}

def request_flights(scity, ecity, day, duration, fare):
    url = "https://airline-api.naver.com/graphql"
    headers = {
        "accept": "*/*",
        "accept-language": "ko,en;q=0.9,en-US;q=0.8",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://flight.naver.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

    body = {
        "operationName": "flight_recommend_by_city",
        "variables": {
            "scity": f"{scity}",
            "ecity": f"{ecity}",
            "roundTripTime": f"{day},{day}",
            "duration": f"1,{duration}",
            "fare": f"10000,{fare}"
        },
        "query": """
        query flight_recommend_by_city(
            $scity: String, 
            $ecity: String, 
            $duration: String, 
            $stops: Int, 
            $sdate: String, 
            $continents: String, 
            $roundTripTime: String, 
            $fare: String, 
            $themes: String
        ) {
            recommendByCity(
                scity: $scity
                ecity: $ecity
                duration: $duration
                stops: $stops
                sdate: $sdate
                continents: $continents
                roundTripTime: $roundTripTime
                fare: $fare
                themes: $themes
            ) {
                airline
                sdate1
                sdate2
                price
                stops
                roundTripTime
            }
        }
        """
    }
    return requests.post(url, json=body, headers=headers)

class Flight:
    kr_holidays = holidays.KR(years=[datetime.now().year, datetime.now().year + 1])

    def __init__(self, scity, ecity, fare, duration, day, vacation_limit, sdate1, sdate2, roundTripTime, price, airline, stops):
        self.scity = scity
        self.ecity = ecity
        self.fare = int(fare)
        self.duration = int(duration)
        self.day = int(day)
        self.vacation_limit = int(vacation_limit)
        self.vacation_req = None
        self.sdate1 = datetime.strptime(sdate1, '%Y%m%d')
        self.sdate2 = datetime.strptime(sdate2, '%Y%m%d')
        self.roundTripTime = int(roundTripTime)
        self.price = int(price)
        self.airline = airline
        self.stops = int(stops)

    def calc_required_vacation_days(self):
        # 여행 기간 동안의 휴일 카운팅
        holiday_count = 0
        for i in range((self.sdate2 - self.sdate1).days + 1):
            date = self.sdate1 + timedelta(days=i)
            if date in self.kr_holidays or date.weekday() >= 5: # 5:토요일, 6:일요일
                holiday_count += 1
        
        # 사용해야 되는 휴가 수
        self.vacation_req = (self.sdate2 - self.sdate1).days + 1 - holiday_count

    def get_weekday_kr(self, date):
        return '월화수목금토일'[date.weekday()]

    def get_flight_data(self):
        return f"출발: {self.sdate1:%Y/%m/%d}({self.get_weekday_kr(self.sdate1)}), 복귀: {self.sdate2:%Y/%m/%d}({self.get_weekday_kr(self.sdate2)}), 일정: {self.roundTripTime}일, {f'휴가사용: {self.vacation_req}일, ' if self.vacation_req else ''}요금: {self.price:,}원, 항공사: {AIRLINE_CODES.get(self.airline, self.airline)}, 경유횟수: {self.stops}"
    
    def get_flight_link(self):
        return f"https://flight.naver.com/flights/international/{self.scity}-{self.ecity}-{self.sdate1:%Y%m%d}/{self.ecity}-{self.scity}-{self.sdate2:%Y%m%d}?adult=1&fareType=Y"

def printArgs(args):
    print(f"출발지: {args.scity}")
    print(f"도착지: {args.ecity}")
    print(f"최대 요금: {int(args.fare):,}원")
    print(f"최대 비행시간: {args.duration}시간")
    print(f"여행 기간: {args.day}일")
    print(f"최대 사용 휴가 일수: {args.vacation}일")

# 필터링된 항공권 목록 반환
def query_flights(args):
    response = request_flights(args.scity, args.ecity, args.day, args.duration, args.fare)
    response_json = response.json()
    datas = response_json['data']['recommendByCity']
 
    flights = []
    for data in datas:
        flight = Flight(args.scity, args.ecity, args.fare, args.duration, args.day, args.vacation, data['sdate1'], data['sdate2'], data['roundTripTime'], data['price'], data['airline'], data['stops'])

        # 휴가 사용 제한 체크
        if flight.vacation_limit < flight.day:
            flight.calc_required_vacation_days()
            if flight.vacation_req > flight.vacation_limit:
                continue

        flights.append(flight)
  
    return flights  

def parse_args(args=None):
    class CustomArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write(f'error: {message}\n')
            self.print_help()
            sys.exit(2)
            
    parser = CustomArgumentParser(
        description='항공권 조회 프로그램 😛',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    for arg, kwargs in DEFAULT_ARGS.items():
        parser.add_argument(arg, **kwargs)

    parsed_args = parser.parse_args(args)    
    if parsed_args.vacation is None:
        parsed_args.vacation = parsed_args.day
    
    return parsed_args

if __name__ == '__main__':
    # 디버깅용
    if sys.gettrace():
        sys.argv += ['--day', '3', '--fare', '250000', '--vacation', '1']

    args = parse_args()
    
    print("항공권 조회 프로그램 😛")    
    printArgs(args)
    print()
    
    flights = query_flights(args)    
    for flight in flights:
        print(flight.get_flight_data())
        print(f"\t{flight.get_flight_link()}")