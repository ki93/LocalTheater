from bs4 import BeautifulSoup
import requests
from multiprocessing.pool import ThreadPool

# response = requests.get(url)
class MEGABOXMovieInfo:

    def MEGABOXNomalCrawingInfo(self,branch_name,branch_code,totalInfo):
        
        urls = "http://www.megabox.co.kr/pages/theater/Theater_Schedule.jsp"
        linkUrl = "http://www.megabox.co.kr/?menuId=theater-detail&region=10&cinema="

        company = "MEGABOX"
        #지점별
        TicktetingURL = linkUrl+branch_code
        param = {'cinema': branch_code}
        response = requests.post(urls, param)
        parseResult = BeautifulSoup(response.text, 'html.parser')
        TheaterParses = parseResult.find_all('tr',class_="lineheight_80")

        #영화명별
        for TheaterParse in TheaterParses:
            temp = TheaterParse.find('strong').getText().strip()
            if temp != '':
                movieName = TheaterParse.find('strong').getText().strip()
                movieGrade = TheaterParse.find('span', class_='age_m').getText().strip()
                hall = TheaterParse.find('th', id='th_theaterschedule_room').find('div').getText().strip()

            showingParses = TheaterParse.find_all('div',class_='cinema_time')

            #영화 관별
            for showingParse in showingParses:

                seat = showingParse.find('span',class_='seat').getText().strip()
                seatToken = seat.split('/')
                if len(seatToken) != 2:
                    remainSeat = seat
                else :
                    remainSeat = seatToken[0]+"석/" + seatToken[1]+"석"
                data = {
                    'company': company,
                    'branch' : branch_name,
                    'movie': movieName,
                    'viewGrade': movieGrade,
                    'hall' : hall,
                    'special' : '일반',
                    "time" : showingParse.find('span',class_='time').getText().strip(),
                    "link" : TicktetingURL,
                    "remainSeat" : remainSeat,
                }
                totalInfo.append(data)
        
        
    def MEGABOXSpecialCrawingInfo(self,trash,specialInfo):
        MEGABOX_branch = {
            "강남" : '1372',
            "강남대로" : '1359',
            "강동" : '1341',
            "군자" : '1431',
            "동대문" : '1003',
            "마곡" : '1572',
            "목동" : '1581',
            "상봉" : '1311',
            "상암월드컵경기장" : '1211',
            "성수" : '1331',
            "센트럴" : '1371',
            "송파파크하비오" : '1381',
            "신촌" : '1202',
            "은평" : '1221',
            "이수" :  '1561',
            "창동" : '1321',
            "코엑스" : '1351',
            "홍대" : '1212',
            "화곡" : '1571',
            "ARTNINE" : '1562'
        }
        MEGABOXSpecial = []
        MEGABOXSpecial.append({
            'special' : 'The Boutique',
            'screenType' : '10',
            'branch' : ['성수','센트럴','코엑스']
        })
        MEGABOXSpecial.append({
            'special' : 'MX',
            'screenType': '01',
            'branch': ['목동', '상암월드컵경기장', '성수','코엑스']
        })
        MEGABOXSpecial.append({
            'special' : 'comfort',
            'screenType': '12',
            'branch': ['동대문', '목동', '상봉','상암월드컵경기장','신촌','코엑스']
        })

        urls = "http://www.megabox.co.kr/pages/special/Theater_Schedule.jsp"
        
        company = "MEGABOX"
        for special in MEGABOXSpecial:
            linkUrl = "http://www.megabox.co.kr/?menuId=special-detail&screenType="+special['screenType']+"&cinema="
            MEGABOX_TargetBranch = special['branch']
            #지점별
            for branch in MEGABOX_TargetBranch:
                TicktetingURL = linkUrl+MEGABOX_branch[branch]
                param = {'cinema': MEGABOX_branch[branch],'screenType' : special['screenType']}
                response = requests.post(urls, param)
                parseResult = BeautifulSoup(response.text, 'html.parser')
                TheaterParses = parseResult.find_all('tr',class_="lineheight_80")

                #영화명별
                for TheaterParse in TheaterParses:
                    temp = TheaterParse.find('strong').getText().strip()
                    if temp != '':
                        movieName = TheaterParse.find('strong').getText().strip()
                        movieGrade = TheaterParse.find('span', class_='age_m').getText().strip()
                        hall = TheaterParse.find('th', id='th_theaterschedule_room').find('div').getText().strip()
                    showingParses = TheaterParse.find_all('div',class_='cinema_time')

                    #영화 관별
                    for showingParse in showingParses:

                        seat = showingParse.find('span',class_='seat').getText().strip()
                        seatToken = seat.split('/')
                        if len(seatToken) != 2:
                            remainSeat = seat
                        else :
                            remainSeat = seatToken[0]+"석/" + seatToken[1]+"석"
                        data = {
                            'company': company,
                            'branch' : branch,
                            'movie': movieName,
                            'viewGrade': movieGrade,
                            'hall' : hall,
                            'special' : special['special'],
                            "time" : showingParse.find('span',class_='time').getText().strip(),
                            "link" : TicktetingURL,
                            "remainSeat" : remainSeat,
                        }
                        specialInfo.append(data)
        return specialInfo

    def __init__(self):
        self.MEGABOX_branch = {
            "강남" : '1372',
            "강남대로" : '1359',
            "강동" : '1341',
            "군자" : '1431',
            "동대문" : '1003',
            "마곡" : '1572',
            "목동" : '1581',
            "상봉" : '1311',
            "상암월드컵경기장" : '1211',
            "성수" : '1331',
            "센트럴" : '1371',
            "송파파크하비오" : '1381',
            "신촌" : '1202',
            "은평" : '1221',
            "이수" :  '1561',
            "창동" : '1321',
            "코엑스" : '1351',
            "홍대" : '1212',
            "화곡" : '1571',
            "ARTNINE" : '1562'
        }

