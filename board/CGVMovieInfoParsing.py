from bs4 import BeautifulSoup
import requests
import datetime

class CGVMovieInfo :
    def CGVCrawingInfo(self,branch_name,branchCode,totalInfo,specialInfo):
        
        mainUrl = "http://www.cgv.co.kr"
        time = datetime.datetime.now()
        company = "CGV"
        ##지점별 검색
        day = str(time.year)+str(time.month)+str(time.day)
        url = mainUrl+"/common/showtimes/iframeTheater.aspx?areacode=01&date="+day+"&theatercode="+branchCode
        response = requests.get(url)
        parseResult = BeautifulSoup(response.text,'html.parser')
        branchMovies = []
        movieResults = parseResult.find_all('div',class_='col-times')
        for movieResult in movieResults:
        #영화 이름 별로 검색
            playingTable = []
            halInfo = movieResult.find('div',class_='info-hall').find_all('li')


            theaters = movieResult.find_all('div',class_='type-hall')
            for theater in theaters:
                if(branch_name == "천호") :
                    print(theater)
                screenType = theater.find('span', class_="screentype")
                if screenType != None:
                    screenType = screenType.getText().strip()
                else:
                    screenType = "일반"

                #영화 이름당 할당된 관 검색
                showResults = theater.find_all('a')
                for showResult in showResults:
                    #하나의 관에 상영이 몇개인지 검색
                    data = {
                        'company': company,
                        'branch': branch_name,
                        'movie': movieResult.find('strong').getText().strip(),
                        'viewGrade': theater.find('li').getText().strip(),
                        'special' : screenType,
                        "time": showResult.find('em').getText().strip(),
                        "link": mainUrl + showResult['href'],
                        "remainSeat": showResult.find('span',class_='txt-lightblue').getText().strip()[4:] + "/" + halInfo[2].getText().strip()[3:].strip()
                    }
                    if screenType == '일반':
                        totalInfo.append(data)
                    else :
                        specialInfo.append(data)
    def __init__(self):
        self.CGV_branch = {
            '강남' : '0056',
            '동대문' : '0252',
            '미아': '0057',
            '영등포': '0059',
            '수유': '0276',
            '강변': '0001',
            '등촌': '0230',
            '불광': '0030',
            '왕십리': '0074',
            '신촌': '0150',
            '건대입구': '0229',
            '명동x이진혁': '0009',
            '상봉': '0046',
            '용산': '0013',
            '압구정': '0040',
            '구로': '0010',
            '명동 시네마': '0105',
            '성신여대': '0300',
            '중계': '0131',
            '여의도': '0112',
            '대학로': '0063',
            '목동': '0011',
            '송파': '0088',
            '천호': '0199',
            '청담': '0107',
            '피카디리': '0223',
            '하계': '0164',
            '홍대': '0191',
        }

