import requests
import json
import datetime
from multiprocessing.pool import ThreadPool

class LOTTEMovieInfo:

    def LOTTENomalCrawingInfo(self,branch_name,branch_code,totalInfo) :
        time = datetime.datetime.now()
        CineCode = "1004"
        urls = "http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx?nocashe=0.10753130276220801"
        company = "Lotte"

        Bookingurl = "http://www.lottecinema.co.kr/LCHS/Contents/Cinema/Cinema-Detail.aspx?divisionCode=1&detailDivisionCode=1&cinemaID="
        
        param = {
            "ParamList": '{"MethodName":"GetPlaySequence","channelType":"HO","osType":"Chrome","osVersion":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36","playDate":"2019-'
                + str(time.month) + '-' + str(time.day) + '","cinemaID":"1|1|' + str(branch_code) + '","representationMovieCode":""}'
        }

        response = requests.post(urls, param)
        parseResult = json.loads(response.text)
        for items in parseResult['PlaySeqs']['Items']:
            data = {
                'company': company,
                'branch': items['CinemaNameKR'],
                'movie': items['MovieNameKR'],
                'viewGrade': items['ViewGradeNameKR'],
                'hall' : items['ScreenNameKR'],
                'special' : items['ScreenDivisionNameKR'],
                "time": items['StartTime'],
                "link": Bookingurl+branch_code,
                "remainSeat": str(items['BookingSeatCount'])+"석/"+str(items['TotalSeatCount'])+"석"
            }
            totalInfo.append(data)

    def LOTTEspecialCrawingInfo(self,trash,totalInfo):
        time = datetime.datetime.now()
        LOTTE_Special = []
        LOTTE_Special.append({
            'cinemaCategoryCode': '300',
            'branch': {
                "월드타워": '1016',
                '건대입구': '1004',
                '에비뉴엘': '1001'
            }
        })
        LOTTE_Special.append({
            'cinemaCategoryCode': '941',
            'branch': {
                '월드타워': '1016'
            }
        })
        LOTTE_Special.append({
            'cinemaCategoryCode': '980',
            'branch': {
                '월드타워': '1016',
                '건대입구': '1004',
            }
        })
        LOTTE_Special.append({
            'cinemaCategoryCode': '930',
            'branch': {
                '월드타워': '1016',
                '가산디지털': '1013',
                '노원': '1003',
                '청량리': '1008'
            }
        })
        LOTTE_Special.append({
            'cinemaCategoryCode': '960',
            'branch': {
                '월드타워': '1016',
            }
        })
        LOTTE_Special.append({
            'cinemaCategoryCode': '200',
            'branch': {
                '월드타워': '1016',
                '은평(롯데몰)': '1021',
                '합정': '1010',
                '노원': '1003'
            }
        })
        urls = "http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx?nocashe=0.10753130276220801"
        company = "Lotte"

        for Lotte_branch in LOTTE_Special:
            Bookingurl = "http://www.lottecinema.co.kr/LCHS/Contents/Cinema/Cinema-Detail.aspx?divisionCode=2&detailDivisionCode=" + \
                         Lotte_branch['cinemaCategoryCode'] + "&cinemaID="

            for branch in Lotte_branch['branch']:
                param = {
                    "ParamList": '{"MethodName":"GetPlaySequence","channelType":"HO","osType":"Chrome","osVersion":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36","playDate":"2019-'
                        + str(time.month) + '-' + str(time.day) + '","cinemaID":"2|' + Lotte_branch['cinemaCategoryCode'] + '|' + str(
                        Lotte_branch['branch'][branch]) + '","representationMovieCode":""}'
                }

                response = requests.post(urls, param)
                parseResult = json.loads(response.text)
                for items in parseResult['PlaySeqs']['Items']:
                    if items['ScreenDivisionNameKR'] == '' or items['ScreenDivisionNameKR'] == '일반':
                        continue
                    data = {
                        'company': company,
                        'branch': items['CinemaNameKR'],
                        'movie': items['MovieNameKR'],
                        'viewGrade': items['ViewGradeNameKR'],
                        'hall' : items['ScreenNameKR'],
                        'special': items['ScreenDivisionNameKR'],
                        "time": items['StartTime'],
                        "link": Bookingurl + Lotte_branch['branch'][branch],
                        "remainSeat": str(items['BookingSeatCount']) + "석/" + str(items['TotalSeatCount']) + "석"
                    }
                    totalInfo.append(data)
        return totalInfo


    def __init__(self):
        self.Lotte_branch = {
            "가산디지털" : "1013",
            "가양" : "1018",
            "강동" : "9010",
            "건대입구" : "1004",
            "김포공항" : "1009",
            "노원" : "1003",
            "독산" : "1017",
            "브로드웨이(신사)" : "9056",
            "서울대입구" : "1012",
            "수락산" : "1019",
            "수유" : '1022',
            "신도림" : "1015",
            "신림" : "1007",
            "에비뉴엘(명동)" : "1001",
            "영등포" : "1002",
            "용산" : "1014",
            "월드타워" : "1016",
            "은평(롯데몰)" : "1021",
            "장안" : "9053",
            "청량리" : "1008",
            "합정" : "1010",
            "홍대입구" : "1005",
            "황학" : "1011"
        }

